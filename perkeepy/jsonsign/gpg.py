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

from typing import TYPE_CHECKING
from typing import Iterator
from typing import Optional
from typing import Protocol
from typing import TypedDict

import tempfile
from contextlib import contextmanager

from gnupg import GPG


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


class SubprocessGPGKeyInspector:
    @contextmanager
    def _temp_gpg_instance(self) -> Iterator[GPG]:
        with tempfile.TemporaryDirectory() as tempdir:
            yield GPG(gnupghome=tempdir)

    def get_key_fingerprint(self, armored_key: str) -> str:
        with self._temp_gpg_instance() as gpg:
            imported_fingerprints: list[str] = gpg.import_keys(
                key_data=armored_key
            ).fingerprints
            if len(imported_fingerprints) == 0:
                raise Exception("No key found")

            if len(imported_fingerprints) > 1:
                raise Exception("More than 1 key was imported")

            return imported_fingerprints[0]

    @staticmethod
    def _assert_implements_gpg_key_inspector(
        inspector: "SubprocessGPGKeyInspector",
    ) -> GPGKeyInspector:
        return inspector


class SubprocessGPGSignerFactory:
    def __init__(
        self,
        gpg_home_path: str,
        private_key_data: str,
    ) -> None:
        self._gpg: GPG = GPG(
            gnupghome=gpg_home_path,
            use_agent=False,
        )
        self._gpg.import_keys(key_data=private_key_data)

    def _has_private_key(self, fingerprint: str) -> bool:
        for key in self._gpg.list_keys(secret=True):
            if key["fingerprint"] == fingerprint:
                return True
        return False

    def get_gpg_signer(self, fingerprint: str) -> GPGSigner:
        if not self._has_private_key(fingerprint):
            raise Exception(
                f"No private key matching fingerprint {fingerprint}"
            )
        return SubprocessGPGSigner(
            gpg=self._gpg,
            fingerprint=fingerprint,
        )

    @staticmethod
    def _assert_implements_gpg_signer_factory(
        signer_factory: "SubprocessGPGSignerFactory",
    ) -> GPGSignerFactory:
        return signer_factory


class SubprocessGPGSigner:
    def __init__(self, gpg: GPG, fingerprint: str):
        self._gpg: GPG = gpg
        self._fingerprint: str = fingerprint

    def sign_detached_armored(self, data: bytes) -> str:
        return self._gpg.sign(
            message=data,
            keyid=self._fingerprint,
            detach=True,
            binary=False,
        ).data.decode()

    @staticmethod
    def _assert_implements_gpg_signer(
        signer: "SubprocessGPGSigner",
    ) -> GPGSigner:
        return signer
