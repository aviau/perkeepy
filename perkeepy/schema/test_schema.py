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
    schema: Schema = Schema.from_blob(
        Blob.from_contents_str(
            """
{"camliVersion": 1,
 "camliType": "bytes",
  "parts": [
    {"blobRef": "digalg-blobref", "size": 1024},
    {"bytesRef": "blobref", "size": 5000000, "offset": 492 },
    {"blobRef": "digalg-blobref", "size": 10}
   ]
}
"""
        )
    )
    assert schema.get_type() == CamliType.BYTES

    schema = Schema.from_blob(
        Blob.from_contents_str(
            """
{"camliVersion": 1,
 "camliType": "bytes",
 "parts": [
    {"blobRef": "sha224-85c65daed99f1a8e55b1043ec7a88d1bb8829cf54a50a87c9de8b625", "size": 66668},
    {"blobRef": "sha224-1f4e786c96e41cbdf52be9ca5b0bfdaa6c4e42b8cac2a6240d4cf50b", "size": 79218},
    {"blobRef": "sha224-5f88afd28c0a568ca9278ec7e4c45c8af97a001e835b76b5ecf255dd", "size": 68778},
    {"blobRef": "sha224-093e5a9cccd18acfc7f41bfc7ab3f2af05a8f6921b4111f8cfd130cf", "size": 76396}
  ]
}
"""
        )
    )
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
