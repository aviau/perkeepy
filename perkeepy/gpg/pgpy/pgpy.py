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

import pgpy
import pgpy.types
from pgpy import PGPSignature

from perkeepy.gpg import GPGKeyInspector
from perkeepy.gpg import GPGSignatureVerifier
from perkeepy.gpg import GPGSigner


class PGPYGPGSigner:
    def __init__(
        self,
        armored_private_keys: list[str],
    ) -> None:
        self._keys: dict[str, pgpy.PGPKey] = {}

        for armored_private_key in armored_private_keys:
            private_key: pgpy.PGPKey = pgpy.PGPKey()
            private_key.parse(armored_private_key)

            if private_key.is_public:
                raise Exception(f"Key {private_key.fingerprint} is public")

            self._keys[private_key.fingerprint] = private_key

    def _has_private_key(self, *, fingerprint: str) -> bool:
        return fingerprint in self._keys

    def sign_detached_armored(self, *, fingerprint: str, data: bytes) -> str:
        if not self._has_private_key(fingerprint=fingerprint):
            raise Exception(
                f"No private key with a matching fingerprint for {fingerprint}"
            )

        signature: PGPSignature = self._keys[fingerprint].sign(data)
        signature_armored: str = str(signature)
        return signature_armored

    @staticmethod
    def _assert_implements_gpg_signer(
        signer: "PGPYGPGSigner",
    ) -> GPGSigner:
        return signer


class PGPYGPGKeyInspector:
    def get_key_fingerprint(self, *, armored_key: str) -> str:
        key: pgpy.PGPKey = pgpy.PGPKey()
        key.parse(armored_key)
        return key.fingerprint

    @staticmethod
    def _assert_implements_gpg_key_inspector(
        inspector: "PGPYGPGKeyInspector",
    ) -> GPGKeyInspector:
        return inspector


class PGPYGPGSignatureVerifier:
    def verify_signature(
        self,
        *,
        data: bytes,
        armored_detached_signature: str,
        armored_public_key: str,
    ) -> bool:
        # Load sig
        signature: pgpy.PGPSignature = pgpy.PGPSignature()
        signature.parse(armored_detached_signature)

        # Load key
        key: pgpy.PGPKey = pgpy.PGPKey()
        key.parse(armored_public_key)

        # Verify
        verified: pgpy.types.SignatureVerification = key.verify(data, signature)
        is_verified: bool = bool(verified)

        return is_verified

    @staticmethod
    def _assert_implements_gpg_signature_verifier(
        verifier: "PGPYGPGSignatureVerifier",
    ) -> GPGSignatureVerifier:
        return verifier
