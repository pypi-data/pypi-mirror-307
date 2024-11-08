from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.file_resolver.directory import (
    Directory,
)
import logging
import os
from pydantic import (
    BaseModel,
)

LOGGER = logging.getLogger(__name__)


class DirectoryConfig(BaseModel):
    path: str
    exclude: tuple[str, ...]


class DirectorySource(BaseModel):
    config: DirectoryConfig
    resolver: Directory | None = None

    def file_resolver(self) -> Resolver:
        if self.resolver is None:
            self.resolver = Directory(
                root=self.config.path, exclude=self.config.exclude
            )
        return self.resolver


def new_from_directory_path(
    path: str, exclude: tuple[str, ...]
) -> DirectorySource | None:
    return new_from_directory(DirectoryConfig(path=path, exclude=exclude))


def new_from_directory(cfg: DirectoryConfig) -> DirectorySource | None:
    if not os.path.isdir(cfg.path):
        LOGGER.error("Given path is not a directory: %s", cfg.path)
        return None

    return DirectorySource(config=cfg, resolver=None)
