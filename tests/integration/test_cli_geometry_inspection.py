import json
import subprocess
import sys


def test_cli_inspects_unsorted_custom_geometry() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-custom",
            "--sensor",
            "RX2",
            "0.30",
            "--sensor",
            "RX0",
            "0.00",
            "--sensor",
            "RX1",
            "0.15",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""

    payload = json.loads(completed.stdout)

    assert payload["geometry_kind"] == "custom_linear_1d"
    assert payload["position_unit"] == "m"
    assert payload["sensor_count"] == 3

    assert [channel["sensor_id"] for channel in payload["authoritative_channels"]] == [
        "RX2",
        "RX0",
        "RX1",
    ]

    assert [
        channel["sensor_id"] for channel in payload["sorted_geometric_view"]["channels"]
    ] == ["RX0", "RX1", "RX2"]

    assert payload["sorted_geometric_view"]["sorted_to_authoritative"] == [1, 2, 0]

    assert payload["sorted_geometric_view"]["authoritative_to_sorted"] == [2, 0, 1]

    assert payload["metrics"]["centroid_m"] == 0.15
    assert payload["metrics"]["aperture_m"] == 0.3
    assert payload["metrics"]["adjacent_spacings_m"] == [
        0.15,
        0.15,
    ]

    assert payload["default_phase_reference"] == {
        "policy": "declared_geometry_centroid",
        "position_m": 0.15,
    }

    assert payload["diagnostics"] == []


def test_cli_reports_typed_duplicate_position_failure() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-custom",
            "--sensor",
            "RX0",
            "0.0",
            "--sensor",
            "RX1",
            "0.0",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""

    payload = json.loads(completed.stderr)

    assert payload["error"]["code"] == "duplicate_position"
