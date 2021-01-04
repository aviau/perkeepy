from typing import Protocol

from .ref import Ref


class Fetcher(Protocol):
    def fetch(self, ref: Ref) -> bytes:
        ...
