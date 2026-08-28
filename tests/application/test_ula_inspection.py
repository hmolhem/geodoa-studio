import pytest

from geodoa.application.geometry_inspection import PhaseReferencePolicy
from geodoa.application.ula_inspection import inspect_ula_geometry
from geodoa.domain.geometry import GeometryDiagnosticCode
from geodoa.domain.ula import ULAGenerationSpec, ULAPlacementPolicy


def test_centered_ula_inspection_matches_hand_oracle() -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.CENTROID,
    )

    result = inspect_ula_geometry(spec)

    assert result.generation_spec is spec

    assert tuple(
        channel.position_m for channel in result.inspection.geometry.channels
    ) == pytest.approx((-0.375, -0.125, 0.125, 0.375))

    assert result.inspection.metrics.sensor_count == 4
    assert result.inspection.metrics.centroid_m == pytest.approx(0.0)
    assert result.inspection.metrics.aperture_m == pytest.approx(0.75)

    assert result.inspection.metrics.adjacent_spacings_m == pytest.approx(
        (0.25, 0.25, 0.25)
    )
    assert result.inspection.metrics.min_adjacent_spacing_m == pytest.approx(0.25)
    assert result.inspection.metrics.max_adjacent_spacing_m == pytest.approx(0.25)
    assert result.inspection.metrics.mean_adjacent_spacing_m == pytest.approx(0.25)

    assert (
        result.inspection.default_phase_reference.policy
        is PhaseReferencePolicy.DECLARED_GEOMETRY_CENTROID
    )
    assert result.inspection.default_phase_reference.position_m == pytest.approx(0.0)

    assert result.inspection.diagnostics == ()


def test_first_sensor_ula_inspection_matches_hand_oracle() -> None:
    result = inspect_ula_geometry(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=-0.50,
            placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
        )
    )

    assert tuple(
        channel.position_m for channel in result.inspection.geometry.channels
    ) == pytest.approx((-0.50, -0.25, 0.00, 0.25))

    assert result.inspection.metrics.centroid_m == pytest.approx(-0.125)
    assert result.inspection.metrics.aperture_m == pytest.approx(0.75)

    assert result.inspection.default_phase_reference.position_m == pytest.approx(-0.125)


def test_ula_inspection_preserves_identity_sorted_permutations() -> None:
    result = inspect_ula_geometry(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )
    )

    assert result.inspection.sorted_view.sorted_to_authoritative == (
        0,
        1,
        2,
        3,
    )
    assert result.inspection.sorted_view.authoritative_to_sorted == (
        0,
        1,
        2,
        3,
    )


@pytest.mark.parametrize(
    "placement_policy",
    [
        ULAPlacementPolicy.FIRST_SENSOR,
        ULAPlacementPolicy.CENTROID,
    ],
)
def test_single_sensor_ula_inspection_reports_zero_aperture(
    placement_policy: ULAPlacementPolicy,
) -> None:
    result = inspect_ula_geometry(
        ULAGenerationSpec(
            sensor_count=1,
            spacing_m=0.25,
            anchor_m=-0.40,
            placement_policy=placement_policy,
        )
    )

    assert result.inspection.metrics.sensor_count == 1
    assert result.inspection.metrics.centroid_m == pytest.approx(-0.40)
    assert result.inspection.metrics.aperture_m == pytest.approx(0.0)
    assert result.inspection.metrics.adjacent_spacings_m == ()

    assert result.inspection.diagnostics == (GeometryDiagnosticCode.ZERO_APERTURE,)

    assert result.inspection.default_phase_reference.position_m == pytest.approx(-0.40)
