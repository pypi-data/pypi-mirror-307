from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection.toml import (
    parse_toml_with_tree_sitter,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.rust.package import (
    package_url,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.exceptions import (
    UnexpectedNode,
)
import logging
from pydantic import (
    ValidationError,
)
from typing import (
    ItemsView,
)

LOGGER = logging.getLogger(__name__)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        c_upd = {"line": sourceline}
        l_upd = {"coordinates": location.coordinates.model_copy(update=c_upd)}
        return location.model_copy(update=l_upd)
    return location


def _get_version(value: IndexedDict | str) -> str | None:
    if isinstance(value, str):
        return value
    if "git" in value:
        repo_url: str = value["git"]
        branch: str = value["branch"]
        return f"{repo_url}@{branch}"
    version: str | None = value.get("version")
    return version


def _get_packages(
    reader: LocationReadCloser,
    dependencies: IndexedDict | None,
) -> list[Package]:
    if dependencies is None:
        return []

    packages = []

    general_location = _get_location(
        reader.location, dependencies.position.start.line
    )
    items: ItemsView[str, IndexedDict | str] = dependencies.items()

    for name, value in items:
        version = _get_version(value)
        if not name or not version:
            continue

        location = (
            _get_location(reader.location, value.position.start.line)
            if isinstance(value, IndexedDict)
            else general_location
        )

        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    locations=[location],
                    language=Language.RUST,
                    licenses=[],
                    p_url=package_url(name=name, version=version),
                    type=PackageType.RustPkg,
                )
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types "
                "are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(  # type: ignore
                            include_url=False,
                        ),
                        "location": location.path(),
                    }
                },
            )
            continue

    return packages


def parse_cargo_toml(
    _: Resolver | None, __: Environment | None, reader: LocationReadCloser
) -> tuple[list[Package], list[Relationship]]:
    try:
        content = parse_toml_with_tree_sitter(reader.read_closer.read())
    except UnexpectedNode:
        return [], []

    deps: IndexedDict | None = content.get("dependencies")
    dev_deps: IndexedDict | None = content.get("dev-dependencies")
    packages = [
        *_get_packages(reader, deps),
        *_get_packages(reader, dev_deps),
    ]
    return packages, []
