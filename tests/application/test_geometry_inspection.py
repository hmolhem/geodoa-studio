import pytest

from geodoa.application.geometry_inspection import (
    PhaseReferencePolicy,
    inspect_custom_geometry,
)
from geodoa.domain.geometry import (
    GeometryDiagnosticCode,
    LinearArrayGeometry,
    SensorChannel1D,
)


def test_inspection_matches_unsorted_hand_oracle() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    result = inspect_custom_geometry(geometry)

    assert result.geometry is geometry

    assert tuple(channel.sensor_id for channel in result.geometry.channels) == (
        "RX2",
        "RX0",
        "RX1",
    )

    assert tuple(channel.sensor_id for channel in result.sorted_view.channels) == (
        "RX0",
        "RX1",
        "RX2",
    )

    assert result.sorted_view.sorted_to_authoritative == (1, 2, 0)
    assert result.sorted_view.authoritative_to_sorted == (2, 0, 1)

    assert result.metrics.sensor_count == 3
    assert result.metrics.centroid_m == pytest.approx(0.15)
    assert result.metrics.aperture_m == pytest.approx(0.30)
    assert result.metrics.adjacent_spacings_m == pytest.approx((0.15, 0.15))

    assert (
        result.default_phase_reference.policy
        is PhaseReferencePolicy.DECLARED_GEOMETRY_CENTROID
    )
    assert result.default_phase_reference.position_m == pytest.approx(0.15)

    assert result.diagnostics == ()


def test_single_channel_reports_zero_aperture_diagnostic() -> None:
    geometry = LinearArrayGeometry(channels=(SensorChannel1D("RX0", -0.25),))

    result = inspect_custom_geometry(geometry)

    assert result.metrics.sensor_count == 1
    assert result.metrics.aperture_m == pytest.approx(0.0)

    assert result.diagnostics == (GeometryDiagnosticCode.ZERO_APERTURE,)

    assert result.default_phase_reference.position_m == pytest.approx(-0.25)


def test_translation_moves_centroid_phase_reference() -> None:
    original = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    translated = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", 0.03),
            SensorChannel1D("RX1", 0.18),
        )
    )

    original_result = inspect_custom_geometry(original)
    translated_result = inspect_custom_geometry(translated)

    assert original_result.default_phase_reference.position_m == (pytest.approx(0.075))

    assert translated_result.default_phase_reference.position_m == (
        pytest.approx(0.105)
    )

    assert translated_result.metrics.aperture_m == pytest.approx(
        original_result.metrics.aperture_m
    )


def test_default_phase_reference_does_not_follow_sorted_first_channel() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    result = inspect_custom_geometry(geometry)

    assert result.sorted_view.channels[0].position_m == pytest.approx(0.00)
    assert result.default_phase_reference.position_m == pytest.approx(0.15)
