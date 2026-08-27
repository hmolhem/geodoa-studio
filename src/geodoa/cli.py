from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from geodoa.application.geometry_inspection import inspect_custom_geometry
from geodoa.domain.geometry import (
    GeometryValidationError,
    LinearArrayGeometry,
    SensorChannel1D,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geodoa")
    subparsers = parser.add_subparsers(dest="command", required=True)

    geometry_parser = subparsers.add_parser("geometry")
    geometry_subparsers = geometry_parser.add_subparsers(
        dest="geometry_command",
        required=True,
    )

    inspect_parser = geometry_subparsers.add_parser("inspect-custom")
    inspect_parser.add_argument(
        "--sensor",
        nargs=2,
        action="append",
        metavar=("SENSOR_ID", "POSITION_M"),
        required=True,
        help="Add one physical sensor channel as SENSOR_ID POSITION_M.",
    )

    return parser


def _run_inspect_custom(args: argparse.Namespace) -> int:
    channels: list[SensorChannel1D] = []

    for sensor_id, position_text in args.sensor:
        try:
            position_m = float(position_text)
        except ValueError:
            error_payload = {
                "error": {
                    "code": "invalid_position_literal",
                    "message": (
                        f"Position {position_text!r} for sensor "
                        f"{sensor_id!r} is not a valid floating-point value."
                    ),
                }
            }
            print(
                json.dumps(error_payload, indent=2, sort_keys=True),
                file=__import__("sys").stderr,
            )
            return 2

        channels.append(
            SensorChannel1D(
                sensor_id=sensor_id,
                position_m=position_m,
            )
        )

    try:
        geometry = LinearArrayGeometry(channels=tuple(channels))
    except GeometryValidationError as exc:
        error_payload = {
            "error": {
                "code": exc.code.value,
                "message": str(exc),
            }
        }
        print(
            json.dumps(error_payload, indent=2, sort_keys=True),
            file=__import__("sys").stderr,
        )
        return 2

    result = inspect_custom_geometry(geometry)

    payload = {
        "geometry_kind": "custom_linear_1d",
        "position_unit": "m",
        "sensor_count": result.metrics.sensor_count,
        "authoritative_channels": [
            {
                "sensor_id": channel.sensor_id,
                "position_m": channel.position_m,
            }
            for channel in result.geometry.channels
        ],
        "sorted_geometric_view": {
            "channels": [
                {
                    "sensor_id": channel.sensor_id,
                    "position_m": channel.position_m,
                }
                for channel in result.sorted_view.channels
            ],
            "sorted_to_authoritative": list(result.sorted_view.sorted_to_authoritative),
            "authoritative_to_sorted": list(result.sorted_view.authoritative_to_sorted),
        },
        "metrics": {
            "centroid_m": result.metrics.centroid_m,
            "aperture_m": result.metrics.aperture_m,
            "adjacent_spacings_m": list(result.metrics.adjacent_spacings_m),
            "min_adjacent_spacing_m": (result.metrics.min_adjacent_spacing_m),
            "max_adjacent_spacing_m": (result.metrics.max_adjacent_spacing_m),
            "mean_adjacent_spacing_m": (result.metrics.mean_adjacent_spacing_m),
        },
        "default_phase_reference": {
            "policy": result.default_phase_reference.policy.value,
            "position_m": result.default_phase_reference.position_m,
        },
        "diagnostics": [diagnostic.value for diagnostic in result.diagnostics],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "geometry" and args.geometry_command == "inspect-custom":
        return _run_inspect_custom(args)

    parser.error("Unsupported command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
