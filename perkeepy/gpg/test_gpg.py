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

import os

from .gpg import GPGKeyInspector
from .gpg import GPGSignatureVerifier
from .gpg import GPGSigner


def run_gpg_signer_and_verifier_tests(
    signer: GPGSigner, verifier: GPGSignatureVerifier
) -> None:
    """Test suite for the GPGSigner and GPGSignatureVerifier interfaces"""

    # Load the public key string.
    with open(
        os.path.join(os.path.dirname(__file__), "testdata", "key01.pub"),
        encoding="utf-8",
    ) as public_key_file:
        armored_public_key: str = public_key_file.read()

    # Create a signature, verify that it looks good.
    armored_detached_signature: str = signer.sign_detached_armored(
        fingerprint="FBB89AA320A2806FE497C0492931A67C26F5ABDA",
        data=b"Hello, friends.",
    )
    assert armored_detached_signature.startswith(
        "-----BEGIN PGP SIGNATURE-----",
    )

    # Verify the signature.
    assert (
        verifier.verify_signature(
            data=b"Hello, friends.",
            armored_detached_signature=armored_detached_signature,
            armored_public_key=armored_public_key,
        )
        is True
    )

    # Change the data and verify the signature, this should fail.
    assert (
        verifier.verify_signature(
            data=b"Goodbye, friends.",
            armored_detached_signature=armored_detached_signature,
            armored_public_key=armored_public_key,
        )
        is False
    )


def run_gpg_key_inspector_tests(inspector: GPGKeyInspector) -> None:
    """Test suite for the GPGKeyInspector interface"""

    with open(
        os.path.join(os.path.dirname(__file__), "testdata", "key01.pub"),
        encoding="utf-8",
    ) as key_file:
        key_str: str = key_file.read()
        assert (
            inspector.get_key_fingerprint(armored_key=key_str)
            == "FBB89AA320A2806FE497C0492931A67C26F5ABDA"
        )
