import json
import os
from dataclasses import dataclass, field


@dataclass
class DockerfileConfig:
    command: str  # this is can be defaulted likewise
    dockerfile_path: str = "Dockerfile"
    working_dir: str = ""
    image_name: str = ""
    container_name: str = ""
    match_files: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.image_name:
            self.image_name = (
                os.path.basename(self.dockerfile_path).removeprefix("Dockerfile").removeprefix(".").removeprefix("_")
            )
            self.image_name = self.image_name or "main"
        if not self.container_name:
            self.container_name = self.image_name


def load_dockerfile_configs_from_path(location) -> list[DockerfileConfig]:
    # load an instance of this from a json file
    with open(location, "r") as f:
        data = json.load(f)
    return [DockerfileConfig(**item) for item in data]
