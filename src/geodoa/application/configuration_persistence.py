from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from geodoa.application.geometry_inspection import (
    GeometryInspectionResult,
    inspect_custom_geometry,
)
from geodoa.domain.configuration import GeometryConfigurationV1
from geodoa.serialization.geometry_configuration_json import (
    decode_geometry_configuration_json,
    encode_geometry_configuration_json,
)


@dataclass(frozen=True, slots=True)
class GeometryConfigurationInspectionResult:
    configuration: GeometryConfigurationV1
    inspection: GeometryInspectionResult


def save_geometry_configuration(
    path: str | Path,
    configuration: GeometryConfigurationV1,
) -> None:
    target = Path(path)
    encoded = encode_geometry_configuration_json(configuration)
    target.write_bytes(encoded.encode("utf-8"))


def load_geometry_configuration(
    path: str | Path,
) -> GeometryConfigurationV1:
    source = Path(path)
    text = source.read_bytes().decode("utf-8")
    return decode_geometry_configuration_json(text)


def inspect_geometry_configuration(
    configuration: GeometryConfigurationV1,
) -> GeometryConfigurationInspectionResult:
    inspection = inspect_custom_geometry(configuration.geometry)

    return GeometryConfigurationInspectionResult(
        configuration=configuration,
        inspection=inspection,
    )


def load_and_inspect_geometry_configuration(
    path: str | Path,
) -> GeometryConfigurationInspectionResult:
    configuration = load_geometry_configuration(path)
    return inspect_geometry_configuration(configuration)
