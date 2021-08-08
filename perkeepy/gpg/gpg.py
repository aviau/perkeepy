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

from typing import Protocol


class GPGSigner(Protocol):
    def sign_detached_armored(self, *, data: bytes) -> str:
        """Returns an ASCII-Armored signature of data"""
        ...


class GPGSignerFactory(Protocol):
    def get_gpg_signer(self, *, fingerprint: str) -> GPGSigner:
        """Returns a GPG signer for the given key fingerprint"""
        ...


class GPGKeyInspector(Protocol):
    def get_key_fingerprint(self, *, armored_key: str) -> str:
        """Returns the fingerprint of an armored GPG key"""
        ...


class GPGSignatureVerifier(Protocol):
    def verify_signature(self, *, data: bytes, signature: str) -> bool:
        """Verify a GPG signature for the given data"""
        ...


class GPGSignatureVerifierFactory(Protocol):
    def get_gpg_signature_verifier(
        self, *, public_key: str
    ) -> GPGSignatureVerifier:
        """Returns a GPG signature verifier for a given public key"""
        ...
