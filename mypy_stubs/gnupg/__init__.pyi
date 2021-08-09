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

from typing import Optional
from typing import TypedDict
from typing import Union
from typing import Literal


class GPGKey(TypedDict):
    fingerprint: str

class Sign:
    data: bytes

class ImportResult:
    count: int
    fingerprints: list[str]
    stderr: bytes

class VerificationResult:
    fingerprint: Optional[str]
    valid: bool

class GPG:

    def __init__(
        self,
        gnupghome: Optional[str] = None,
        use_agent: bool = False,
        keyring: Optional[str] = None,
    ) -> None:
        ...

    def list_keys(
        self,
        secret: bool = False
    ) -> list[GPGKey]:
        ...

    def import_keys(
        self,
        key_data: str,
    ) -> ImportResult:
        ...

    def sign(
        self,
        message: bytes,
        keyid: Optional[str],
        detach: bool = False,
        binary: bool = False,
    ) -> Sign:
        ...

    def verify_data(
        self,
        sig_filename: str,
        data: bytes,
    ) -> VerificationResult:
        ...


    def trust_keys(
        self,
        fingerprints: list[str],
        trustlevel: Union[
            Literal['TRUST_NEVER'],
            Literal['TRUST_MARGINAL'],
            Literal['TRUST_FULLY'],
            Literal['TRUST_ULTIMATE'],
        ],
    ) -> None:
        ...
