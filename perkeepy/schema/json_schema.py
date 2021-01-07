from typing import Dict
from typing import Final
from typing import List

import jsonschema


class JsonSchemaValidator:

    blob_json_schema: Final[Dict] = {
        ##########
        ## BASE ##
        ##########
        "$id": "https://perkeep.org/doc/schema/schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Perkeep Schema Blob",
        "type": "object",
        "oneOf": [
            {"$ref": "#/definitions/bytes"},
            {"$ref": "#/definitions/permanode"},
            {"$ref": "#/definitions/file"},
            {"$ref": "#/definitions/claim"},
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
                },
                "required": ["camliVersion", "camliType"],
                "allOf": [
                    {"$ref": "#/definitions/bytes-properties"},
                ],
            },
            "bytes-properties": {
                "type": "object",
                "properties": {
                    "parts": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/bytes-part"},
                    },
                },
            },
            "bytes-part": {
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
            ###########
            ## CLAIM ##
            ###########
            "claim": {
                "type": "object",
                "properties": {
                    "camliVersion": {"const": 1},
                    "camliType": {"const": "claim"},
                    "camliSigner": {"type": "string"},
                    "camliSig": {"type": "string"},
                    "claimDate": {"type": "string", "format": "date"},
                    "permaNode": {"type": "string"},
                    "attribute": {"type": "string"},
                },
                "required": [
                    "camliVersion",
                    "camliType",
                    "claimDate",
                    "permaNode",
                    "attribute",
                    "camliSigner",
                    "camliSig",
                ],
                "oneOf": [
                    {"$ref": "#/definitions/claim-add-attribute"},
                    {"$ref": "#/definitions/claim-set-attribute"},
                    {"$ref": "#/definitions/claim-del-attribute"},
                ],
            },
            "claim-add-attribute": {
                "type": "object",
                "properties": {
                    "claimType": {"const": "add-attribute"},
                },
                "required": [
                    "claimType",
                    "value",
                ],
            },
            "claim-set-attribute": {
                "type": "object",
                "properties": {
                    "claimType": {"const": "set-attribute"},
                },
                "required": [
                    "claimType",
                    "value",
                ],
            },
            "claim-del-attribute": {
                "type": "object",
                "properties": {
                    "claimType": {"const": "del-attribute"},
                },
                "required": [
                    "claimType",
                ],
            },
            ##########
            ## FILE ##
            ##########
            "file": {
                "type": "object",
                "properties": {
                    "camliVersion": {"const": 1},
                    "camliType": {"const": "file"},
                },
                "required": [
                    "camliVersion",
                    "camliType",
                ],
                "allOf": [
                    {"$ref": "#/definitions/bytes-properties"},
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
