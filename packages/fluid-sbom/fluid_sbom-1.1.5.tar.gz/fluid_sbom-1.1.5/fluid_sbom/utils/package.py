from fluid_sbom.internal.package_information.javascript import (
    NPMPackageLicense,
)
from fluid_sbom.pkg.algorithm import (
    algorithm_length,
)
from fluid_sbom.pkg.package import (
    HealthMetadata,
)
import os
import re
from urllib.parse import (
    urlunparse,
)
import uuid


def strip_version_specifier(item: str) -> str:
    # Define the characters that indicate the start of a version specifier
    specifiers = "[(<>="

    # Find the index of the first occurrence of any specifier character
    index = next(
        (i for i, char in enumerate(item) if char in specifiers), None
    )

    # If no specifier character is found, return the original string
    if index is None:
        return item.strip()

    # Return the substring up to the first specifier character, stripped of
    # leading/trailing whitespace
    return item[:index].strip()


def handle_licenses(
    licenses: str | list[str | dict[str, str]] | NPMPackageLicense,
) -> list[str]:
    if isinstance(licenses, dict):
        return [licenses["type"]] if "type" in licenses else []
    if isinstance(licenses, list):
        licenses_list = []
        for license_item in licenses:
            if isinstance(license_item, str):
                licenses_list.append(license_item)
            if isinstance(license_item, dict) and license_item["type"]:
                licenses_list.append(license_item["type"])
        return licenses_list
    return [licenses]


def is_valid_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


def get_author_info(
    health_metadata: HealthMetadata,
) -> list[tuple[str | None, str | None]]:
    author_info = []

    if health_metadata.authors:
        authors_list = health_metadata.authors.split(", ")
        for author in authors_list:
            name: str | None = None
            email: str | None = None
            email_match = re.search(r"<([^<>]+)>", author)

            if email_match:
                email_candidate: str = email_match.group(1)
                if is_valid_email(email_candidate):
                    email = email_candidate
                else:
                    email = None
                name = author.replace(email_match.group(0), "").strip() or None
            else:
                name = author.strip() or None

            author_info.append((name, email))

    return author_info


def infer_algorithm(digest_value: str | None) -> str | None:
    if digest_value:
        for algorithm, length in algorithm_length.items():
            if len(digest_value) == int(length):
                return algorithm.value
    return None


def sanitize_name(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9.-]", "-", text)


def get_document_namespace(working_dir: str) -> str:
    input_type = "unknown-source-type"

    if os.path.isfile(working_dir):
        input_type = "file"
    elif os.path.isdir(working_dir):
        input_type = "dir"

    unique_id = uuid.uuid4()
    identifier = os.path.join(input_type, str(unique_id))
    if working_dir != ".":
        identifier = os.path.join(input_type, f"{working_dir}-{unique_id}")

    doc_namespace = urlunparse(
        ("https", "fluidattacks.com", identifier, "", "", ""),
    )

    return doc_namespace
