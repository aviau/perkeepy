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

from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.index import BlobMeta
from perkeepy.index import Indexer
from perkeepy.sortedkv import SortedKV

from .key_value_builder import HaveValue
from .key_value_builder import KeyValueBuilder


class SortedKVIndex:
    """
    Indexer implementation on top of the SortedKV interface.

    The following keys & values are populated by receiving blobs and queried
    for search operations:

    * Recent Permanodes
    "recpn|<pgp-keyid>|<reverse-modtime>|<claim-blobref>" -> "<permanode-blobref>"
        where reverse-modtime flips each digit to '9'-<digit> and prepends "rt" (for reverse time)
            "2011-11-27T01:23:45Z" = "rt7988-88-72T98:76:54Z"

    * signer blobref of ascii public key -> gpg key id
    "signerkeyid:sha1-ad87ca5c78bd0ce1195c46f7c98e6025abbaf007" = "2931A67C26F5ABDA"

    * PermanodeOfSignerAttrValue:
    "signerattrvalue|<keyid>|<URLEscape(attr)>|<URLEscape(value)>|<reverse-claimtime>|<claim-blobref>" -> "<permanode>"
        e.g.
    "signerattrvalue|2931A67C26F5ABDA|camliRoot|rootval|"+
        "rt7988-88-71T98:67:60.999876543Z|sha1-bf115940641f1aae2e007edcf36b3b18c17256d9" =
        "sha1-7a14cce982aa73ab519e63050f82e2a2adfcf039"

    * Other:
    "meta:<blobref>" -> "<size>|<mimetype>"
    "have:<blobref>" -> "<size>" (used for enumeration, which doesn't need mime type)

    * For GetOwnerClaims(permanode, signer):
    "claim|<permanode-blobref>|<keyid>|<date>|<claim-blobref>" -> "<URL:type>|<URL:attr>|<URL:value>

    """

    def __init__(self, sorted_kv: SortedKV) -> None:
        self._sorted_kv: SortedKV = sorted_kv
        self._key_value_builder: KeyValueBuilder = KeyValueBuilder()

    def receive_blob(self, blob: Blob) -> None:

        # Stop immediately if we have already indexed this blob.
        have_key: str = self._key_value_builder.get_have_key(blob.get_ref())
        have_value_str: Optional[str] = self._sorted_kv.get(have_key)
        if have_value_str is not None:
            have_value: HaveValue = self._key_value_builder.parse_have_value(
                have_value_str
            )
            if have_value.indexed:
                return

        raise NotImplementedError()

    def get_blob_meta(self, ref: Ref) -> Optional[BlobMeta]:
        raise NotImplementedError()

    @staticmethod
    def _assert_implements_indexer(index: "SortedKVIndex") -> Indexer:
        return index
