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

from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.blobserver import Storage
from perkeepy.blobserver.memory import MemoryBlobServer

from .gpg import GPGSignerFactory
from .gpg import SubprocessGPGSignerFactory
from .jsonsign import CamliSig
from .jsonsign import sign_json_str


def test_camlisig() -> None:
    armored_signature: str = """
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9Y
FzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9C
vXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQ
BStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZ
ilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9Y
fbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE=
=aSCK
-----END PGP SIGNATURE-----
"""
    expected_camlisig: str = "iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9YFzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9CvXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQBStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9YfbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE==aSCK"
    expected_restored: str = """-----BEGIN PGP SIGNATURE-----

iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9Y
FzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9C
vXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQ
BStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZ
ilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9Y
fbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE=
=aSCK
-----END PGP SIGNATURE----
"""

    assert (
        CamliSig.from_armored_gpg_signature(armored_signature)
        == expected_camlisig
    )

    assert (
        CamliSig.to_armored_gpg_signature(expected_camlisig)
        == expected_restored
    )


@dataclass
class JSONSignTestEnv:
    bs: Storage
    signer_factory: GPGSignerFactory
    private_key_fingerprint: str
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
        signer_factory: GPGSignerFactory = SubprocessGPGSignerFactory(
            gpg_home_path=signer_tempdir,
            private_key_data=key_1_priv,
        )

        try:
            yield JSONSignTestEnv(
                bs=bs,
                signer_factory=signer_factory,
                private_key_fingerprint="FBB89AA320A2806FE497C0492931A67C26F5ABDA",
                public_key_ref=public_key_blob.get_ref(),
            )
        finally:
            pass


def test_sign_bad_input() -> None:
    with get_test_env() as test_env:

        # Bad JSON
        with pytest.raises(json.JSONDecodeError):
            sign_json_str(
                unsigned_json_str="aa",
                gpg_signer_factory=test_env.signer_factory,
                fetcher=test_env.bs,
            )

        # Not a dict
        with pytest.raises(Exception, match="JSON string must be an object"):
            sign_json_str(
                unsigned_json_str=json.dumps([1, 2, 3]),
                gpg_signer_factory=test_env.signer_factory,
                fetcher=test_env.bs,
            )

        # Unknown camliVersion
        with pytest.raises(Exception, match="Unknown camliVersion"):
            sign_json_str(
                unsigned_json_str=json.dumps(
                    {
                        "camliVersion": 2,
                    }
                ),
                gpg_signer_factory=test_env.signer_factory,
                fetcher=test_env.bs,
            )

        # Expected camliSigner
        with pytest.raises(Exception, match="Expected camliSigner"):
            sign_json_str(
                unsigned_json_str=json.dumps(
                    {
                        "camliVersion": 1,
                    },
                ),
                gpg_signer_factory=test_env.signer_factory,
                fetcher=test_env.bs,
            )

        signed = sign_json_str(
            unsigned_json_str=json.dumps(
                {
                    "camliVersion": 1,
                    "camliSigner": test_env.public_key_ref.to_str(),
                },
            ),
            gpg_signer_factory=test_env.signer_factory,
            fetcher=test_env.bs,
        )
        signed_loaded = json.loads(signed)
        assert signed_loaded["camliVersion"] == 1
        assert (
            signed_loaded["camliSigner"]
            == "sha224-5ec87f8a261ae43b4bd2ef9358424a5f7e27735d3b8dc2dade222a67"
        )
