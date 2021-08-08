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
import tempfile

from . import test_gpg
from .subprocess import SubprocessGPGKeyInspector
from .subprocess import SubprocessGPGSignatureVerifier
from .subprocess import SubprocessGPGSigner


def test_subprocess_gpg_signer_and_verifier() -> None:
    with open(
        os.path.join(os.path.dirname(__file__), "testdata", "key01.priv"),
        "r",
        encoding="utf-8",
    ) as f:
        key_priv: str = f.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_gpg.run_gpg_signer_and_verifier_tests(
            signer=SubprocessGPGSigner(
                gpg_home_path=tmpdir,
                private_key_data=key_priv,
            ),
            verifier=SubprocessGPGSignatureVerifier(),
        )


def test_subprocess_gpg_key_inspector() -> None:
    test_gpg.run_gpg_key_inspector_tests(
        inspector=SubprocessGPGKeyInspector(),
    )
