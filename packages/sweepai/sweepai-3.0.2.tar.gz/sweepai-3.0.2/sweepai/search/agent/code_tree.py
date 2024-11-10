import warnings
from functools import cached_property

from loguru import logger
from pydantic import BaseModel
from tree_sitter import Node, Tree

from sweepai.modify.validate.code_validators import get_parser

warnings.simplefilter("ignore", category=FutureWarning)


def get_indentation(text: str):
    return text.removesuffix(text.lstrip())


def add_line_numbers(text: str, start_line: int, width: int):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        lines[i] = f"{start_line + i:{width}} | {line}"
    return "\n".join(lines)


def get_entity_name_raw(node: Node, language: str = ""):
    # WARNING: .named_child is not safe to call, can seg fault
    if node is None:
        return None
    if (
        node.type
        in (
            # shared
            "comment",
            "string",
            # go lang
            "package_clause",
            "import_declaration",
            # python
            "import_statement",
            "import_from_statement",
            "if_statement",  # for python if __name__ == "__main__":
            "try_statement",
        )
        or not node.is_named
    ):
        return None
    match node.type:
        case "function_declaration":
            # go lang
            return node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
        case "method_declaration":
            try:
                # go lang
                # query.matches(node)
                receiver = (
                    node.child_by_field_name("receiver").named_children[0].named_children[0].text
                )  # pyright: ignore[reportOptionalMemberAccess]
                name = node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
                return receiver + b"." + name
            except Exception:
                # java
                # class methods are called method_declaration
                prefix = b""
                parent = node.parent
                while parent:
                    if parent.type == "class_declaration":
                        class_name = get_entity_name_raw(parent, language=language)
                        prefix = class_name + b"."
                    parent = parent.parent
                return prefix + node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
        case "type_declaration" | "var_declaration" | "const_declaration":
            # go lang
            # TODO: this can return None.text
            return (
                node.named_children[0].child_by_field_name("name").text
            )  # pyright: ignore[reportOptionalMemberAccess]
        case "expression_statement":
            # python
            if node.named_children[0].child_by_field_name("left") is None:
                return None
            return (
                node.named_children[0].child_by_field_name("left").text
            )  # pyright: ignore[reportOptionalMemberAccess]
        case "function_definition" | "class_definition":
            # python
            # Check if this is a class method
            prefix = b""
            parent = node.parent
            while parent:
                if parent.type == "class_definition":
                    class_name = get_entity_name_raw(parent, language=language)
                    prefix = class_name or b"" + b"."
                parent = parent.parent
            return prefix + node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
        case "decorated_definition":
            # python
            return get_entity_name_raw(
                node.named_children[-1], language=language
            )  # pyright: ignore[reportOptionalMemberAccess]
        case "export_statement":
            # typescript
            return get_entity_name_raw(node.child_by_field_name("declaration"), language=language)  # type: ignore
        case "variable_declarator" | "lexical_declaration":
            # typescript
            return (
                node.named_children[0].child_by_field_name("name").text
            )  # pyright: ignore[reportOptionalMemberAccess]
        case "type_alias_declaration":
            # typescript
            return node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
        case "class_declaration":
            # java
            return node.child_by_field_name("name").text  # pyright: ignore[reportOptionalMemberAccess]
        case "field_declaration":
            # java
            # these are fields in a class
            prefix = b""
            parent = node.parent
            while parent:
                if parent.type == "class_declaration":
                    class_name = get_entity_name_raw(parent, language=language)
                    prefix = class_name or b"" + b"."
                parent = parent.parent
            if len(node.named_children) > 2:
                return (
                    prefix + node.named_children[2].named_children[0].text
                )  # pyright: ignore[reportOptionalMemberAccess]
            else:
                # one example is `Class field_name = null;`, in this case there is no named_children[2]
                return (
                    prefix + node.named_children[1].named_children[0].text
                )  # pyright: ignore[reportOptionalMemberAccess]


def get_entity_name(node: Node, language: str = "") -> str | None:
    try:
        entity_name = get_entity_name_raw(node, language=language)
        if entity_name:
            return entity_name.decode()
    except Exception as e:
        logger.exception(e)
    return None


def entity_name_in_entities(entity_name: str | None, entities: list[str]):
    if entity_name:
        return any(entity in entity_name for entity in entities)
    return False


class CodeTree(BaseModel):
    code: str
    language: str
    tree: Tree
    import_types: list[str] = [
        "import_statement",
        "import_from_statement",
        "import_declaration",
    ]
    always_expand_statements: list[str] = [
        "const_declaration",
    ]
    always_expand_files: list[str] = ["sql", "html"]
    # all possible class names
    class_definition_types: list[str] = [
        "class_definition",
        "decorated_definition",
        "class_declaration",
    ]

    class Config:
        arbitrary_types_allowed = True

    @cached_property
    def encoded_code(self):
        return self.code.encode("utf-8")

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as f:
            code = f.read()
        language = file_path.split(".")[-1]
        return cls.from_code(code, language=language)

    @classmethod
    def from_code(cls, code: str, language: str = "python"):
        parser = get_parser(language)
        tree = parser.parse(bytes(code, "utf8"))
        return cls(code=code, language=language, tree=tree)

    def get_entities_spans(self, min_lines: int = 5):
        entities_spans = {}
        lines = self.code.splitlines()
        current_children = self.tree.root_node.children
        while current_children:
            child = current_children.pop(0)
            start_line, _ = child.start_point
            end_line, end_char = child.end_point

            # For whatever reason, sometimes self.code is only a subset of the actual file.
            # This issue would pop up: https://sweep-ai.sentry.io/issues/5778360738
            # Unfortunately, I am unable to reproduce it locally, even with the same file.
            # The only way to bandaid fix it is to add this check, but the root cause is probably upstream.
            end_line = min(end_line, len(lines) - 1)

            if end_char == len(lines[end_line]):
                end_line += 1

            if end_line - start_line < min_lines:
                continue

            named_children = child.named_children
            if named_children:
                current_children.extend(named_children[-1].children)
            if start_line not in entities_spans:
                entities_spans[start_line] = end_line
        return entities_spans

    def get_boundaries(
        self,
        min_lines: int = 25,
    ):
        # TODO: always add last import
        entities_spans = self.get_entities_spans(min_lines=min_lines)
        spans = sorted(entities_spans.items())

        endpoints = []
        for start_line, end_line in spans:
            weight = end_line - start_line
            endpoints.append((start_line, weight))
            endpoints.append((end_line, weight))
        endpoints.sort(key=lambda x: x[0])

        anchors = []
        current_anchor = -1
        current_weight = 0
        for endpoint, weight in endpoints:
            if current_anchor != -1 and endpoint - current_anchor < min_lines:
                if weight > current_weight:
                    current_anchor = endpoint
                    current_weight = weight
            else:
                if current_anchor != -1:
                    anchors.append(current_anchor)
                current_anchor = endpoint
                current_weight = weight
        anchors.append(current_anchor)
        return anchors

    def get_preview(
        self,
        entities: list[str] = [],
        min_lines: int = 5,
    ) -> tuple[str, dict[str, tuple[int, int]], list[str]]:
        """
        Get preview for a file with entities to be expanded, imports should always be expanded
        """
        lines = self.code.splitlines()
        response = ""
        imports_count = 0
        line_number_width = len(str(self.tree.root_node.end_point[0]))
        last_line_added = 0
        entity_mapping: dict[str, tuple[int, int]] = {}  # entity -> (start_line, end_line)
        unused_entities: list[str] = [entity for entity in entities]

        def add_lines(code: str, start_line: int, end_line: int):
            nonlocal response, last_line_added
            if last_line_added + 1 < start_line:
                gap = start_line - last_line_added - 1
                if gap >= min_lines:
                    response += " " * line_number_width + " | "
                    response += get_indentation(lines[last_line_added + 1])
                    response += f"... ({gap} lines)\n"
                else:
                    for i in range(last_line_added + 1, start_line):
                        response += f"{i:{line_number_width}} | {lines[i-1]}\n"

            response += add_line_numbers(code, start_line, line_number_width) + "\n"
            last_line_added = end_line

        nodes: list[Node] = []
        for child in self.tree.root_node.children:
            entity_name = get_entity_name(child, language=self.language)
            if entity_name is None:
                nodes.append(child)
            elif child.type == "class_definition" and entity_name not in entities:
                # Handled class methods.
                nodes.append(child)
                nodes.extend(child.named_children[-1].children)
            elif child.type == "class_declaration" and entity_name not in entities:
                # Handles Java classes.
                nodes.append(child)
                nodes.extend(child.named_children[-1].children)
            elif (
                child.type == "decorated_definition"
                and child.named_children[-1].type == "class_definition"
                and entity_name not in entities
            ):
                # Handles decorated classes, like dataclass.
                nodes.append(child)
                nodes.extend(child.named_children[-1].named_children[-1].children)
            else:
                if entity_name_in_entities(entity_name, entities):
                    unused_entities = [unused for unused in unused_entities if unused not in entity_name]
                nodes.append(child)

        for child in nodes:
            if not child.is_named:
                continue
            is_import = False
            if child.type in self.import_types:
                imports_count += 1
                is_import = True

            start_line, _ = child.start_point
            end_line, _ = child.end_point
            start_line += 1
            end_line += 1

            entity_name = get_entity_name(child, language=self.language)

            if entity_name_in_entities(entity_name, entities):
                unused_entities = [unused for unused in unused_entities if entity_name not in unused]

            # entities to expand - always expand imports
            if (
                end_line - start_line <= min_lines
                or child.type in self.always_expand_statements
                or self.language in self.always_expand_files
                or entity_name_in_entities(entity_name, entities)
                or is_import
            ):
                indentation = get_indentation(lines[start_line - 1])
                add_lines(indentation + child.text.decode(), start_line, end_line)
            else:
                # add entity as unexpanded
                if entity_name:
                    entity_mapping[entity_name] = (start_line, end_line)
                # if no entities are mentioned default to collapsed behaviour otherwise we hide all other entities except the ones mentioned
                if entities:
                    continue
                header = child.text.decode().splitlines()[0]
                footer = child.text.decode().splitlines()[-1]
                if child.type in ("function_definition", "method_declaration"):
                    last_child = child.named_children[-1]
                    body_text = last_child.text
                    # the header should also include parts of the body as long as there is not new line character
                    newline_index = body_text.find(b"\n")
                    bytes_to_add = newline_index if newline_index != -1 else len(body_text)
                    header = self.encoded_code[child.start_byte : last_child.start_byte + bytes_to_add].decode()
                elif child.type == "decorated_definition":
                    header_start_char = child.children[0].start_byte
                    function_definition = next(
                        (child for child in child.children if child.type == "function_definition"),
                        child.children[-1],
                    )
                    header_end_char = function_definition.children[-2].end_byte
                    header = self.encoded_code[header_start_char:header_end_char].decode()

                # fix indentation
                header = get_indentation(lines[start_line - 1]) + header

                add_lines(
                    header.rstrip(),
                    start_line,
                    start_line + len(header.splitlines()) - 1,
                )
                # if not a type of class
                if child.type not in self.class_definition_types:
                    if "return" in footer:
                        add_lines(footer, end_line, end_line)
                    else:
                        add_lines("", end_line + 1, end_line + 1)

        # Add final "... (lines)" if there are remaining lines
        total_lines = len(lines)
        if last_line_added < total_lines:
            gap = total_lines - last_line_added
            response += " " * line_number_width + " | "
            response += get_indentation(lines[last_line_added])
            response += f"... ({gap} lines)\n"

        return response, entity_mapping, unused_entities

    def get_import_line_ranges(self):
        """
        Fetch where lines where imports are located
        """
        import_lines = []

        nodes = []
        for child in self.tree.root_node.children:
            if child.type == "class_definition":
                nodes.append(child)
                nodes.extend(child.named_children[-1].children)
            else:
                nodes.append(child)

        for child in nodes:
            if not child.is_named:
                continue
            is_import = False

            if child.type in self.import_types:
                is_import = True

            start_line, _ = child.start_point
            end_line, _ = child.end_point
            start_line += 1
            end_line += 1

            # entities to expand - always expand imports
            if is_import:
                import_lines.append((start_line, end_line))

        return import_lines


# The main section has been removed and moved to the test file.
