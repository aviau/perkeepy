# Copyright 2021 The Perkeepy Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any
from typing import Final
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing import cast

import json

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref
from perkeepy.gpg import GPGKeyInspector
from perkeepy.gpg import GPGSignatureVerifier
from perkeepy.gpg import GPGSigner

from .camlisig import CamliSig


class _SignableJSON(TypedDict):
    camliVersion: Literal[1]
    camliSigner: str


_SIGNATURE_DELIMITER: Final[bytes] = b',"camliSig":"'


def sign_json_str(
    *,
    unsigned_json_str: str,
    gpg_signer: GPGSigner,
    gpg_key_inspector: GPGKeyInspector,
    fetcher: Fetcher,
) -> bytes:
    """
    Signs JSON objects with the right GPG key based on the camliSigner.
    """

    json_object: Any = json.loads(unsigned_json_str)
    if not isinstance(json_object, dict):
        raise Exception(
            f"JSON string must be an object, got {type(json_object)}"
        )

    camli_version: Any = json_object.get("camliVersion", None)
    if not camli_version == 1:
        raise Exception(f"Unknown camliVersion {camli_version}")

    camli_signer: Any = json_object.get("camliSigner")
    if not isinstance(camli_signer, str):
        raise Exception(
            f"Expected camliSigner to be a string, got {type(camli_signer)}"
        )

    return sign_json(
        unsigned_json_object=cast(_SignableJSON, json_object),
        gpg_signer=gpg_signer,
        gpg_key_inspector=gpg_key_inspector,
        fetcher=fetcher,
    )


def sign_json(
    *,
    unsigned_json_object: _SignableJSON,
    gpg_signer: GPGSigner,
    gpg_key_inspector: GPGKeyInspector,
    fetcher: Fetcher,
) -> bytes:

    # Prepare the JSON for signing
    json_bytes: bytes = json.dumps(unsigned_json_object, indent=4).encode()
    json_bytes = json_bytes.rstrip()
    if not json_bytes.endswith(b"}"):
        raise Exception("The json object should end with '}'")
    json_bytes = json_bytes.removesuffix(b"}")

    # Find the GPG key fingerprint corresponding to the camliSigner
    camli_signer: str = unsigned_json_object["camliSigner"]
    camli_signer_ref: Ref = Ref.from_ref_str(camli_signer)
    camli_signer_public_key_blob: Optional[Blob] = fetcher.fetch_blob(
        camli_signer_ref
    )
    if not camli_signer_public_key_blob:
        raise Exception(f"Could not fetch public key for signer {camli_signer}")
    camli_signer_key_fingerprint: str = gpg_key_inspector.get_key_fingerprint(
        armored_key=camli_signer_public_key_blob.get_bytes().decode(),
    )

    # Sign
    armored_signature: str = gpg_signer.sign_detached_armored(
        fingerprint=camli_signer_key_fingerprint, data=json_bytes
    )
    camli_signature: str = CamliSig.from_armored_gpg_signature(
        armored_signature
    )

    signed_json: bytes = (
        json_bytes + _SIGNATURE_DELIMITER + camli_signature.encode() + b'"}\n'
    )

    return signed_json


def verify_json_signature(
    *,
    signed_json_object: bytes,
    fetcher: Fetcher,
    gpg_signature_verifier: GPGSignatureVerifier,
) -> bool:
    # Load the JSON object
    json_obj: Any = json.loads(signed_json_object)
    if not isinstance(json_obj, dict):
        raise Exception(f"JSON must be an object, got {type(json_obj)}")

    # Extract the signature
    camli_signature: Any = json_obj.get("camliSig", None)
    if not isinstance(camli_signature, str):
        raise Exception(
            f"camliSig must be a string, got {type(camli_signature)}"
        )
    camli_signature_armored: str = CamliSig.to_armored_gpg_signature(
        camli_signature
    )

    # Find the camliSigner's public key
    camli_signer: Any = json_obj.get("camliSigner", None)
    if not isinstance(camli_signer, str):
        raise Exception(
            f"camliSigner must be a string, got {type(camli_signer)}"
        )
    camli_signer_ref: Ref = Ref.from_ref_str(camli_signer)
    camli_signer_public_key_blob: Optional[Blob] = fetcher.fetch_blob(
        camli_signer_ref
    )
    if not camli_signer_public_key_blob:
        raise Exception(f"Could not fetch public key for signer {camli_signer}")
    camli_signer_public_key: str = (
        camli_signer_public_key_blob.get_bytes().decode()
    )

    # Isolate the signed content
    signed_bytes_end_index = signed_json_object.rindex(_SIGNATURE_DELIMITER)
    signed_bytes: bytes = signed_json_object[:signed_bytes_end_index]

    # Verify the signature
    result = gpg_signature_verifier.verify_signature(
        data=signed_bytes,
        armored_detached_signature=camli_signature_armored,
        armored_public_key=camli_signer_public_key,
    )

    return result
