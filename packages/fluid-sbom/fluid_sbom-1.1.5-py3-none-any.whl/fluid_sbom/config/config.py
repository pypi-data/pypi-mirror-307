from enum import (
    Enum,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from pydantic import (
    BaseModel,
    ConfigDict,
)
from typing import (
    Type,
)


class SbomOutputFormat(str, Enum):
    FLUID_JSON: str = "fluid-json"
    CYCLONEDX_JSON: str = "cyclonedx-json"
    CYCLONEDX_XML: str = "cyclonedx-xml"
    SPDX_JSON: str = "spdx-json"
    SPDX_XML: str = "spdx-xml"


class SourceType(Enum):
    DIRECTORY = "dir"
    DOCKER = "docker"
    DOCKER_DAEMON = "docker-daemon"

    @classmethod
    def from_string(cls: Type["SourceType"], value: str) -> "SourceType":
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")


class SbomConfig(BaseModel):
    source: str
    source_type: SourceType
    output_format: str
    output: str
    resolver: Resolver | None = None
    exclude: tuple[str, ...]
    docker_user: str | None = None
    docker_password: str | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
