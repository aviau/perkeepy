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

from typing import Iterator

import tempfile
from contextlib import contextmanager

from gnupg import GPG
from gnupg import ImportResult

from perkeepy.gpg import GPGKeyInspector
from perkeepy.gpg import GPGSignatureVerifier
from perkeepy.gpg import GPGSigner


@contextmanager
def _temp_gpg_instance() -> Iterator[GPG]:
    with tempfile.TemporaryDirectory(
        prefix="perkeepy-temp-gpg-instance"
    ) as tempdir:
        yield GPG(
            gnupghome=tempdir,
            use_agent=False,
        )


class SubprocessGPGKeyInspector:
    def get_key_fingerprint(self, *, armored_key: str) -> str:
        with _temp_gpg_instance() as gpg:
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


class SubprocessGPGSigner:
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

    def sign_detached_armored(self, *, fingerprint: str, data: bytes) -> str:
        return self._gpg.sign(
            message=data,
            keyid=fingerprint,
            detach=True,
            binary=False,
        ).data.decode()

    @staticmethod
    def _assert_implements_gpg_signer(
        signer: "SubprocessGPGSigner",
    ) -> GPGSigner:
        return signer


class SubprocessGPGSignatureVerifier:
    def verify_signature(
        self,
        *,
        data: bytes,
        armored_detached_signature: str,
        armored_public_key: str,
    ) -> bool:
        with _temp_gpg_instance() as gpg:
            import_result: "ImportResult" = gpg.import_keys(armored_public_key)
            imported_fingerprints: list[str] = import_result.fingerprints
            if not imported_fingerprints:
                raise Exception(
                    f"Could not import the provided key: {str(import_result.stderr)}",
                )
            with tempfile.NamedTemporaryFile(mode="w") as signature_tempfile:
                signature_tempfile.write(armored_detached_signature)
                signature_tempfile.flush()
                verified = gpg.verify_data(
                    sig_filename=signature_tempfile.name,
                    data=data,
                )
        return bool(
            verified.valid is True
            and verified.fingerprint
            and verified.fingerprint in imported_fingerprints
        )

    @staticmethod
    def _assert_implements_gpg_signature_verifier(
        v: "SubprocessGPGSignatureVerifier",
    ) -> GPGSignatureVerifier:
        return v
