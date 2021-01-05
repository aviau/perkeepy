import jsonschema
import pytest

from perkeepy.blob import Blob
from perkeepy.schema import Schema

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


def test_schema_from_blob() -> None:
    blob: Blob = Blob.from_contents_str(
        """
{"camliVersion": 1,
 "camliType": "bytes",
  "parts": [
    {"blobRef": "digalg-blobref", "size": 1024},
    {"bytesRef": "digalg-blobref", "size": 5000000, "offset": 492 },
    {"blobRef": "digalg-blobref", "size": 10}
   ]
}
"""
    )
    schema: Schema = Schema.from_blob(blob)


def test_schema_from_blob_raises() -> None:
    blob: Blob = Blob.from_contents_str(
        """
{"camliVersion": 1,
  "parts": [
    {"blobRef": "digalg-blobref", "size": 1024},
    {"bytesRef": "digalg-blobref", "size": 5000000, "offset": 492 },
    {"blobRef": "digalg-blobref", "size": 10}
   ]
}
"""
    )
    with pytest.raises(Exception, match=".*camliType/*"):
        schema: Schema = Schema.from_blob(blob)
