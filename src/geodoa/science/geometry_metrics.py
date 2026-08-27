from __future__ import annotations

from dataclasses import dataclass

from geodoa.domain.geometry import LinearArrayGeometry


@dataclass(frozen=True, slots=True)
class PhysicalGeometryMetrics:
    sensor_count: int
    centroid_m: float
    aperture_m: float
    adjacent_spacings_m: tuple[float, ...]
    min_adjacent_spacing_m: float | None
    max_adjacent_spacing_m: float | None
    mean_adjacent_spacing_m: float | None


def compute_physical_geometry_metrics(
    geometry: LinearArrayGeometry,
) -> PhysicalGeometryMetrics:
    positions_m = tuple(channel.position_m for channel in geometry.channels)
    sensor_count = geometry.sensor_count

    centroid_m = sum(positions_m) / sensor_count

    sorted_positions_m = tuple(
        channel.position_m for channel in geometry.sorted_view().channels
    )

    aperture_m = sorted_positions_m[-1] - sorted_positions_m[0]

    adjacent_spacings_m = tuple(
        right - left
        for left, right in zip(
            sorted_positions_m,
            sorted_positions_m[1:],
            strict=False,
        )
    )

    if not adjacent_spacings_m:
        min_adjacent_spacing_m = None
        max_adjacent_spacing_m = None
        mean_adjacent_spacing_m = None
    else:
        min_adjacent_spacing_m = min(adjacent_spacings_m)
        max_adjacent_spacing_m = max(adjacent_spacings_m)
        mean_adjacent_spacing_m = sum(adjacent_spacings_m) / len(adjacent_spacings_m)

    return PhysicalGeometryMetrics(
        sensor_count=sensor_count,
        centroid_m=centroid_m,
        aperture_m=aperture_m,
        adjacent_spacings_m=adjacent_spacings_m,
        min_adjacent_spacing_m=min_adjacent_spacing_m,
        max_adjacent_spacing_m=max_adjacent_spacing_m,
        mean_adjacent_spacing_m=mean_adjacent_spacing_m,
    )
