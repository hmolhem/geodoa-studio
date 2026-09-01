import json

import pytest

from geodoa.domain.configuration import (
    CustomGeometryConstruction,
    GeometryConfigurationCode,
    GeometryConfigurationError,
    GeometryConfigurationV1,
    ULAGeometryConstruction,
)
from geodoa.domain.geometry import (
    GeometryValidationCode,
    GeometryValidationError,
    LinearArrayGeometry,
    SensorChannel1D,
)
from geodoa.domain.ula import (
    ULAGenerationSpec,
    ULAPlacementPolicy,
    generate_ula,
)
from geodoa.serialization.geometry_configuration_json import (
    GEOMETRY_CONFIGURATION_SCHEMA,
    GEOMETRY_CONFIGURATION_SCHEMA_VERSION,
    GeometryConfigurationJSONCode,
    GeometryConfigurationJSONError,
    decode_geometry_configuration_json,
    encode_geometry_configuration_json,
)


def test_custom_configuration_round_trip_preserves_authoritative_geometry() -> None:
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

    encoded = encode_geometry_configuration_json(configuration)
    decoded = decode_geometry_configuration_json(encoded)

    assert decoded == configuration
    assert tuple(channel.sensor_id for channel in decoded.geometry.channels) == (
        "RX2",
        "RX0",
        "RX1",
    )


def test_ula_configuration_round_trip_preserves_construction_provenance() -> None:
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

    encoded = encode_geometry_configuration_json(configuration)
    decoded = decode_geometry_configuration_json(encoded)

    assert decoded == configuration


def test_encoding_is_deterministic_across_round_trip() -> None:
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

    first_encoding = encode_geometry_configuration_json(configuration)
    decoded = decode_geometry_configuration_json(first_encoding)
    second_encoding = encode_geometry_configuration_json(decoded)

    assert second_encoding == first_encoding


def test_encoded_document_contains_explicit_schema_and_resolved_geometry() -> None:
    spec = ULAGenerationSpec(
        sensor_count=2,
        spacing_m=0.25,
        anchor_m=0.0,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    document = json.loads(encode_geometry_configuration_json(configuration))

    assert document["schema"] == GEOMETRY_CONFIGURATION_SCHEMA
    assert document["schema_version"] == GEOMETRY_CONFIGURATION_SCHEMA_VERSION
    assert document["geometry"]["position_unit"] == "m"
    assert document["geometry"]["channels"] == [
        {"sensor_id": "RX0", "position_m": 0.0},
        {"sensor_id": "RX1", "position_m": 0.25},
    ]


def test_decoder_rejects_invalid_json() -> None:
    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json("{")

    assert exc_info.value.code is GeometryConfigurationJSONCode.INVALID_JSON


def test_decoder_rejects_duplicate_json_key() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema":"duplicate",'
        '"schema_version":1,'
        '"geometry":{},'
        '"construction":{}}'
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert exc_info.value.code is GeometryConfigurationJSONCode.DUPLICATE_JSON_KEY


@pytest.mark.parametrize(
    "token",
    [
        "NaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_decoder_rejects_nonstandard_json_numeric_constants(
    token: str,
) -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":1,'
        '"geometry":{'
        '"kind":"linear_1d",'
        '"position_unit":"m",'
        '"channels":[{"sensor_id":"RX0","position_m":'
        f"{token}"
        "}]},"
        '"construction":{"kind":"custom"}}'
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert exc_info.value.code is GeometryConfigurationJSONCode.INVALID_JSON


def test_decoder_rejects_unsupported_schema() -> None:
    text = (
        '{"schema":"other.schema","schema_version":1,"geometry":{},"construction":{}}'
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert exc_info.value.code is GeometryConfigurationJSONCode.UNSUPPORTED_SCHEMA


def test_decoder_rejects_unsupported_schema_version() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":2,'
        '"geometry":{},'
        '"construction":{}}'
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert (
        exc_info.value.code is GeometryConfigurationJSONCode.UNSUPPORTED_SCHEMA_VERSION
    )


def test_decoder_rejects_unexpected_root_key() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":1,'
        '"geometry":{},'
        '"construction":{},'
        '"unexpected":true}'
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert (
        exc_info.value.code
        is GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE
    )


def test_decoder_rejects_invalid_ula_placement_policy() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":1,'
        '"geometry":{'
        '"kind":"linear_1d",'
        '"position_unit":"m",'
        '"channels":[{"sensor_id":"RX0","position_m":0.0}]},'
        '"construction":{'
        '"kind":"ula",'
        '"generator_version":1,'
        '"parameters":{'
        '"sensor_count":1,'
        '"spacing_m":0.25,'
        '"anchor_m":0.0,'
        '"placement_policy":"invalid"'
        "}}}"
    )

    with pytest.raises(GeometryConfigurationJSONError) as exc_info:
        decode_geometry_configuration_json(text)

    assert (
        exc_info.value.code
        is GeometryConfigurationJSONCode.INVALID_CONFIGURATION_STRUCTURE
    )


def test_decoder_preserves_domain_geometry_validation() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":1,'
        '"geometry":{'
        '"kind":"linear_1d",'
        '"position_unit":"m",'
        '"channels":[]},'
        '"construction":{"kind":"custom"}}'
    )

    with pytest.raises(GeometryValidationError) as exc_info:
        decode_geometry_configuration_json(text)

    assert exc_info.value.code is GeometryValidationCode.EMPTY_GEOMETRY


def test_decoder_detects_ula_construction_geometry_mismatch() -> None:
    text = (
        '{"schema":"geodoa.geometry_configuration",'
        '"schema_version":1,'
        '"geometry":{'
        '"kind":"linear_1d",'
        '"position_unit":"m",'
        '"channels":['
        '{"sensor_id":"RX0","position_m":0.0},'
        '{"sensor_id":"RX1","position_m":0.3}'
        "]},"
        '"construction":{'
        '"kind":"ula",'
        '"generator_version":1,'
        '"parameters":{'
        '"sensor_count":2,'
        '"spacing_m":0.25,'
        '"anchor_m":0.0,'
        '"placement_policy":"first_sensor"'
        "}}}"
    )

    with pytest.raises(GeometryConfigurationError) as exc_info:
        decode_geometry_configuration_json(text)

    assert (
        exc_info.value.code is GeometryConfigurationCode.CONSTRUCTION_GEOMETRY_MISMATCH
    )


def test_deterministic_encoding_normalizes_integral_physical_values() -> None:
    spec = ULAGenerationSpec(
        sensor_count=2,
        spacing_m=1,
        anchor_m=0,
        placement_policy=ULAPlacementPolicy.FIRST_SENSOR,
    )

    configuration = GeometryConfigurationV1(
        geometry=generate_ula(spec),
        construction=ULAGeometryConstruction(spec=spec),
    )

    encoded_1 = encode_geometry_configuration_json(configuration)
    encoded_2 = encode_geometry_configuration_json(
        decode_geometry_configuration_json(encoded_1)
    )

    assert encoded_2 == encoded_1
    assert '"position_m":0.0' in encoded_1
    assert '"spacing_m":1.0' in encoded_1
    assert '"anchor_m":0.0' in encoded_1
