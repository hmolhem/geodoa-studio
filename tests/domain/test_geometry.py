import math

import pytest

from geodoa.domain.geometry import (
    GeometryValidationCode,
    GeometryValidationError,
    LinearArrayGeometry,
    SensorChannel1D,
)


def test_custom_geometry_preserves_authoritative_order() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    assert geometry.sensor_count == 3
    assert tuple(channel.sensor_id for channel in geometry.channels) == (
        "RX2",
        "RX0",
        "RX1",
    )
    assert tuple(channel.position_m for channel in geometry.channels) == (
        0.30,
        0.00,
        0.15,
    )


def test_sorted_view_preserves_channel_identity_and_permutation() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    sorted_view = geometry.sorted_view()

    assert tuple(channel.sensor_id for channel in sorted_view.channels) == (
        "RX0",
        "RX1",
        "RX2",
    )
    assert tuple(channel.position_m for channel in sorted_view.channels) == (
        0.00,
        0.15,
        0.30,
    )
    assert sorted_view.sorted_to_authoritative == (1, 2, 0)
    assert sorted_view.authoritative_to_sorted == (2, 0, 1)

    assert tuple(channel.sensor_id for channel in geometry.channels) == (
        "RX2",
        "RX0",
        "RX1",
    )


def test_single_channel_geometry_is_valid() -> None:
    geometry = LinearArrayGeometry(channels=(SensorChannel1D("RX0", -0.25),))

    assert geometry.sensor_count == 1
    assert geometry.sorted_view().sorted_to_authoritative == (0,)


def test_empty_geometry_is_rejected() -> None:
    with pytest.raises(GeometryValidationError) as exc_info:
        LinearArrayGeometry(channels=())

    assert exc_info.value.code is GeometryValidationCode.EMPTY_GEOMETRY


@pytest.mark.parametrize(
    "position_m",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_nonfinite_position_is_rejected(position_m: float) -> None:
    with pytest.raises(GeometryValidationError) as exc_info:
        LinearArrayGeometry(channels=(SensorChannel1D("RX0", position_m),))

    assert exc_info.value.code is GeometryValidationCode.NONFINITE_POSITION


def test_duplicate_sensor_identity_is_rejected() -> None:
    with pytest.raises(GeometryValidationError) as exc_info:
        LinearArrayGeometry(
            channels=(
                SensorChannel1D("RX0", 0.00),
                SensorChannel1D("RX0", 0.15),
            )
        )

    assert exc_info.value.code is GeometryValidationCode.DUPLICATE_SENSOR_ID


def test_duplicate_physical_position_is_rejected() -> None:
    with pytest.raises(GeometryValidationError) as exc_info:
        LinearArrayGeometry(
            channels=(
                SensorChannel1D("RX0", 0.00),
                SensorChannel1D("RX1", 0.00),
            )
        )

    assert exc_info.value.code is GeometryValidationCode.DUPLICATE_POSITION
