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

import json
import os
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass

import pytest

from perkeepy import jsonsign
from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.blobserver import Storage
from perkeepy.blobserver.memory import MemoryBlobServer
from perkeepy.gpg import GPGKeyInspector
from perkeepy.gpg import GPGSignatureVerifier
from perkeepy.gpg import GPGSigner
from perkeepy.gpg.subprocess import SubprocessGPGKeyInspector
from perkeepy.gpg.subprocess import SubprocessGPGSignatureVerifier
from perkeepy.gpg.subprocess import SubprocessGPGSigner


@dataclass
class JSONSignTestEnv:
    bs: Storage
    gpg_key_inspector: GPGKeyInspector
    gpg_signer: GPGSigner
    gpg_signature_verifier: GPGSignatureVerifier
    public_key_ref: Ref


@contextmanager
def get_test_env() -> Iterator[JSONSignTestEnv]:
    """Returns utils for performing a jsonsign test"""

    # Create a blobserver
    bs: Storage = MemoryBlobServer()

    # Add a public key
    with open(
        os.path.join(os.path.dirname(__file__), "testdata", "key01.pub"),
        encoding="utf-8",
    ) as public_key_file:
        public_key_blob: Blob = Blob.from_contents_str(public_key_file.read())
        bs.receive_blob(public_key_blob)

    # Load the corresponding private key
    with open(
        os.path.join(os.path.dirname(__file__), "testdata", "key01.priv"),
        encoding="utf-8",
    ) as key_file:
        key_1_priv: str = key_file.read()

    with tempfile.TemporaryDirectory() as signer_tempdir:

        # Create a GPG signer with the first public key
        gpg_signer: GPGSigner = SubprocessGPGSigner(
            gpg_home_path=signer_tempdir,
            private_key_data=key_1_priv,
        )

        try:
            yield JSONSignTestEnv(
                bs=bs,
                gpg_key_inspector=SubprocessGPGKeyInspector(),
                gpg_signer=gpg_signer,
                gpg_signature_verifier=SubprocessGPGSignatureVerifier(),
                public_key_ref=public_key_blob.get_ref(),
            )
        finally:
            pass


def test_jsonsign_and_verify() -> None:
    with get_test_env() as test_env:

        # Bad JSON
        with pytest.raises(json.JSONDecodeError):
            jsonsign.sign_json_str(
                unsigned_json_str="aa",
                gpg_signer=test_env.gpg_signer,
                gpg_key_inspector=SubprocessGPGKeyInspector(),
                fetcher=test_env.bs,
            )

        # Not a dict
        with pytest.raises(Exception, match="JSON string must be an object"):
            jsonsign.sign_json_str(
                unsigned_json_str=json.dumps([1, 2, 3]),
                gpg_signer=test_env.gpg_signer,
                gpg_key_inspector=test_env.gpg_key_inspector,
                fetcher=test_env.bs,
            )

        # Unknown camliVersion
        with pytest.raises(Exception, match="Unknown camliVersion"):
            jsonsign.sign_json_str(
                unsigned_json_str=json.dumps(
                    {
                        "camliVersion": 2,
                    }
                ),
                gpg_signer=test_env.gpg_signer,
                gpg_key_inspector=test_env.gpg_key_inspector,
                fetcher=test_env.bs,
            )

        # Expected camliSigner
        with pytest.raises(Exception, match="Expected camliSigner"):
            jsonsign.sign_json_str(
                unsigned_json_str=json.dumps(
                    {
                        "camliVersion": 1,
                    },
                ),
                gpg_signer=test_env.gpg_signer,
                gpg_key_inspector=test_env.gpg_key_inspector,
                fetcher=test_env.bs,
            )

        # Sucessfully sign
        signed = jsonsign.sign_json_str(
            unsigned_json_str=json.dumps(
                {
                    "camliVersion": 1,
                    "camliSigner": test_env.public_key_ref.to_str(),
                },
            ),
            gpg_signer=test_env.gpg_signer,
            gpg_key_inspector=test_env.gpg_key_inspector,
            fetcher=test_env.bs,
        )
        signed_loaded = json.loads(signed)
        assert signed_loaded["camliVersion"] == 1
        assert (
            signed_loaded["camliSigner"]
            == "sha224-5ec87f8a261ae43b4bd2ef9358424a5f7e27735d3b8dc2dade222a67"
        )
        assert signed.splitlines()[-1].startswith(b',"camliSig":"')

        # Verify the signature
        assert (
            jsonsign.verify_json_signature(
                signed_json_object=signed,
                fetcher=test_env.bs,
                gpg_signature_verifier=test_env.gpg_signature_verifier,
            )
            == True
        )
