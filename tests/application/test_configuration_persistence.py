from pathlib import Path

from geodoa.application.configuration_persistence import (
    inspect_geometry_configuration,
    load_and_inspect_geometry_configuration,
    load_geometry_configuration,
    save_geometry_configuration,
)
from geodoa.domain.configuration import (
    CustomGeometryConstruction,
    GeometryConfigurationV1,
    ULAGeometryConstruction,
)
from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D
from geodoa.domain.ula import (
    ULAGenerationSpec,
    ULAPlacementPolicy,
    generate_ula,
)
from geodoa.serialization.geometry_configuration_json import (
    encode_geometry_configuration_json,
)


def test_save_and_load_custom_configuration_round_trip(tmp_path: Path) -> None:
    configuration = GeometryConfigurationV1(
        geometry=LinearArrayGeometry(
            channels=(
                SensorChannel1D("RX2", 0.30),
                SensorChannel1D("RX0", 0.00),
                SensorChannel1D("RX1", 0.15),
            )
        ),
        construction=CustomGeometryConstruction(),
    )

    path = tmp_path / "custom_geometry.json"

    save_geometry_configuration(path, configuration)
    loaded = load_geometry_configuration(path)

    assert loaded == configuration


def test_save_writes_exact_canonical_utf8_bytes(tmp_path: Path) -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.CENTROID,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    path = tmp_path / "ula_geometry.json"

    save_geometry_configuration(path, configuration)

    expected = encode_geometry_configuration_json(configuration).encode("utf-8")

    assert path.read_bytes() == expected


def test_load_preserves_ula_construction_provenance(tmp_path: Path) -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=-0.5,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    path = tmp_path / "ula_geometry.json"

    save_geometry_configuration(path, configuration)
    loaded = load_geometry_configuration(path)

    assert loaded == configuration


def test_inspection_reuses_existing_geometry_semantics() -> None:
    configuration = GeometryConfigurationV1(
        geometry=LinearArrayGeometry(
            channels=(
                SensorChannel1D("A", -0.5),
                SensorChannel1D("B", 0.0),
                SensorChannel1D("C", 0.5),
            )
        ),
        construction=CustomGeometryConstruction(),
    )

    result = inspect_geometry_configuration(configuration)

    assert result.configuration is configuration
    assert result.inspection.geometry is configuration.geometry
    assert result.inspection.metrics.sensor_count == 3
    assert result.inspection.metrics.centroid_m == 0.0
    assert result.inspection.metrics.aperture_m == 1.0
    assert result.inspection.default_phase_reference.position_m == 0.0


def test_load_and_inspect_round_trip(tmp_path: Path) -> None:
    spec = ULAGenerationSpec(
        sensor_count=4,
        spacing_m=0.25,
        anchor_m=-0.5,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    path = tmp_path / "ula_geometry.json"

    save_geometry_configuration(path, configuration)
    result = load_and_inspect_geometry_configuration(path)

    assert result.configuration == configuration
    assert result.inspection.metrics.sensor_count == 4
    assert result.inspection.metrics.centroid_m == -0.125
    assert result.inspection.metrics.aperture_m == 0.75
    assert result.inspection.default_phase_reference.position_m == -0.125
