import json
import subprocess
import sys

import pytest


def test_cli_inspects_centered_ula() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-ula",
            "--sensor-count",
            "4",
            "--spacing-m",
            "0.25",
            "--anchor-m",
            "0.0",
            "--placement",
            "centroid",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""

    payload = json.loads(completed.stdout)

    assert payload["geometry_kind"] == "ula"
    assert payload["position_unit"] == "m"
    assert payload["sensor_count"] == 4

    assert payload["generation"] == {
        "sensor_count": 4,
        "spacing_m": 0.25,
        "anchor_m": 0.0,
        "placement_policy": "centroid",
    }

    assert [channel["sensor_id"] for channel in payload["authoritative_channels"]] == [
        "RX0",
        "RX1",
        "RX2",
        "RX3",
    ]

    assert [
        channel["position_m"] for channel in payload["authoritative_channels"]
    ] == pytest.approx([-0.375, -0.125, 0.125, 0.375])

    assert payload["sorted_geometric_view"]["sorted_to_authoritative"] == [0, 1, 2, 3]

    assert payload["sorted_geometric_view"]["authoritative_to_sorted"] == [0, 1, 2, 3]

    assert payload["metrics"]["centroid_m"] == pytest.approx(0.0)
    assert payload["metrics"]["aperture_m"] == pytest.approx(0.75)

    assert payload["metrics"]["adjacent_spacings_m"] == pytest.approx(
        [0.25, 0.25, 0.25]
    )

    assert payload["default_phase_reference"] == {
        "policy": "declared_geometry_centroid",
        "position_m": 0.0,
    }

    assert payload["diagnostics"] == []


def test_cli_inspects_first_sensor_anchored_ula() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-ula",
            "--sensor-count",
            "4",
            "--spacing-m",
            "0.25",
            "--anchor-m",
            "-0.50",
            "--placement",
            "first_sensor",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0

    payload = json.loads(completed.stdout)

    assert [
        channel["position_m"] for channel in payload["authoritative_channels"]
    ] == pytest.approx([-0.50, -0.25, 0.00, 0.25])

    assert payload["metrics"]["centroid_m"] == pytest.approx(-0.125)
    assert payload["metrics"]["aperture_m"] == pytest.approx(0.75)

    assert payload["default_phase_reference"]["position_m"] == pytest.approx(-0.125)


def test_cli_reports_typed_nonpositive_spacing_failure() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-ula",
            "--sensor-count",
            "4",
            "--spacing-m",
            "0.0",
            "--anchor-m",
            "0.0",
            "--placement",
            "centroid",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""

    payload = json.loads(completed.stderr)

    assert payload["error"]["code"] == "nonpositive_spacing"


def test_cli_reports_invalid_spacing_literal() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "geodoa.cli",
            "geometry",
            "inspect-ula",
            "--sensor-count",
            "4",
            "--spacing-m",
            "not-a-number",
            "--anchor-m",
            "0.0",
            "--placement",
            "centroid",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""

    payload = json.loads(completed.stderr)

    assert payload["error"]["code"] == "invalid_spacing_literal"
