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
    def sign_detached_armored(self, *, fingerprint: str, data: bytes) -> str:
        """
        Returns an ASCII-Armored signature of data, signed with the private
        key corresponding to the given fingerprint.
        """
        ...


class GPGKeyInspector(Protocol):
    def get_key_fingerprint(self, *, armored_key: str) -> str:
        """Returns the fingerprint of an armored GPG key"""
        ...


class GPGSignatureVerifier(Protocol):
    def verify_signature(
        self,
        *,
        data: bytes,
        armored_detached_signature: str,
        armored_public_key: str,
    ) -> bool:
        """
        Verify that the given armored signature is valid for the given data
        and that it was made with the given armored public key.
        """
        ...
