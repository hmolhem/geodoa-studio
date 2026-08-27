from __future__ import annotations

from dataclasses import dataclass

from geodoa.application.geometry_inspection import (
    GeometryInspectionResult,
    inspect_custom_geometry,
)
from geodoa.domain.ula import ULAGenerationSpec, generate_ula


@dataclass(frozen=True, slots=True)
class ULAInspectionResult:
    generation_spec: ULAGenerationSpec
    inspection: GeometryInspectionResult


def inspect_ula_geometry(
    spec: ULAGenerationSpec,
) -> ULAInspectionResult:
    geometry = generate_ula(spec)
    inspection = inspect_custom_geometry(geometry)

    return ULAInspectionResult(
        generation_spec=spec,
        inspection=inspection,
    )
