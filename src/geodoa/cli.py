from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from geodoa.application.configuration_persistence import (
    load_and_inspect_geometry_configuration,
)
from geodoa.application.geometry_inspection import (
    GeometryInspectionResult,
    inspect_custom_geometry,
)
from geodoa.application.ula_inspection import inspect_ula_geometry
from geodoa.domain.configuration import (
    GeometryConfigurationError,
    ULAGeometryConstruction,
)
from geodoa.domain.geometry import (
    GeometryValidationError,
    LinearArrayGeometry,
    SensorChannel1D,
)
from geodoa.domain.ula import (
    ULAGenerationError,
    ULAGenerationSpec,
    ULAPlacementPolicy,
)
from geodoa.serialization.geometry_configuration_json import (
    GeometryConfigurationJSONError,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geodoa")
    subparsers = parser.add_subparsers(dest="command", required=True)

    geometry_parser = subparsers.add_parser("geometry")
    geometry_subparsers = geometry_parser.add_subparsers(
        dest="geometry_command",
        required=True,
    )

    inspect_custom_parser = geometry_subparsers.add_parser("inspect-custom")
    inspect_custom_parser.add_argument(
        "--sensor",
        nargs=2,
        action="append",
        metavar=("SENSOR_ID", "POSITION_M"),
        required=True,
        help="Add one physical sensor channel as SENSOR_ID POSITION_M.",
    )

    inspect_ula_parser = geometry_subparsers.add_parser("inspect-ula")
    inspect_ula_parser.add_argument("--sensor-count", required=True)
    inspect_ula_parser.add_argument("--spacing-m", required=True)
    inspect_ula_parser.add_argument("--anchor-m", required=True)
    inspect_ula_parser.add_argument(
        "--placement",
        choices=[policy.value for policy in ULAPlacementPolicy],
        required=True,
    )

    inspect_config_parser = geometry_subparsers.add_parser("inspect-config")
    inspect_config_parser.add_argument(
        "--input",
        required=True,
        help="Path to a canonical GeoDOA geometry configuration JSON file.",
    )

    return parser


def _print_error(code: str, message: str) -> int:
    error_payload = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    print(
        json.dumps(error_payload, indent=2, sort_keys=True),
        file=sys.stderr,
    )
    return 2


def _inspection_payload(
    result: GeometryInspectionResult,
    *,
    geometry_kind: str,
    generation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "geometry_kind": geometry_kind,
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
            "min_adjacent_spacing_m": result.metrics.min_adjacent_spacing_m,
            "max_adjacent_spacing_m": result.metrics.max_adjacent_spacing_m,
            "mean_adjacent_spacing_m": result.metrics.mean_adjacent_spacing_m,
        },
        "default_phase_reference": {
            "policy": result.default_phase_reference.policy.value,
            "position_m": result.default_phase_reference.position_m,
        },
        "diagnostics": [diagnostic.value for diagnostic in result.diagnostics],
    }

    if generation is not None:
        payload["generation"] = generation

    return payload


def _run_inspect_custom(args: argparse.Namespace) -> int:
    channels: list[SensorChannel1D] = []

    for sensor_id, position_text in args.sensor:
        try:
            position_m = float(position_text)
        except ValueError:
            return _print_error(
                "invalid_position_literal",
                (
                    f"Position {position_text!r} for sensor "
                    f"{sensor_id!r} is not a valid floating-point value."
                ),
            )

        channels.append(
            SensorChannel1D(
                sensor_id=sensor_id,
                position_m=position_m,
            )
        )

    try:
        geometry = LinearArrayGeometry(channels=tuple(channels))
    except GeometryValidationError as exc:
        return _print_error(exc.code.value, str(exc))

    result = inspect_custom_geometry(geometry)

    print(
        json.dumps(
            _inspection_payload(
                result,
                geometry_kind="custom_linear_1d",
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_inspect_ula(args: argparse.Namespace) -> int:
    try:
        sensor_count = int(args.sensor_count)
    except ValueError:
        return _print_error(
            "invalid_sensor_count_literal",
            (f"Sensor count {args.sensor_count!r} is not a valid integer."),
        )

    try:
        spacing_m = float(args.spacing_m)
    except ValueError:
        return _print_error(
            "invalid_spacing_literal",
            (f"Spacing {args.spacing_m!r} is not a valid floating-point value."),
        )

    try:
        anchor_m = float(args.anchor_m)
    except ValueError:
        return _print_error(
            "invalid_anchor_literal",
            (f"Anchor {args.anchor_m!r} is not a valid floating-point value."),
        )

    placement_policy = ULAPlacementPolicy(args.placement)

    try:
        spec = ULAGenerationSpec(
            sensor_count=sensor_count,
            spacing_m=spacing_m,
            anchor_m=anchor_m,
            placement_policy=placement_policy,
        )
        result = inspect_ula_geometry(spec)
    except ULAGenerationError as exc:
        return _print_error(exc.code.value, str(exc))

    print(
        json.dumps(
            _inspection_payload(
                result.inspection,
                geometry_kind="ula",
                generation={
                    "sensor_count": spec.sensor_count,
                    "spacing_m": spec.spacing_m,
                    "anchor_m": spec.anchor_m,
                    "placement_policy": spec.placement_policy.value,
                },
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_inspect_config(args: argparse.Namespace) -> int:
    try:
        result = load_and_inspect_geometry_configuration(args.input)
    except GeometryConfigurationJSONError as exc:
        return _print_error(exc.code.value, str(exc))
    except GeometryValidationError as exc:
        return _print_error(exc.code.value, str(exc))
    except GeometryConfigurationError as exc:
        return _print_error(exc.code.value, str(exc))
    except FileNotFoundError:
        return _print_error(
            "configuration_file_not_found",
            f"Configuration file was not found: {args.input!r}.",
        )
    except UnicodeDecodeError:
        return _print_error(
            "invalid_configuration_utf8",
            "Configuration file is not valid UTF-8.",
        )

    construction = result.configuration.construction

    generation: dict[str, Any] | None = None
    geometry_kind = "custom_linear_1d"

    if isinstance(construction, ULAGeometryConstruction):
        geometry_kind = "ula"
        generation = {
            "sensor_count": construction.spec.sensor_count,
            "spacing_m": construction.spec.spacing_m,
            "anchor_m": construction.spec.anchor_m,
            "placement_policy": construction.spec.placement_policy.value,
            "generator_version": construction.generator_version,
        }

    print(
        json.dumps(
            _inspection_payload(
                result.inspection,
                geometry_kind=geometry_kind,
                generation=generation,
            ),
            indent=2,
            sort_keys=True,
        )
    )

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "geometry":
        if args.geometry_command == "inspect-custom":
            return _run_inspect_custom(args)

        if args.geometry_command == "inspect-ula":
            return _run_inspect_ula(args)

        if args.geometry_command == "inspect-config":
            return _run_inspect_config(args)

    parser.error("Unsupported command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
