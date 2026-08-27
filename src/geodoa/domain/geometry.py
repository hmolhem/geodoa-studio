from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite


class GeometryValidationCode(StrEnum):
    EMPTY_GEOMETRY = "empty_geometry"
    NONFINITE_POSITION = "nonfinite_position"
    DUPLICATE_SENSOR_ID = "duplicate_sensor_id"
    DUPLICATE_POSITION = "duplicate_position"


class GeometryDiagnosticCode(StrEnum):
    ZERO_APERTURE = "zero_aperture"


class GeometryValidationError(ValueError):
    def __init__(self, code: GeometryValidationCode, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class SensorChannel1D:
    sensor_id: str
    position_m: float


@dataclass(frozen=True, slots=True)
class SortedGeometryView:
    channels: tuple[SensorChannel1D, ...]
    sorted_to_authoritative: tuple[int, ...]
    authoritative_to_sorted: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class LinearArrayGeometry:
    channels: tuple[SensorChannel1D, ...]

    def __post_init__(self) -> None:
        if not self.channels:
            raise GeometryValidationError(
                GeometryValidationCode.EMPTY_GEOMETRY,
                "A linear-array geometry must contain at least one channel.",
            )

        seen_sensor_ids: set[str] = set()
        seen_positions: set[float] = set()

        for channel in self.channels:
            if not isfinite(channel.position_m):
                raise GeometryValidationError(
                    GeometryValidationCode.NONFINITE_POSITION,
                    (
                        f"Channel {channel.sensor_id!r} has a nonfinite "
                        f"position: {channel.position_m!r}."
                    ),
                )

            if channel.sensor_id in seen_sensor_ids:
                raise GeometryValidationError(
                    GeometryValidationCode.DUPLICATE_SENSOR_ID,
                    f"Duplicate sensor identity: {channel.sensor_id!r}.",
                )

            if channel.position_m in seen_positions:
                raise GeometryValidationError(
                    GeometryValidationCode.DUPLICATE_POSITION,
                    (
                        "Duplicate physical position under the default "
                        f"scalar-channel policy: {channel.position_m!r} m."
                    ),
                )

            seen_sensor_ids.add(channel.sensor_id)
            seen_positions.add(channel.position_m)

    @property
    def sensor_count(self) -> int:
        return len(self.channels)

    def sorted_view(self) -> SortedGeometryView:
        indexed_channels = sorted(
            enumerate(self.channels),
            key=lambda item: item[1].position_m,
        )

        sorted_to_authoritative = tuple(
            authoritative_index for authoritative_index, _ in indexed_channels
        )

        authoritative_to_sorted_list = [0] * self.sensor_count

        for sorted_index, authoritative_index in enumerate(sorted_to_authoritative):
            authoritative_to_sorted_list[authoritative_index] = sorted_index

        return SortedGeometryView(
            channels=tuple(channel for _, channel in indexed_channels),
            sorted_to_authoritative=sorted_to_authoritative,
            authoritative_to_sorted=tuple(authoritative_to_sorted_list),
        )
