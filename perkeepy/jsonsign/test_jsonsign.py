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
from perkeepy.gpg.pgpy import PGPYGPGKeyInspector
from perkeepy.gpg.pgpy import PGPYGPGSignatureVerifier
from perkeepy.gpg.pgpy import PGPYGPGSigner


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

    yield JSONSignTestEnv(
        bs=bs,
        gpg_key_inspector=PGPYGPGKeyInspector(),
        gpg_signer=PGPYGPGSigner(armored_private_keys=[key_1_priv]),
        gpg_signature_verifier=PGPYGPGSignatureVerifier(),
        public_key_ref=public_key_blob.get_ref(),
    )


def test_jsonsign_and_verify() -> None:
    with get_test_env() as test_env:

        # Bad JSON
        with pytest.raises(json.JSONDecodeError):
            jsonsign.sign_json_str(
                unsigned_json_str="aa",
                gpg_signer=test_env.gpg_signer,
                gpg_key_inspector=test_env.gpg_key_inspector,
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


def test_signature_from_go_implementation() -> None:
    public_key_blob_str: str = """-----BEGIN PGP PUBLIC KEY BLOCK-----

xsBNBGAHnVgBCADerM1lth1pgduiuOOhu6vFxnt5PoZbH+PRB/iJflgmBrswryPr
5oyalJrv6k5mnbgHumz46OaZFW6oaOpO5xLHVvcNuPjJceyPV2IeSz5PLm1SAlge
gSgCWGpAdcNsj+FIdftd7d1/mL42S9DQ4xByrkTkY06mAnci8oy5mplNHGa6nnib
sm5iWPcGX6Rvz3YCkm/kdKyYhBzoBJFUh4r13LxCiF6aefHN1NXvJQsleAPjUsTl
aouhfumRpKnEol/tJJuys/LnCC+tkU1D6qiAI+ALnCzWKhbCgfbt2InimxEC3YQZ
MfoyWlkBlLxT9rDBf8rkXuF7qXNKiPA4w571ABEBAAE=
=4ilV
-----END PGP PUBLIC KEY BLOCK-----
"""
    public_key_blob = Blob.from_contents_str(public_key_blob_str)
    assert (
        public_key_blob.get_ref().to_str()
        == "sha224-755426de872509a10461cb908a2ab8012df9f63706aaa6994f0ad895"
    )

    signed_json_object: bytes = b"""{"camliVersion": 1,
  "camliSigner": "sha224-755426de872509a10461cb908a2ab8012df9f63706aaa6994f0ad895",
  "camliType": "permanode",
  "claimDate": "2021-08-08T21:49:57.225132035Z",
  "random": "wNqQLPEH/aq/lGYN2D43EV1UEu8="
,"camliSig":"wsBcBAABCAAQBQJhEFGFCRAwgMgbA5XuOQAAMDcIADiyzvzCAhjcwbmLuSHicMihrwHRC+4S/GxERNiqf+5nW/lCbwUa9quvFadukc0+OK18IiqYPXnPe9OAxgH29Yds60WtzVATOrSqarmWuy48gZekQ8m+r3qRMs4fbu0PgUSnz3bPYeNwx+4NncoO1lwM9o9brA9HRHkDmuJ1jYWTuuDDsC5NbuHxwsLD1ATF9JH0S/NWNFpl0El+9RfsbRg7FdC3O37Dqu7nO9giM5XQDViNiLT/gKStck28COdhyHJvB+l0egqir5oQJ1wODErcOdVpS7k7bAfS9+I1WBuLs1++bVk8beVBp4GsJGKRgor1o+7FFFqDUMEDIPyE43o==c+i6"}"""

    with get_test_env() as test_env:
        # Load the public key
        test_env.bs.receive_blob(public_key_blob)

        # Verify the signature
        assert (
            jsonsign.verify_json_signature(
                signed_json_object=signed_json_object,
                fetcher=test_env.bs,
                gpg_signature_verifier=test_env.gpg_signature_verifier,
            )
            is True
        )
