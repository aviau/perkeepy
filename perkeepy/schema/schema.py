from typing import Dict
from typing import Final
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypedDict

import enum
import json

import jsonschema

from perkeepy.blob import Blob

from .json_schema import JsonSchemaValidator


class CamliType(enum.Enum):
    BYTES = "bytes"
    PERMANODE = "permanode"
    FILE = "file"
    CLAIM = "claim"


class BytesPart(TypedDict):
    size: int
    blobRef: str
    bytesRef: str


class SchemaSuperset(TypedDict):
    camliVersion: str
    camliType: str
    parts: List[BytesPart]


class Schema:
    """
    A schema is a JSON-encoded blob that describes other blobs. We recognize
    a schema by the presence of the "camliVersion" and "camliType" fields.
    """

    SCHEMA_MAX_BYTES: Final[int] = 1000000

    def __init__(self, blob: Blob, ss: SchemaSuperset) -> None:
        self._blob = blob
        self._ss = ss

    def get_type(self) -> CamliType:
        return CamliType(self._ss["camliType"])

    @classmethod
    def from_blob(cls, blob: Blob) -> "Schema":
        if len(blob.get_bytes()) > cls.SCHEMA_MAX_BYTES:
            raise Exception(
                f"Schema blobs must be smaller than {cls.SCHEMA_MAX_BYTES} bytes, got {len(blob.get_bytes())}"
            )

        if not blob.is_utf8():
            raise Exception("Schema blobs must be encoded using utf-8")

        blob_str: str = blob.get_bytes().decode("utf-8")

        blob_json: SchemaSuperset = json.loads(blob_str)

        validation_errors = JsonSchemaValidator.validate(dict(blob_json))
        if validation_errors:
            raise Exception(
                f"The blob's schema is not valid: {str(validation_errors)}"
            )

        return cls(
            blob=blob,
            ss=blob_json,
        )

    def get_superset(self) -> SchemaSuperset:
        return self._ss

    def as_bytes(self) -> "BytesSchema":
        return BytesSchema(schema=self)

    def as_file(self) -> "FileSchema":
        return FileSchema(schema=self)


class BytesSchema:
    def __init__(self, schema: Schema) -> None:
        if schema.get_type() != CamliType.BYTES:
            raise Exception(
                f"Invalid camliType: got {schema.get_type()} and expected {CamliType.BYTES.value}"
            )
        self._schema = schema

    def get_parts(self) -> List[BytesPart]:
        return self._schema.get_superset().get("parts", [])


class FileSchema(BytesSchema):
    def __init__(self, schema: Schema) -> None:
        if schema.get_type() != CamliType.FILE:
            raise Exception(
                f"Invalid camliype: got {schema.get_type()} and expected {CamliType.FILE.value}"
            )
        self._schema = schema
