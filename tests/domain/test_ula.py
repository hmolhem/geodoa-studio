import math
from typing import cast

import pytest

from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D
from geodoa.domain.ula import (
    ULAGenerationCode,
    ULAGenerationError,
    ULAGenerationSpec,
    ULAPlacementPolicy,
    generate_ula,
)


def test_centered_ula_matches_hand_oracle() -> None:
    geometry = generate_ula(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )
    )

    assert tuple(channel.sensor_id for channel in geometry.channels) == (
        "RX0",
        "RX1",
        "RX2",
        "RX3",
    )
    assert tuple(channel.position_m for channel in geometry.channels) == (
        -0.375,
        -0.125,
        0.125,
        0.375,
    )


def test_first_sensor_ula_matches_hand_oracle() -> None:
    geometry = generate_ula(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=-0.50,
            placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
        )
    )

    assert tuple(channel.position_m for channel in geometry.channels) == (
        -0.50,
        -0.25,
        0.00,
        0.25,
    )


def test_ula_sensor_ids_are_deterministic() -> None:
    geometry = generate_ula(
        ULAGenerationSpec(
            sensor_count=3,
            spacing_m=0.20,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
        )
    )

    assert tuple(channel.sensor_id for channel in geometry.channels) == (
        "RX0",
        "RX1",
        "RX2",
    )


def test_ula_authoritative_order_is_already_geometrically_sorted() -> None:
    geometry = generate_ula(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )
    )

    sorted_view = geometry.sorted_view()

    assert sorted_view.sorted_to_authoritative == (0, 1, 2, 3)
    assert sorted_view.authoritative_to_sorted == (0, 1, 2, 3)


def test_generated_ula_matches_equivalent_custom_geometry() -> None:
    generated = generate_ula(
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )
    )

    custom = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", -0.375),
            SensorChannel1D("RX1", -0.125),
            SensorChannel1D("RX2", 0.125),
            SensorChannel1D("RX3", 0.375),
        )
    )

    assert generated == custom


@pytest.mark.parametrize(
    "placement_policy",
    [
        ULAPlacementPolicy.FIRST_SENSOR,
        ULAPlacementPolicy.CENTROID,
    ],
)
def test_single_sensor_ula_is_valid(
    placement_policy: ULAPlacementPolicy,
) -> None:
    geometry = generate_ula(
        ULAGenerationSpec(
            sensor_count=1,
            spacing_m=0.25,
            anchor_m=-0.40,
            placement_policy=placement_policy,
        )
    )

    assert geometry.channels == (SensorChannel1D("RX0", -0.40),)


@pytest.mark.parametrize("sensor_count", [0, -1])
def test_invalid_sensor_count_is_rejected(sensor_count: int) -> None:
    with pytest.raises(ULAGenerationError) as exc_info:
        ULAGenerationSpec(
            sensor_count=sensor_count,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )

    assert exc_info.value.code is ULAGenerationCode.INVALID_SENSOR_COUNT


@pytest.mark.parametrize(
    "spacing_m",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_nonfinite_spacing_is_rejected(spacing_m: float) -> None:
    with pytest.raises(ULAGenerationError) as exc_info:
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=spacing_m,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )

    assert exc_info.value.code is ULAGenerationCode.NONFINITE_SPACING


@pytest.mark.parametrize("spacing_m", [0.0, -0.25])
def test_nonpositive_spacing_is_rejected(spacing_m: float) -> None:
    with pytest.raises(ULAGenerationError) as exc_info:
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=spacing_m,
            anchor_m=0.0,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )

    assert exc_info.value.code is ULAGenerationCode.NONPOSITIVE_SPACING


@pytest.mark.parametrize(
    "anchor_m",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_nonfinite_anchor_is_rejected(anchor_m: float) -> None:
    with pytest.raises(ULAGenerationError) as exc_info:
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=anchor_m,
            placement_policy=ULAPlacementPolicy.CENTROID,
        )

    assert exc_info.value.code is ULAGenerationCode.NONFINITE_ANCHOR


def test_invalid_placement_policy_is_rejected() -> None:
    invalid_policy = cast(ULAPlacementPolicy, "unsupported")

    with pytest.raises(ULAGenerationError) as exc_info:
        ULAGenerationSpec(
            sensor_count=4,
            spacing_m=0.25,
            anchor_m=0.0,
            placement_policy=invalid_policy,
        )

    assert exc_info.value.code is ULAGenerationCode.INVALID_PLACEMENT_POLICY
