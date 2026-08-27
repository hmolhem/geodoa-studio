import pytest

from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D
from geodoa.science.geometry_metrics import (
    compute_physical_geometry_metrics,
)


def test_metrics_match_unsorted_hand_calculated_oracle() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    metrics = compute_physical_geometry_metrics(geometry)

    assert metrics.sensor_count == 3
    assert metrics.centroid_m == pytest.approx(0.15)
    assert metrics.aperture_m == pytest.approx(0.30)
    assert metrics.adjacent_spacings_m == pytest.approx((0.15, 0.15))
    assert metrics.min_adjacent_spacing_m == pytest.approx(0.15)
    assert metrics.max_adjacent_spacing_m == pytest.approx(0.15)
    assert metrics.mean_adjacent_spacing_m == pytest.approx(0.15)


def test_single_channel_metrics_are_explicit() -> None:
    geometry = LinearArrayGeometry(channels=(SensorChannel1D("RX0", -0.25),))

    metrics = compute_physical_geometry_metrics(geometry)

    assert metrics.sensor_count == 1
    assert metrics.centroid_m == pytest.approx(-0.25)
    assert metrics.aperture_m == pytest.approx(0.0)
    assert metrics.adjacent_spacings_m == ()
    assert metrics.min_adjacent_spacing_m is None
    assert metrics.max_adjacent_spacing_m is None
    assert metrics.mean_adjacent_spacing_m is None


def test_uniform_translation_preserves_aperture_and_spacings() -> None:
    original = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    translation_m = 0.03

    translated = LinearArrayGeometry(
        channels=tuple(
            SensorChannel1D(
                channel.sensor_id,
                channel.position_m + translation_m,
            )
            for channel in original.channels
        )
    )

    original_metrics = compute_physical_geometry_metrics(original)
    translated_metrics = compute_physical_geometry_metrics(translated)

    assert translated_metrics.sensor_count == original_metrics.sensor_count
    assert translated_metrics.aperture_m == pytest.approx(original_metrics.aperture_m)
    assert translated_metrics.adjacent_spacings_m == pytest.approx(
        original_metrics.adjacent_spacings_m
    )
    assert translated_metrics.centroid_m == pytest.approx(
        original_metrics.centroid_m + translation_m
    )

    assert tuple(channel.sensor_id for channel in translated.channels) == tuple(
        channel.sensor_id for channel in original.channels
    )


def test_grp002_geometry_centroid_subset() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    metrics = compute_physical_geometry_metrics(geometry)

    assert metrics.centroid_m == pytest.approx(0.075)
    assert metrics.aperture_m == pytest.approx(0.15)
    assert metrics.adjacent_spacings_m == pytest.approx((0.15,))


def test_grp003_translation_geometry_subset() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", 0.03),
            SensorChannel1D("RX1", 0.18),
        )
    )

    metrics = compute_physical_geometry_metrics(geometry)

    assert metrics.centroid_m == pytest.approx(0.105)
    assert metrics.aperture_m == pytest.approx(0.15)
    assert metrics.adjacent_spacings_m == pytest.approx((0.15,))
