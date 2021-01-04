from typing import Protocol

from perkeepy.blob import Ref


class Fetcher(Protocol):
    def fetch(self, ref: Ref) -> bytes:
        ...
