import jsonschema
import pytest

from perkeepy.blob import Blob
from perkeepy.schema import Schema

from .schema import CamliType
from .schema import JsonSchemaValidator


def test_json_schema() -> None:
    """Validate that our JSON Schema is correct."""

    assert JsonSchemaValidator.is_valid(
        {
            "camliVersion": 1,
            "camliType": "bytes",
            "size": 0,
        }
    )

    assert not JsonSchemaValidator.is_valid(
        {
            "camliType": "bytes",
        }
    )


def test_schema_from_blob_bytes() -> None:
    blob: Blob = Blob.from_contents_str(
        """
{"camliVersion": 1,
 "camliType": "bytes",
 "size": 11,
  "parts": [
    {"blobRef": "digalg-blobref", "size": 1024},
    {"bytesRef": "blobref", "size": 5000000, "offset": 492 },
    {"blobRef": "digalg-blobref", "size": 10}
   ]
}
"""
    )
    schema: Schema = Schema.from_blob(blob)
    assert schema.get_type() == CamliType.BYTES


def test_schema_from_blob_permanode() -> None:
    blob: Blob = Blob.from_contents_str(
        """
{"camliVersion": 1,
 "camliType": "permanode",
 "random": "615e05c68c8411df81a2001b639d041f",
 "camliSigner": "hashalg-xxxxxxxxxxx"
}
"""
    )
    schema: Schema = Schema.from_blob(blob)
    assert schema.get_type() == CamliType.PERMANODE


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
    with pytest.raises(Exception):
        schema: Schema = Schema.from_blob(blob)
