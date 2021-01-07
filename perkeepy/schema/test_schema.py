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


def test_schema_from_blob_file() -> None:
    blob: Blob = Blob.from_contents_str(
        """
{
	"camliType": "file",
	"camliVersion": 1,
	"fileName": "pattes_orford.png",
	"parts": [{
		"blobRef": "sha224-0ec3f537a82cb2d95b9929bef457ac21ed1ea22d22ff6b5bc401de31",
		"size": 262144
	}, {
		"blobRef": "sha224-2835a980eb488ae1dfbd5e471cd868fccd9ca7e47b403e8a281666a5",
		"size": 88599
	}, {
		"blobRef": "sha224-ed1d80769d615aec8181d04d9f25492843fbb6eea49fe058d8e34ff8",
		"size": 73889
	}, {
		"blobRef": "sha224-f64dd508cb359703862e31989f74d478faa54c62e50266cab86ddb08",
		"size": 69568
	}, {
		"bytesRef": "sha224-0b2bfe9ce5ac54990512c226e172a144a9a38e16b8b0c88aed6099b1",
		"size": 291060
	}, {
		"blobRef": "sha224-0e4615f54e6575c5e260d18cb760340e44cc150c817e8dbb5562d221",
		"size": 70617
	}, {
		"blobRef": "sha224-3d16526dd3bbc81dba64f5562a90c348e58f5929421c8e786a65e2e6",
		"size": 74981
	}, {
		"blobRef": "sha224-f25954248c1d91cc4465fc304b35cd0ec3075431c8d4c06e9fcb42ec",
		"size": 16558
	}],
	"unixMtime": "2020-10-21T04:51:52Z"
}
"""
    )
    schema: Schema = Schema.from_blob(blob)
    assert schema.get_type() == CamliType.FILE


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
