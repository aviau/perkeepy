from typing import Callable
from typing import Optional

from .ref import Hash
from .ref import Ref

ReadAll = Callable[[], bytes]


class Blob:
    def __init__(self, ref: Ref, readall: ReadAll) -> None:
        self._ref: Ref = ref
        self.readall: ReadAll = readall
        self._bytes: Optional[bytes] = None

    def get_ref(self) -> Ref:
        return self._ref

    def get_bytes(self) -> bytes:
        if self._bytes is None:
            self._bytes = self.readall()
        return self._bytes

    def is_utf8(self) -> bool:
        try:
            self.get_bytes().decode("utf-8")
        except UnicodeDecodeError:
            return False
        return True

    def is_valid(self) -> bool:
        hash_: Hash = self._ref.get_new_hash()
        hash_.update(self.get_bytes())
        return hash_.hexdigest() == self._ref.get_hexdigest()
