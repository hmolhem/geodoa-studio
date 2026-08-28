from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite

from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D


class ULAGenerationCode(StrEnum):
    INVALID_SENSOR_COUNT = "invalid_sensor_count"
    NONFINITE_SPACING = "nonfinite_spacing"
    NONPOSITIVE_SPACING = "nonpositive_spacing"
    NONFINITE_ANCHOR = "nonfinite_anchor"
    INVALID_PLACEMENT_POLICY = "invalid_placement_policy"


class ULAGenerationError(ValueError):
    def __init__(self, code: ULAGenerationCode, message: str) -> None:
        super().__init__(message)
        self.code = code


class ULAPlacementPolicy(StrEnum):
    FIRST_SENSOR = "first_sensor"
    CENTROID = "centroid"


@dataclass(frozen=True, slots=True)
class ULAGenerationSpec:
    sensor_count: int
    spacing_m: float
    anchor_m: float
    placement_policy: ULAPlacementPolicy

    def __post_init__(self) -> None:
        if (
            isinstance(self.sensor_count, bool)
            or not isinstance(self.sensor_count, int)
            or self.sensor_count < 1
        ):
            raise ULAGenerationError(
                ULAGenerationCode.INVALID_SENSOR_COUNT,
                "ULA sensor_count must be an integer greater than or equal to one.",
            )

        if not isfinite(self.spacing_m):
            raise ULAGenerationError(
                ULAGenerationCode.NONFINITE_SPACING,
                f"ULA spacing must be finite: {self.spacing_m!r}.",
            )

        if self.spacing_m <= 0.0:
            raise ULAGenerationError(
                ULAGenerationCode.NONPOSITIVE_SPACING,
                f"ULA spacing must be strictly positive: {self.spacing_m!r} m.",
            )

        if not isfinite(self.anchor_m):
            raise ULAGenerationError(
                ULAGenerationCode.NONFINITE_ANCHOR,
                f"ULA construction anchor must be finite: {self.anchor_m!r} m.",
            )

        if not isinstance(self.placement_policy, ULAPlacementPolicy):
            raise ULAGenerationError(
                ULAGenerationCode.INVALID_PLACEMENT_POLICY,
                f"Unsupported ULA placement policy: {self.placement_policy!r}.",
            )


def generate_ula(spec: ULAGenerationSpec) -> LinearArrayGeometry:
    if spec.placement_policy is ULAPlacementPolicy.FIRST_SENSOR:
        first_position_m = spec.anchor_m
    elif spec.placement_policy is ULAPlacementPolicy.CENTROID:
        first_position_m = (
            spec.anchor_m - 0.5 * (spec.sensor_count - 1) * spec.spacing_m
        )
    else:  # pragma: no cover - ULAGenerationSpec validates this invariant.
        raise AssertionError("Unreachable ULA placement policy.")

    channels = tuple(
        SensorChannel1D(
            sensor_id=f"RX{index}",
            position_m=first_position_m + index * spec.spacing_m,
        )
        for index in range(spec.sensor_count)
    )

    return LinearArrayGeometry(channels=channels)
