from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, Iterator, Literal, Optional

import joblib
from diskcache import Cache
from loguru import logger
from tqdm import tqdm
from tree_sitter import Node

from sweepai.config.client import SweepConfig
from sweepai.config.server import CACHE_DIRECTORY
from sweepai.modify.validate.code_validators import EXT_TO_LANGUAGE, get_language
from sweepai.search.agent.code_tree import CodeTree
from sweepai.utils.cache import hash_code
from sweepai.utils.timer import Timer

entities_cache = Cache(f"{CACHE_DIRECTORY}/entities_cache")
ENTITIES_CACHE_VERSION = "v0.1"

# Future: migrate to https://github.com/tree-sitter/tree-sitter-graph
# TODO: python built-in methods are not being recognized properly
# TODO: add better support for raw import statements and aliases
# for testing s exp queries, go to https://tree-sitter.github.io/tree-sitter/playground
# all s_exp stored in sweepai/search/agent/tree_sitter_querys/[language].scm


def clip(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


@dataclass
class LanguageConfig:
    language: str
    s_exp_query: str
    builtin_variables: set[str]
    builtin_modules: set[str]
    builtin_methods: set[str]
    config_directory: ClassVar[str] = "sweepai/search/agent/tree_sitter_queries"

    @classmethod
    def from_language(cls, language: str):
        s_exp_query = open(f"{cls.config_directory}/{language}.scm").read()
        metadata_path = f"{cls.config_directory}/{language}.json"
        if os.path.exists(metadata_path):
            with open(metadata_path) as f:
                metadata = json.load(f)
        else:
            metadata = {}
        return cls(
            language=language,
            s_exp_query=s_exp_query,
            builtin_variables=set(metadata.get("variables", [])),
            builtin_modules=set(metadata.get("modules", [])),
            builtin_methods=set(metadata.get("methods", [])),
        )

    @cached_property
    def builtin_modules_pattern(self):
        return re.compile("^(" + f"|".join(self.builtin_modules) + ").*")

    def is_builtin_module(self, module: str) -> bool:
        module = module.strip('"')
        return self.builtin_modules_pattern.fullmatch(module)

    @classmethod
    def get_available_languages(cls):
        return [
            file_path.removesuffix(".scm")
            for file_path in os.listdir(cls.config_directory)
            if file_path.endswith(".scm")
        ]

    @classmethod
    def load_all(cls):
        return {language: cls.from_language(language) for language in cls.get_available_languages()}


LANGUAGE_CONFIGS = LanguageConfig.load_all()


def parse_potential_entity_from_line(query_to_get_entity_from: str):
    if "::" in query_to_get_entity_from:
        split_query_with_potential_entity = query_to_get_entity_from.split("::")
    elif ":" in query_to_get_entity_from:
        split_query_with_potential_entity = query_to_get_entity_from.split(":")
    else:
        return "", query_to_get_entity_from
    file_path, entity_name = (
        split_query_with_potential_entity[0],
        split_query_with_potential_entity[1],
    )
    return file_path, entity_name


# Based on: https://tree-sitter.github.io/tree-sitter/code-navigation-systems#examples, with a few modifications
node_types = [
    "definition.import",
    "definition.constant",
    "definition.class",
    "definition.function",
    "definition.method",
    "definition.parameter",
    "definition.interface",
    "definition.variable",
    "definition.type",
    "reference.call",
    "reference.class",
    "reference.implementation",
    "reference.type",
]


class Serializable:
    """Can use Pydantic but Pydantic is a bit of a pita to work with."""

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Entity(Serializable):
    name: str
    type: Literal[
        "definition.constant",
        "definition.class",
        "definition.function",
        "definition.method",
        "definition.interface",
        "definition.variable",
        "definition.type",
        "reference.call",
        "reference.class",
        "reference.implementation",
        "reference.type",
    ]

    start_line: int
    end_line: int
    start_char: int
    end_char: int

    file_path: str
    language: str
    role: Literal["definition", "reference"]
    contents: str | None = None
    metadata: dict[str, dict] = field(default_factory=dict)
    parent: Optional[Entity] = None

    @classmethod
    def from_node(
        cls,
        name: str,
        type: Literal[
            "definition.constant",
            "definition.class",
            "definition.function",
            "definition.method",
            "definition.interface",
            "definition.variable",
            "definition.type",
            "reference.call",
            "reference.class",
            "reference.implementation",
            "reference.type",
        ],
        node: Node,
        file_path: str,
        parent: Optional[Entity] = None,
        **kwargs,
    ):
        role, entity_type = type.split(".")
        start_char = node.start_byte
        end_char = node.end_byte

        contents = " " * node.start_point[1] + node.text.decode()
        parent_node = node.parent
        if (
            parent_node
            and max((parent_node.end_point[0] - parent_node.start_point[0]), 1)
            / max(node.end_point[0] - node.start_point[0], 1)
            <= 2
        ):
            # continuously check parent
            contents = " " * parent_node.start_point[1] + parent_node.text.decode()
            start_char = parent_node.start_byte
            end_char = parent_node.end_byte
        data = {
            "name": name,
            "type": type,
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
            "file_path": file_path,
            "start_char": start_char,
            "end_char": end_char,
            "parent": parent,
            "contents": contents,
        }
        if entity_type == "import":
            return Import(**data, **kwargs)
        elif role == "definition":
            return Definition(**data, **kwargs)
        else:
            return Reference(**data, **kwargs)

    def hydrate(self, file_contents: str):
        self.contents = file_contents[self.start_char : self.end_char + 1]
        for attr in ["parent", "object", "referenced_entity", "resolved_entity"]:
            if hasattr(self, attr) and (entity := getattr(self, attr)):
                entity.hydrate(file_contents)

    @property
    def entity_type(self):
        return self.type.split(".")[-1]

    @property
    def file_denotation(self):
        return f"{self.file_path}:{self.start_line}-{self.end_line}"

    @property
    def full_reference(self):
        return f"{self.file_path}:{self.full_name}"

    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.full_name}.{self.name}"
        return self.name

    def __str__(self):
        return self.full_name

    def get_parents(self):
        if self.parent:
            return self.parent.get_parents() + [self.parent]
        return []

    def to_dict(self):
        data = {**super().to_dict()}
        if "contents" in data:
            del data["contents"]
        if "node" in data:
            del data["node"]
        for attr in ["parent", "object", "referenced_entity", "resolved_entity"]:
            if attr in data and data[attr] and isinstance(data[attr], Serializable):
                data[attr] = data[attr].to_dict()
        return data

    @classmethod
    def from_dict(cls, **kwargs):
        role, entity_type = kwargs["type"].split(".")
        for attr in ["parent", "object", "referenced_entity", "resolved_entity"]:
            if attr in kwargs and kwargs[attr]:
                kwargs[attr] = cls.from_dict(**kwargs[attr])
        if entity_type == "import":
            return Import(
                **kwargs,
            )
        elif role == "definition":
            return Definition(
                **kwargs,
            )
        else:
            return Reference(
                **kwargs,
            )


@dataclass
class Definition(Entity):
    scope: Literal["local", "global"] = "global"
    role: Literal["definition"] = "definition"
    type_annotation: str | None = None

    def __post_init__(self):
        if self.entity_type == "function" and self.parent and self.parent.entity_type == "class":
            self.type = "definition.method"
        if self.parent and self.parent.entity_type != "class":
            self.scope = "local"


@dataclass
class Import(Definition):
    module: str = ""

    def __post_init__(self):
        if self.language == "go":
            self.module = self.name
            self.name = self.name.strip('"').split("/")[-1]
        elif self.language == "python":
            if not self.module.endswith(".py"):
                self.module = self.module.replace(".", "/")
                self.module += ".py"


@dataclass
class Reference(Entity):
    referenced_entity: Optional[Entity] = None  # e.g. the import that contains this reference
    resolved_entity: Optional[Entity] = None  # e.g. the actual definition of this reference
    origin_type: Literal["defined", "builtin", "imported", "unknown"] = "unknown"
    role: Literal["reference"] = "reference"
    object: Entity | None = None

    def __post_init__(self):
        # TODO: classify into variable, types, functions etc.
        builtins = LANGUAGE_CONFIGS[self.language].builtin_variables
        if self.name in builtins:
            self.origin_type = "builtin"
        elif self.name in LANGUAGE_CONFIGS[self.language].builtin_methods and self.object:
            self.origin_type = "builtin"

    @property
    def full_name(self):
        name = self.name
        if self.object:
            name = f"{self.object}.{self.name}"
        if self.parent:
            return f"{self.parent.full_name}.{name}"
        return name


def get_parents(node: Node) -> Iterator[Node]:
    parent = node.parent
    while parent:
        yield parent
        parent = parent.parent


@dataclass
class FileEntities(Serializable):
    """
    TODO: add general query support
    """

    key: str
    definitions: dict[str, Definition] = field(default_factory=dict)
    references: list[Reference] = field(default_factory=list)
    node_id_mapping: dict[int, str] = field(default_factory=dict)

    def all_entities(self) -> list[Entity]:
        return sorted([*self.definitions.values(), *self.references], key=lambda x: x.start_line)

    @classmethod
    def get_query(cls, language_name: str):
        if not hasattr(cls, "query_cache"):
            cls.query_cache = {}
        query = cls.query_cache.get(language_name, None)
        if query is None:
            language_config = LANGUAGE_CONFIGS[language_name]
            language = get_language(language_name)
            query = language.query(language_config.s_exp_query)
            cls.query_cache[language_name] = query
        return query

    @classmethod
    def from_file(cls, file_path: str, cwd: str = "", key: str = "", no_cache: bool = False) -> FileEntities | None:
        language_name = file_path.split(".")[-1]
        language_name = EXT_TO_LANGUAGE.get(language_name, language_name)
        if language_name not in LANGUAGE_CONFIGS:
            return None
        if not os.path.exists(file_path):
            return None  # This edge case only happens when back-testing

        if not no_cache:
            file_contents_for_hash = open(file_path, "r").read()
            key = f"{key}-{hash_code(file_contents_for_hash)}"
            if cached_entities := cls.from_cache(key):
                return cached_entities

        code_tree = CodeTree.from_file(file_path)  # 30% of time spent here
        file_contents = code_tree.code
        file_bytes = code_tree.code.encode()
        query = cls.get_query(language_name)
        matches = query.matches(code_tree.tree.root_node)
        entities_mapping = cls(key=key)
        # entities: dict[str, Entity] = {} # maps names to Entities
        for _id, match in matches:
            match_type = None
            name_node = match["name"]
            node = None
            for key in node_types:
                if key in match:
                    match_type = key
                    node = match[key]
            if match_type:
                name = file_bytes[name_node.start_byte : name_node.end_byte].decode("utf-8")
                parent_name = ""
                kwargs = {}
                for parent in get_parents(node):
                    if parent.id in entities_mapping.node_id_mapping:
                        parent_name = entities_mapping.node_id_mapping[parent.id]
                        break
                if match_type == "definition.import" and "module" in match:
                    kwargs["module"] = file_contents[match["module"].start_byte : match["module"].end_byte]
                if match_type == "definition.variable" and "type" in match:
                    kwargs["type_annotation"] = file_contents[match["type"].start_byte : match["type"].end_byte]
                if "object" in match:
                    if match["object"].id in entities_mapping.node_id_mapping:
                        kwargs["object"] = entities_mapping.definitions[
                            entities_mapping.node_id_mapping[match["object"].id]
                        ]
                    else:
                        object_name = file_contents[match["object"].start_byte : match["object"].end_byte]
                        kwargs["object"] = Entity.from_node(
                            name=object_name,
                            type="reference.variable",
                            node=match["object"],
                            file_path=file_path.removeprefix(cwd + os.sep),
                            parent=entities_mapping.definitions.get(parent_name),
                            language=language_name,
                        )
                entity = Entity.from_node(
                    name,
                    match_type,
                    node,
                    file_path.removeprefix(cwd + os.sep),
                    entities_mapping.definitions.get(parent_name),
                    language=language_name,
                    **kwargs,
                )
                entities_mapping.add_entity(entity, node.id)
        # Single file resolution
        for entity in entities_mapping.references:
            entities_mapping.resolve_entity(entity)
        # entities_mapping.to_cache()
        return entities_mapping

    def get_entity(self, name: str, scope: list[str] = []):
        current_scope = scope
        while True:
            full_name = ".".join([frame for frame in current_scope] + [name])
            if full_name in self.definitions:
                # match up the types
                return self.definitions[full_name]
            if len(current_scope) == 0:
                break
            current_scope.pop()

    def add_entity(self, entity: Entity, node_id: int):
        if entity.role == "definition":
            self.definitions[entity.full_name] = entity
            self.node_id_mapping[node_id] = entity.full_name
        else:
            self.references.append(entity)

    def resolve_entity(self, entity: Reference):
        language_config = LANGUAGE_CONFIGS[entity.language]
        if entity.origin_type != "builtin":
            referenced_entity = self.get_entity(entity.name, [parent.name for parent in entity.get_parents()])
            if referenced_entity:
                entity.referenced_entity = referenced_entity
                entity.origin_type = "defined"
                if referenced_entity.type_annotation:
                    entity.type_annotation = (
                        referenced_entity.type_annotation
                    )  # not sure if this is the best way to do it
                    # use a node later
                    if entity.type_annotation in self.definitions:
                        type_definition_entity = self.definitions[entity.type_annotation]
                        if type_definition_entity.entity_type == "import":
                            if language_config.is_builtin_module(type_definition_entity.module):
                                entity.origin_type = "builtin"
                            else:
                                entity.origin_type = "imported"
                        elif type_definition_entity.entity_type == "type":
                            entity.origin_type = "defined"
                if referenced_entity.entity_type == "import":
                    if language_config.is_builtin_module(referenced_entity.module):
                        entity.origin_type = "builtin"
                    else:
                        entity.origin_type = "imported"
                else:
                    entity.resolved_entity = referenced_entity
            if not entity.referenced_entity:
                if entity.object:
                    # check object in the parent scope
                    referenced_entity = self.get_entity(
                        entity.object.name,
                        [parent.name for parent in entity.get_parents()],
                    )
                    if referenced_entity:
                        entity.referenced_entity = referenced_entity
                        type_name = referenced_entity.type_annotation
                        if type_name:
                            type_entity = self.get_entity(
                                type_name,
                                [parent.name for parent in entity.get_parents()],
                            )
                            if type_entity:
                                referenced_type_entity = self.get_entity(
                                    referenced_entity.type_annotation,
                                    [parent.name for parent in entity.get_parents()],
                                )
                                if isinstance(referenced_type_entity, Import) and language_config.is_builtin_module(
                                    referenced_type_entity.module
                                ):
                                    entity.origin_type = "builtin"
                                else:
                                    entity.origin_type = "imported"
                                return entity
                        referenced_name = (
                            entity.referenced_entity.module
                            if isinstance(entity.referenced_entity, Import)
                            else entity.referenced_entity.name
                        )
                        if language_config.is_builtin_module(referenced_name):
                            entity.origin_type = "builtin"
                        else:
                            entity.origin_type = "imported"
                        return entity
                elif entity.language == "go" or entity.language == "java":
                    entity.origin_type = "imported"
        return entity

    def hydrate(self, file_contents: str):
        for entity in self.definitions.values():
            entity.hydrate(file_contents)
        for entity in self.references:
            entity.hydrate(file_contents)

    @classmethod
    def from_dict(cls, data: dict, key: str):
        try:
            return cls(
                key=key,
                definitions={name: Entity.from_dict(**entity) for name, entity in data["definitions"].items()},
                references=[Entity.from_dict(**entity) for entity in data["references"]],
            )
        except Exception:
            logger.error(f"Error deserializing entity: {data}")
            return None

    def to_dict(self):
        return {
            "key": self.key,
            "definitions": {name: entity.to_dict() for name, entity in self.definitions.items()},
            "references": [entity.to_dict() for entity in self.references],
        }

    def to_cache(self):
        with Timer(f"serializing: {self.key}", min_time=0.01):
            obj = self.to_dict()
        entities_cache[self.key] = obj

    @classmethod
    def from_cache(cls, key: str):
        if results := entities_cache.get(key, None):
            with Timer(f"deserializing: {key}", min_time=0.05):
                return cls.from_dict(results, key=key)


def gitignored_walk(directory: str, sweep_config: SweepConfig) -> Iterator[str]:
    with subprocess.Popen(
        ["git", "ls-files", "--recurse-submodules"],
        stdout=subprocess.PIPE,
        cwd=directory,
    ) as proc:
        for line in proc.stdout:
            file_path = line.decode().strip()
            if not sweep_config.is_file_excluded_aggressive(directory, file_path):  # filters out auto-generated files
                yield file_path


# TODO: handle multi-root workspaces


def serialize(data):
    if isinstance(data, list):
        return [serialize(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize(value) for key, value in data.items()}
    elif isinstance(data, Serializable):
        return serialize(data.to_dict())
    else:
        return data


def get_file_entities_from_file(file_path: str, dir_path: str, key: str):
    if os.path.isdir(os.path.join(dir_path, file_path)):
        return None
    with Timer(f"FileEntities.from_file({file_path})", min_time=0.1):
        entities = FileEntities.from_file(
            os.path.join(dir_path, file_path),
            cwd=dir_path,
            key=f"{key}:{file_path}",
            no_cache=True,
        )
    return (file_path, entities) if entities else None


@dataclass
class EntitiesIndex(Serializable):
    key: str
    # file path -> entity name -> entity
    entities_mapping: dict[str, FileEntities] = field(default_factory=dict)
    definitions_index: dict[str, list[Entity]] = field(default_factory=dict)
    # (file path, entity name) -> entity[]
    usages_index: dict[str, list[Reference]] = field(default_factory=dict)
    entities_search_cache: dict[tuple[str, str], list[Entity]] = field(default_factory=dict)

    def __repr__(self):
        return f"EntitiesIndex({self.key}, {len(self.entities_mapping)} files, {len(self.definitions_index)} definitions, {len(self.usages_index)} usages)"

    @classmethod
    def from_dir(cls, dir_path: str, key: str = "", no_cache: bool = False) -> EntitiesIndex:
        key = key or dir_path
        if not no_cache and (cached_index := entities_cache.get(key)) is not None:
            return cached_index
        files_to_entities = cls.ingest_dir(dir_path, key=key)
        definitions_index: dict[str, list[Entity]] = {}
        for _, entities_mapping in files_to_entities.items():
            for name, entity in entities_mapping.definitions.items():
                if entity.scope == "global":
                    definitions_index.setdefault(entity.name, []).append(entity)
        results = cls(
            key=key,
            entities_mapping=files_to_entities,
            definitions_index=definitions_index,
        )
        if not no_cache:
            with Timer("hydrating entities"):
                results.hydrate(dir_path)
        with Timer("resolving references"):
            results.resolve_references()
        entities_cache[key] = results
        return results

    @staticmethod
    def ingest_dir(
        dir_path: str,
        dirs_to_ingest: list[str] = [],
        key: str = "",
    ) -> dict[str, FileEntities]:
        # Helper functio to ingest entities from a directory
        files_to_entities = {}
        sweep_config = SweepConfig()
        file_list = list(gitignored_walk(dir_path, sweep_config))
        # TODO: make this configurable
        # TODO: make caching better
        if dirs_to_ingest:
            file_list = [
                file_path for file_path in file_list if any(dir_path in file_path for dir_path in dirs_to_ingest)
            ]
        with Timer("ingesting files"):
            workers = clip(len(file_list), 1, 8)
            # specify to use thread
            try:

                results = joblib.Parallel(n_jobs=workers, backend="multiprocessing")(
                    joblib.delayed(get_file_entities_from_file)(file_path, dir_path, key) for file_path in file_list
                )
            except Exception as e:
                logger.error(f"Error ingesting entities: {e}")
                results = [get_file_entities_from_file(file_path, dir_path, key) for file_path in file_list]
            files_to_entities.update(dict(filter(None, results)))
        return files_to_entities

    def resolve_references(self):
        for entities_mapping in tqdm(
            self.entities_mapping.values(),
            desc="Resolving references",
            total=len(self.entities_mapping),
        ):
            for entity in entities_mapping.references:
                if entity.origin_type == "imported":
                    module_path = (
                        entity.referenced_entity.module
                        if isinstance(entity.referenced_entity, Import)
                        else os.path.dirname(entity.file_path)
                    )
                    resolved_entities = self.get_entities(entity.name, module_path)

                    if resolved_entities:
                        entity.resolved_entity = resolved_entities[0]
                        self.usages_index.setdefault(
                            f"{entity.resolved_entity.file_path}:{entity.resolved_entity.name}",
                            [],
                        ).append(entity)
                        # logger.debug(f"{entity.full_reference} -> {entity.resolved_entity.full_reference}")
                        entity.origin_type = "imported"  # for go lang
                    else:
                        # logger.warning(f"Could not resolve {entity.full_name} from {entity.file_denotation}")
                        if entity.language == "go" and not entity.object:
                            entity.origin_type = "unknown"  # for go lang
                elif entity.referenced_entity:
                    self.usages_index.setdefault(
                        f"{entity.referenced_entity.file_path}:{entity.referenced_entity.name}",
                        [],
                    ).append(entity)
        # breakpoint()

    def retrieve_entities(self, query: str, include_imports: bool = True):
        # This one loops through get_entities and tries many different variations
        file_path, entity_name = parse_potential_entity_from_line(query)
        *path, entity_name = entity_name.split(".")
        popped_items = ""
        while path:
            current_entity_name = ".".join(path + [entity_name])
            if entities := self.get_entities(
                current_entity_name,
                file_path + popped_items,
                include_imports=include_imports,
            ):
                return entities
            popped_items += "." + path.pop()
        return self.get_entities(entity_name, file_path + popped_items, include_imports=include_imports)

    def get_entities(self, name: str, module_path: str, include_imports: bool = True) -> list[Definition]:
        # This one checks the name and sorts by module_path
        if cached_entities := self.entities_search_cache.get((name, module_path), None):
            return cached_entities
        entities = self.definitions_index.get(name, [])
        if not include_imports:
            entities = [entity for entity in entities if entity.entity_type != "import"]
        # LCS handles the case where the module path is a substring of the file path
        from rapidfuzz.distance import LCSseq  # lazy import for speedup

        entities = sorted(
            entities,
            key=lambda x: (
                x.entity_type != "import",  # de-prioritize imports
                LCSseq.similarity(x.file_path, module_path) if module_path else 0,
                len(self.usages_index.get(f"{x.file_path}:{x.name}", [])),
            ),
            reverse=True,
        )
        # TODO: refactor this out
        self.entities_search_cache[(name, module_path)] = entities
        return entities

    def get_dependencies(self, entity: Entity):
        file_entities = self.entities_mapping[entity.file_path]
        dependencies: list[Reference] = []
        for reference in file_entities.references:
            if reference.start_line >= entity.start_line and reference.end_line <= entity.end_line:
                dependencies.append(reference)
        return dependencies

    def get_entities_data(self, symbol: str, file_path: str = "") -> dict[str, list[Entity]]:
        definitions = self.retrieve_entities(f"{file_path}:{symbol}")
        return {
            "definitions": definitions,
            "usages": self.usages_index.get(f"{file_path}:{symbol}", []),
            "dependencies": (self.get_dependencies(definitions[0]) if definitions else []),
        }

    def hydrate(self, dir_path: str):
        new_entities_mapping = {}
        for file_path, file_entities in tqdm(self.entities_mapping.items(), total=len(self.entities_mapping)):
            try:
                file_contents = open(os.path.join(dir_path, file_path)).read()
            except FileNotFoundError:
                continue
            file_entities.hydrate(file_contents)
            new_entities_mapping[file_path] = file_entities
        self.entities_mapping = new_entities_mapping
        new_definitions_index = {}
        for entities in tqdm(self.definitions_index.values(), total=len(self.definitions_index)):
            for entity in entities:
                try:
                    file_contents = open(os.path.join(dir_path, entity.file_path)).read()
                except FileNotFoundError:
                    continue
                entity.hydrate(file_contents)
                new_definitions_index.setdefault(entity.name, []).append(entity)
        self.definitions_index = new_definitions_index
        new_usages_index = {}
        for usages in tqdm(self.usages_index.values(), total=len(self.usages_index)):  # this one is a bit slower
            for usage in usages:
                try:
                    file_contents = open(os.path.join(dir_path, usage.file_path)).read()
                except FileNotFoundError:
                    continue
                usage.hydrate(file_contents)
                new_usages_index.setdefault(usage.file_path, []).append(usage)
        self.usages_index = new_usages_index

    def to_dict(self):
        data = super().to_dict()
        data["entities_search_cache"] = {}
        return data

    @classmethod
    def from_dict(cls, data):
        with Timer("loading entities mapping"):
            entities_mapping = {
                file_path: FileEntities.from_dict(entities_mapping)
                for file_path, entities_mapping in tqdm(
                    data["entities_mapping"].items(), desc="Loading entities mapping"
                )
            }
        with Timer("loading remaining"):
            definitions_index = {
                name: [Entity.from_dict(**entity) for entity in entities]
                for name, entities in data["definitions_index"].items()
            }
            usages_index = {
                file_path: [Entity.from_dict(**entity) for entity in entities]
                for file_path, entities in data["usages_index"].items()
            }
            results = cls(
                key=data["key"],
                entities_mapping=entities_mapping,
                definitions_index=definitions_index,
                usages_index=usages_index,
            )
        return results
