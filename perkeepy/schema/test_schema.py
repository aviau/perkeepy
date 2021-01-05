import jsonschema

from perkeepy.blob import Blob

from .schema import JsonSchemaValidator


def test_json_schema() -> None:
    """Validate that our JSON Schema is correct."""

    assert JsonSchemaValidator.is_valid(
        {
            "camliVersion": 1,
            "camliType": "bytes",
        }
    )

    assert not JsonSchemaValidator.is_valid(
        {
            "camliType": "bytes",
        }
    )

    assert any(
        message == "'camliVersion' is a required property"
        for message in JsonSchemaValidator.validate(
            {
                "camliType": "bytes",
            }
        )
    )
