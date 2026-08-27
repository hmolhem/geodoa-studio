from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from geodoa.domain.geometry import (
    GeometryDiagnosticCode,
    LinearArrayGeometry,
    SortedGeometryView,
)
from geodoa.science.geometry_metrics import (
    PhysicalGeometryMetrics,
    compute_physical_geometry_metrics,
)


class PhaseReferencePolicy(StrEnum):
    DECLARED_GEOMETRY_CENTROID = "declared_geometry_centroid"


@dataclass(frozen=True, slots=True)
class DefaultPhaseReference1D:
    policy: PhaseReferencePolicy
    position_m: float


@dataclass(frozen=True, slots=True)
class GeometryInspectionResult:
    geometry: LinearArrayGeometry
    sorted_view: SortedGeometryView
    metrics: PhysicalGeometryMetrics
    default_phase_reference: DefaultPhaseReference1D
    diagnostics: tuple[GeometryDiagnosticCode, ...]


def inspect_custom_geometry(
    geometry: LinearArrayGeometry,
) -> GeometryInspectionResult:
    metrics = compute_physical_geometry_metrics(geometry)

    diagnostics: tuple[GeometryDiagnosticCode, ...]
    if metrics.aperture_m == 0.0:
        diagnostics = (GeometryDiagnosticCode.ZERO_APERTURE,)
    else:
        diagnostics = ()

    default_phase_reference = DefaultPhaseReference1D(
        policy=PhaseReferencePolicy.DECLARED_GEOMETRY_CENTROID,
        position_m=metrics.centroid_m,
    )

    return GeometryInspectionResult(
        geometry=geometry,
        sorted_view=geometry.sorted_view(),
        metrics=metrics,
        default_phase_reference=default_phase_reference,
        diagnostics=diagnostics,
    )
