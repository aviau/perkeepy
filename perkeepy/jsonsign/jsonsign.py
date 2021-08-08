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
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing import cast

import json

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref

from .gpg import GPGSigner
from .gpg import GPGSignerFactory
from .gpg import SubprocessGPGKeyInspector


class SignableJSON(TypedDict):
    camliVersion: Literal[1]
    camliSigner: str


class CamliSig:
    @staticmethod
    def from_armored_gpg_signature(armored_gpg_signature: str) -> str:
        # Cleanup before looking for indexes
        armored_gpg_signature = armored_gpg_signature.strip()

        # Look for start and end indexes
        start_index: int = armored_gpg_signature.index("\n\n")
        end_index: int = armored_gpg_signature.index("\n-----")

        # Isolate the sig
        signature: str = armored_gpg_signature[start_index:end_index]

        # Remove newlines
        signature = signature.replace("\n", "")

        return signature

    @staticmethod
    def to_armored_gpg_signature(camli_sig: str) -> str:
        armored_gpg_signature: str = "-----BEGIN PGP SIGNATURE-----\n\n"

        # Extract the CRC
        last_equal_index: int = camli_sig.rindex("=")
        crc: str = camli_sig[last_equal_index:]
        camli_sig = camli_sig[:last_equal_index]

        chunks: list[str] = []
        while camli_sig:
            chunks.append(camli_sig[:64])
            camli_sig = camli_sig[64:]
        chunks.append(crc)

        armored_gpg_signature += "\n".join(chunks)
        armored_gpg_signature += "\n"

        armored_gpg_signature += "-----END PGP SIGNATURE----\n"
        return armored_gpg_signature


def sign_json_str(
    *,
    unsigned_json_str: str,
    gpg_signer_factory: GPGSignerFactory,
    fetcher: Fetcher,
) -> str:
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
        unsigned_json_object=cast(SignableJSON, json_object),
        gpg_signer_factory=gpg_signer_factory,
        fetcher=fetcher,
    )


def sign_json(
    *,
    unsigned_json_object: SignableJSON,
    gpg_signer_factory: GPGSignerFactory,
    fetcher: Fetcher,
) -> str:

    # Prepare the JSON for signing
    json_str: str = json.dumps(unsigned_json_object, indent=4)
    json_str = json_str.rstrip()
    if not json_str[-1] == "}":
        raise Exception("The json object should end with '}'")
    json_str = json_str[:-1]

    # Find the GPG key fingerprint corresponding to the camliSigner
    camli_signer: str = unsigned_json_object["camliSigner"]
    camli_signer_ref: Ref = Ref.from_ref_str(camli_signer)
    camli_signer_public_key_blob: Optional[Blob] = fetcher.fetch_blob(
        camli_signer_ref
    )
    if not camli_signer_public_key_blob:
        raise Exception(f"Could not fetch public key for signer {camli_signer}")
    camli_signer_key_fingerprint: str = (
        SubprocessGPGKeyInspector().get_key_fingerprint(
            camli_signer_public_key_blob.get_bytes().decode()
        )
    )

    # Create a GPG Signer
    gpg_signer: GPGSigner = gpg_signer_factory.get_gpg_signer(
        fingerprint=camli_signer_key_fingerprint
    )
    armored_signature: str = gpg_signer.sign_detached_armored(
        data=json_str.encode()
    )
    camli_signature: str = CamliSig.from_armored_gpg_signature(
        armored_signature
    )

    signed_json: str = json_str + ',"camliSig":"' + camli_signature + '"}\n'

    return signed_json
