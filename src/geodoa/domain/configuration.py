from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from geodoa.domain.geometry import LinearArrayGeometry
from geodoa.domain.ula import ULAGenerationSpec, generate_ula

CURRENT_ULA_GENERATOR_VERSION = 1


class GeometryConfigurationCode(StrEnum):
    INVALID_CONSTRUCTION = "invalid_construction"
    UNSUPPORTED_ULA_GENERATOR_VERSION = "unsupported_ula_generator_version"
    CONSTRUCTION_GEOMETRY_MISMATCH = "construction_geometry_mismatch"


class GeometryConfigurationError(ValueError):
    def __init__(
        self,
        code: GeometryConfigurationCode,
        message: str,
    ) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class CustomGeometryConstruction:
    pass


@dataclass(frozen=True, slots=True)
class ULAGeometryConstruction:
    spec: ULAGenerationSpec
    generator_version: int = CURRENT_ULA_GENERATOR_VERSION


GeometryConstruction = CustomGeometryConstruction | ULAGeometryConstruction


@dataclass(frozen=True, slots=True)
class GeometryConfigurationV1:
    geometry: LinearArrayGeometry
    construction: GeometryConstruction

    def __post_init__(self) -> None:
        if isinstance(self.construction, CustomGeometryConstruction):
            return

        if isinstance(self.construction, ULAGeometryConstruction):
            generator_version = self.construction.generator_version
            if (
                isinstance(generator_version, bool)
                or not isinstance(generator_version, int)
                or generator_version != CURRENT_ULA_GENERATOR_VERSION
            ):
                raise GeometryConfigurationError(
                    GeometryConfigurationCode.UNSUPPORTED_ULA_GENERATOR_VERSION,
                    (
                        "Unsupported ULA generator version: "
                        f"{self.construction.generator_version!r}. "
                        "The current configuration contract supports version "
                        f"{CURRENT_ULA_GENERATOR_VERSION}."
                    ),
                )

            generated_geometry = generate_ula(self.construction.spec)

            if generated_geometry != self.geometry:
                raise GeometryConfigurationError(
                    GeometryConfigurationCode.CONSTRUCTION_GEOMETRY_MISMATCH,
                    (
                        "ULA construction provenance does not reproduce the "
                        "authoritative physical geometry exactly."
                    ),
                )

            return

        raise GeometryConfigurationError(
            GeometryConfigurationCode.INVALID_CONSTRUCTION,
            ("Geometry configuration construction must be custom or ULA provenance."),
        )
