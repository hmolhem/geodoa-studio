from __future__ import annotations

import json
from enum import StrEnum
from typing import NoReturn, cast

from geodoa.domain.configuration import (
    CustomGeometryConstruction,
    GeometryConfigurationV1,
    ULAGeometryConstruction,
)
from geodoa.domain.geometry import LinearArrayGeometry, SensorChannel1D
from geodoa.domain.ula import (
    ULAGenerationSpec,
    ULAPlacementPolicy,
)

GEOMETRY_CONFIGURATION_SCHEMA = "geodoa.geometry_configuration"
GEOMETRY_CONFIGURATION_SCHEMA_VERSION = 1


class GeometryConfigurationJSONCode(StrEnum):
    INVALID_JSON = "invalid_json"
    DUPLICATE_JSON_KEY = "duplicate_json_key"
    UNSUPPORTED_SCHEMA = "unsupported_schema"
    UNSUPPORTED_SCHEMA_VERSION = "unsupported_schema_version"
    INVALID_CONFIGURATION_STRUCTURE = "invalid_configuration_structure"


class GeometryConfigurationJSONError(ValueError):
    def __init__(
        self,
        code: GeometryConfigurationJSONCode,
        message: str,
    ) -> None:
        super().__init__(message)
        self.code = code


def _reject_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}

    for key, value in pairs:
        if key in result:
            raise GeometryConfigurationJSONError(
                GeometryConfigurationJSONCode.DUPLICATE_JSON_KEY,
                f"Duplicate JSON object key: {key!r}.",
            )

        result[key] = value

    return result


def _reject_nonstandard_constant(token: str) -> NoReturn:
    raise GeometryConfigurationJSONError(
        GeometryConfigurationJSONCode.INVALID_JSON,
        f"Non-standard JSON numeric constant is not permitted: {token!r}.",
    )


def _require_mapping(
    value: object,
    context: str,
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"{context} must be a JSON object.",
        )

    return cast(dict[str, object], value)


def _require_list(
    value: object,
    context: str,
) -> list[object]:
    if not isinstance(value, list):
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"{context} must be a JSON array.",
        )

    return cast(list[object], value)


def _require_exact_keys(
    mapping: dict[str, object],
    expected_keys: set[str],
    context: str,
) -> None:
    actual_keys = set(mapping)

    if actual_keys == expected_keys:
        return

    missing = sorted(expected_keys - actual_keys)
    unexpected = sorted(actual_keys - expected_keys)

    raise GeometryConfigurationJSONError(
        GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
        (
            f"{context} has invalid keys. "
            f"Missing: {missing!r}; unexpected: {unexpected!r}."
        ),
    )


def _require_string(
    value: object,
    context: str,
) -> str:
    if not isinstance(value, str):
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"{context} must be a JSON string.",
        )

    return value


def _require_integer(
    value: object,
    context: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"{context} must be a JSON integer.",
        )

    return value


def _require_number(
    value: object,
    context: str,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"{context} must be a JSON number.",
        )

    return float(value)


def _configuration_document(
    configuration: GeometryConfigurationV1,
) -> dict[str, object]:
    geometry_document: dict[str, object] = {
        "kind": "linear_1d",
        "position_unit": "m",
        "channels": [
            {
                "sensor_id": channel.sensor_id,
                "position_m": channel.position_m,
            }
            for channel in configuration.geometry.channels
        ],
    }

    construction = configuration.construction

    if isinstance(construction, CustomGeometryConstruction):
        construction_document: dict[str, object] = {
            "kind": "custom",
        }

    elif isinstance(construction, ULAGeometryConstruction):
        construction_document = {
            "kind": "ula",
            "generator_version": construction.generator_version,
            "parameters": {
                "sensor_count": construction.spec.sensor_count,
                "spacing_m": construction.spec.spacing_m,
                "anchor_m": construction.spec.anchor_m,
                "placement_policy": construction.spec.placement_policy.value,
            },
        }

    else:  # pragma: no cover - domain contract rejects this invariant.
        raise AssertionError("Unreachable geometry construction type.")

    return {
        "schema": GEOMETRY_CONFIGURATION_SCHEMA,
        "schema_version": GEOMETRY_CONFIGURATION_SCHEMA_VERSION,
        "geometry": geometry_document,
        "construction": construction_document,
    }


def encode_geometry_configuration_json(
    configuration: GeometryConfigurationV1,
) -> str:
    return json.dumps(
        _configuration_document(configuration),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def decode_geometry_configuration_json(
    text: str,
) -> GeometryConfigurationV1:
    try:
        loaded: object = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonstandard_constant,
        )
    except GeometryConfigurationJSONError:
        raise
    except json.JSONDecodeError as exc:
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_JSON,
            f"Invalid JSON document: {exc.msg}.",
        ) from exc

    root = _require_mapping(loaded, "Configuration document")
    _require_exact_keys(
        root,
        {"schema", "schema_version", "geometry", "construction"},
        "Configuration document",
    )

    schema = _require_string(root["schema"], "schema")

    if schema != GEOMETRY_CONFIGURATION_SCHEMA:
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.UNSUPPORTED_SCHEMA,
            f"Unsupported configuration schema: {schema!r}.",
        )

    schema_version = _require_integer(
        root["schema_version"],
        "schema_version",
    )

    if schema_version != GEOMETRY_CONFIGURATION_SCHEMA_VERSION:
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.UNSUPPORTED_SCHEMA_VERSION,
            f"Unsupported configuration schema version: {schema_version!r}.",
        )

    geometry_document = _require_mapping(
        root["geometry"],
        "geometry",
    )
    _require_exact_keys(
        geometry_document,
        {"kind", "position_unit", "channels"},
        "geometry",
    )

    geometry_kind = _require_string(
        geometry_document["kind"],
        "geometry.kind",
    )

    if geometry_kind != "linear_1d":
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"Unsupported geometry kind: {geometry_kind!r}.",
        )

    position_unit = _require_string(
        geometry_document["position_unit"],
        "geometry.position_unit",
    )

    if position_unit != "m":
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"Unsupported physical position unit: {position_unit!r}.",
        )

    channel_documents = _require_list(
        geometry_document["channels"],
        "geometry.channels",
    )

    channels: list[SensorChannel1D] = []

    for index, channel_value in enumerate(channel_documents):
        channel_document = _require_mapping(
            channel_value,
            f"geometry.channels[{index}]",
        )
        _require_exact_keys(
            channel_document,
            {"sensor_id", "position_m"},
            f"geometry.channels[{index}]",
        )

        channels.append(
            SensorChannel1D(
                sensor_id=_require_string(
                    channel_document["sensor_id"],
                    f"geometry.channels[{index}].sensor_id",
                ),
                position_m=_require_number(
                    channel_document["position_m"],
                    f"geometry.channels[{index}].position_m",
                ),
            )
        )

    geometry = LinearArrayGeometry(channels=tuple(channels))

    construction_document = _require_mapping(
        root["construction"],
        "construction",
    )

    construction_kind = _require_string(
        construction_document.get("kind"),
        "construction.kind",
    )

    construction: CustomGeometryConstruction | ULAGeometryConstruction

    if construction_kind == "custom":
        _require_exact_keys(
            construction_document,
            {"kind"},
            "construction",
        )

        construction = CustomGeometryConstruction()

    elif construction_kind == "ula":
        _require_exact_keys(
            construction_document,
            {"kind", "generator_version", "parameters"},
            "construction",
        )

        generator_version = _require_integer(
            construction_document["generator_version"],
            "construction.generator_version",
        )

        parameters = _require_mapping(
            construction_document["parameters"],
            "construction.parameters",
        )
        _require_exact_keys(
            parameters,
            {
                "sensor_count",
                "spacing_m",
                "anchor_m",
                "placement_policy",
            },
            "construction.parameters",
        )

        placement_policy_value = _require_string(
            parameters["placement_policy"],
            "construction.parameters.placement_policy",
        )

        try:
            placement_policy = ULAPlacementPolicy(placement_policy_value)
        except ValueError as exc:
            raise GeometryConfigurationJSONError(
                GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
                (f"Unsupported ULA placement policy: {placement_policy_value!r}."),
            ) from exc

        spec = ULAGenerationSpec(
            sensor_count=_require_integer(
                parameters["sensor_count"],
                "construction.parameters.sensor_count",
            ),
            spacing_m=_require_number(
                parameters["spacing_m"],
                "construction.parameters.spacing_m",
            ),
            anchor_m=_require_number(
                parameters["anchor_m"],
                "construction.parameters.anchor_m",
            ),
            placement_policy=placement_policy,
        )

        construction = ULAGeometryConstruction(
            spec=spec,
            generator_version=generator_version,
        )

    else:
        raise GeometryConfigurationJSONError(
            GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE,
            f"Unsupported construction kind: {construction_kind!r}.",
        )

    return GeometryConfigurationV1(
        geometry=geometry,
        construction=construction,
    )
