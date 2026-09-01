from typing import cast

import pytest

from geodoa.domain.configuration import (
    CURRENT_ULA_GENERATOR_VERSION,
    CustomGeometryConstruction,
    GeometryConfigurationCode,
    GeometryConfigurationError,
    GeometryConfigurationV1,
    ULAGeometryConstruction,
)
from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D
from geodoa.domain.ula import (
    ULAGenerationSpec,
    ULAPlacementPolicy,
    generate_ula,
)


def test_custom_configuration_preserves_authoritative_geometry() -> None:
    geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX2", 0.30),
            SensorChannel1D("RX0", 0.00),
            SensorChannel1D("RX1", 0.15),
        )
    )

    construction = CustomGeometryConstruction()

    configuration = GeometryConfigurationV1(
        geometry=geometry,
        construction=construction,
    )

    assert configuration.geometry is geometry
    assert configuration.construction is construction
    assert tuple(channel.sensor_id for channel in configuration.geometry.channels) == (
        "RX2",
        "RX0",
        "RX1",
    )


def test_ula_configuration_accepts_matching_centroid_geometry() -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.CENTROID,
    )

    geometry = generate_ula(spec)

    configuration = GeometryConfigurationV1(
        geometry=geometry,
        construction=ULAGeometryConstruction(spec=spec),
    )

    assert configuration.geometry == geometry
    construction = configuration.construction
    assert isinstance(construction, ULAGeometryConstruction)
    assert construction.spec is spec
    assert construction.generator_version == CURRENT_ULA_GENERATOR_VERSION


def test_ula_configuration_accepts_matching_first_sensor_geometry() -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=-0.50,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    assert tuple(
        channel.position_m for channel in configuration.geometry.channels
    ) == pytest.approx((-0.50, -0.25, 0.00, 0.25))


def test_ula_configuration_rejects_geometry_mismatch() -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.CENTROID,
    )

    mismatched_geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("RX0", -0.375),
            SensorChannel1D("RX1", -0.125),
            SensorChannel1D("RX2", 0.125),
            SensorChannel1D("RX3", 0.40),
        )
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        GeometryConfigurationV1(
            geometry=mismatched_geometry,
            construction=ULAGeometryConstruction(spec=spec),
        )

    assert (
        exc_info.value.code is GeometryConfigurationCode.CONSTRUCTION_GEOMETRY_MISMATCH
    )


def test_ula_configuration_rejects_sensor_identity_mismatch() -> None:
    spec = ULAGenerationSpec(
        sensor_count=2,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    mismatched_geometry = LinearArrayGeometry(
        channels=(
            SensorChannel1D("A", 0.0),
            SensorChannel1D("B", 0.25),
        )
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        GeometryConfigurationV1(
            geometry=mismatched_geometry,
            construction=ULAGeometryConstruction(spec=spec),
        )

    assert (
        exc_info.value.code is GeometryConfigurationCode.CONSTRUCTION_GEOMETRY_MISMATCH
    )


def test_ula_configuration_rejects_authoritative_order_mismatch() -> None:
    spec = ULAGenerationSpec(
        sensor_count=3,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    generated = generate_ula(spec)

    reordered_geometry = LinearArrayGeometry(
        channels=(
            generated.channels[1],
            generated.channels[0],
            generated.channels[2],
        )
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        GeometryConfigurationV1(
            geometry=reordered_geometry,
            construction=ULAGeometryConstruction(spec=spec),
        )

    assert (
        exc_info.value.code is GeometryConfigurationCode.CONSTRUCTION_GEOMETRY_MISMATCH
    )


@pytest.mark.parametrize(
    "generator_version",
    [
        0,
        2,
        True,
        1.0,
    ],
)
def test_ula_configuration_rejects_unsupported_generator_version(
    generator_version: object,
) -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.CENTROID,
    )

    construction = ULAGeometryConstruction(
        spec=spec,
        generator_version=cast(int, generator_version),
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        GeometryConfigurationV1(
            geometry=generate_ula(spec),
            construction=construction,
        )

    assert (
        exc_info.value.code
        is GeometryConfigurationCode.UNSUPPORTED_ULA_GENERATOR_VERSION
    )


def test_configuration_rejects_unknown_construction_runtime_value() -> None:
    geometry = LinearArrayGeometry(channels=(SensorChannel1D("RX0", 0.0),))

    invalid_construction = cast(
        CustomGeometryConstruction | ULAGeometryConstruction,
        object(),
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        GeometryConfigurationV1(
            geometry=geometry,
            construction=invalid_construction,
        )

    assert exc_info.value.code is GeometryConfigurationCode.INVALID_CONSTRUCTION
