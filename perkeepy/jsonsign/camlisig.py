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


class CamliSig:
    @staticmethod
    def from_armored_gpg_signature(armored_gpg_signature: str) -> str:
        # Cleanup before looking for indexes
        armored_gpg_signature = armored_gpg_signature.strip()

        # Look for start and end indexes
        start_index: int = armored_gpg_signature.index("\n\n")
        end_index: int = armored_gpg_signature.index("\n-----")

        # Isolate the sig
        signature: str = armored_gpg_signature[start_index:end_index]

        # Remove newlines
        signature = signature.replace("\n", "")

        return signature

    @staticmethod
    def to_armored_gpg_signature(camli_sig: str) -> str:
        armored_gpg_signature: str = "-----BEGIN PGP SIGNATURE-----\n\n"

        # Extract the CRC
        last_equal_index: int = camli_sig.rindex("=")
        crc: str = camli_sig[last_equal_index:]
        camli_sig = camli_sig[:last_equal_index]

        chunks: list[str] = []
        while camli_sig:
            chunks.append(camli_sig[:64])
            camli_sig = camli_sig[64:]
        chunks.append(crc)

        armored_gpg_signature += "\n".join(chunks)
        armored_gpg_signature += "\n"

        armored_gpg_signature += "-----END PGP SIGNATURE-----\n"
        return armored_gpg_signature
