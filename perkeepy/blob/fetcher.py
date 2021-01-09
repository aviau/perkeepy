from typing import Protocol

from .blob import Blob
from .ref import Ref


class Fetcher(Protocol):
    def fetch_blob(self, ref: Ref) -> Blob:
        ...
