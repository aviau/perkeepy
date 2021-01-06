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


class CamliType(enum.Enum):
    BYTES = "bytes"
    PERMANODE = "permanode"


class JsonSchemaValidator:

    blob_json_schema: Final[Dict] = {
        ##########
        ## BASE ##
        ##########
        "$id": "https://perkeep.org/doc/schema/schemablob.schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Perkeep Schema Blob",
        "type": "object",
        "oneOf": [
            {"$ref": "#/definitions/bytes"},
            {"$ref": "#/definitions/permanode"},
        ],
        ############
        # SUBTYPES #
        ############
        "definitions": {
            ###########
            ## BYTES ##
            ###########
            "bytes": {
                "type": "object",
                "properties": {
                    "camliVersion": {"const": 1},
                    "camliType": {"const": "bytes"},
                    "size": {"type": "number"},
                    "parts": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/bytes-parts"},
                    },
                },
                "required": ["camliVersion", "camliType", "size"],
            },
            "bytes-parts": {
                "type": "object",
                "properties": {
                    "blobRef": {"type": "string"},
                    "bytesRef": {"type": "string"},
                    "size": {"type": "number"},
                },
                "oneOf": [
                    {"required": ["blobRef"]},
                    {"required": ["bytesRef"]},
                ],
                "required": ["size"],
            },
            ###############
            ## PERMANODE ##
            ###############
            "permanode": {
                "type": "object",
                "properties": {
                    "camliVersion": {"const": 1},
                    "camliType": {"const": "permanode"},
                    "random": {"type": "string"},
                    "camliSigner": {"type": "string"},
                },
                "required": [
                    "camliVersion",
                    "camliType",
                    "random",
                    "camliSigner",
                ],
            },
        },
    }

    @classmethod
    def validate(cls, data: Dict) -> List[str]:
        validator = jsonschema.validators.validator_for(
            schema=cls.blob_json_schema
        )(cls.blob_json_schema)

        validation_errors: List[str] = []
        for validation_error in validator.iter_errors(instance=data):
            validation_errors.append(str(validation_error.message))

            print(validation_error)

        return validation_errors

    @classmethod
    def is_valid(cls, data: Dict) -> bool:
        return len(cls.validate(data)) == 0


class SchemaSuperset(TypedDict):
    camliVersion: str
    camliType: str


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
