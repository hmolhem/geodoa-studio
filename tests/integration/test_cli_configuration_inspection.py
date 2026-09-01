import json
import subprocess
import sys
from pathlib import Path

import pytest

from geodoa.application.configuration_persistence import (
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


def _run_inspect_config(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-config",
            "--input",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_inspects_saved_ula_configuration(tmp_path: Path) -> None:
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

    path = tmp_path / "ula.json"
    save_geometry_configuration(path, configuration)

    completed = _run_inspect_config(path)

    assert completed.returncode == 0
    assert completed.stderr == ""

    payload = json.loads(completed.stdout)

    assert payload["geometry_kind"] == "ula"
    assert payload["sensor_count"] == 4
    assert payload["generation"] == {
        "sensor_count": 4,
        "spacing_m": 0.25,
        "anchor_m": -0.5,
        "placement_policy": "first_sensor",
        "generator_version": 1,
    }

    assert [
        channel["position_m"] for channel in payload["authoritative_channels"]
    ] == pytest.approx([-0.5, -0.25, 0.0, 0.25])

    assert payload["metrics"]["centroid_m"] == pytest.approx(-0.125)
    assert payload["metrics"]["aperture_m"] == pytest.approx(0.75)
    assert payload["default_phase_reference"]["position_m"] == pytest.approx(-0.125)


def test_cli_inspects_saved_custom_configuration_without_reordering(
    tmp_path: Path,
) -> None:
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

    path = tmp_path / "custom.json"
    save_geometry_configuration(path, configuration)

    completed = _run_inspect_config(path)

    assert completed.returncode == 0

    payload = json.loads(completed.stdout)

    assert payload["geometry_kind"] == "custom_linear_1d"

    assert [channel["sensor_id"] for channel in payload["authoritative_channels"]] == [
        "RX2",
        "RX0",
        "RX1",
    ]

    assert payload["sorted_geometric_view"]["sorted_to_authoritative"] == [
        1,
        2,
        0,
    ]


def test_cli_reports_missing_configuration_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    completed = _run_inspect_config(path)

    assert completed.returncode == 2
    assert completed.stdout == ""

    payload = json.loads(completed.stderr)

    assert payload["error"]["code"] == "configuration_file_not_found"


def test_cli_reports_invalid_configuration_json(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{", encoding="utf-8")

    completed = _run_inspect_config(path)

    assert completed.returncode == 2
    assert completed.stdout == ""

    payload = json.loads(completed.stderr)

    assert payload["error"]["code"] == "invalid_json"
