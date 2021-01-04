from typing import Protocol
from typing import runtime_checkable


import hashlib


class Hash(Protocol):
    def update(self, bytes: bytes) -> None:
        ...

    def digest(self) -> bytes:
        ...


@runtime_checkable
class Ref(Protocol):
    def get_bytes(self) -> bytes:
        ...

    def get_digest_name(self) -> str:
        ...

    def get_new_hash(self) -> Hash:
        ...

    def equals(self, other: "Ref") -> bool:
        ...


class BaseRef:
    def __init__(self) -> None:
        raise Exception("This is an Abstract Base Class")

    def equals(self, other: object) -> bool:
        if not isinstance(self, Ref) or not isinstance(other, Ref):
            return False

        return (
            self.get_digest_name() == other.get_digest_name()
            and self.get_bytes() == other.get_bytes()
        )


class SHA224Ref(BaseRef):
    def __init__(self, bytes_: bytes) -> None:
        self.bytes = bytes_

    def get_bytes(self) -> bytes:
        return self.bytes

    def get_digest_name(self) -> str:
        return "sha224"

    def get_new_hash(self) -> Hash:
        return hashlib.sha224()


def ref_from_str(ref: str) -> Ref:
    hash_type, hexdigest = ref.split("-")
    if hash_type == "sha224":
        return SHA224Ref(bytes_=bytearray.fromhex(hexdigest))
    else:
        raise Exception(f"Unsupported hash type {hash_type}")
