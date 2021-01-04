from typing import Protocol
from typing import runtime_checkable

import abc


import hashlib


class Hash(Protocol):
    def update(self, bytes: bytes) -> None:
        ...

    def digest(self) -> bytes:
        ...


class Ref(abc.ABC):
    def __init__(self, bytes_: bytes) -> None:
        self.bytes = bytes_

    def get_bytes(self) -> bytes:
        return self.bytes

    @abc.abstractclassmethod
    def get_digest_name(self) -> str:
        ...

    @abc.abstractclassmethod
    def get_new_hash(self) -> Hash:
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ref):
            return False
        return (
            self.get_digest_name() == other.get_digest_name()
            and self.get_bytes() == other.get_bytes()
        )

    @staticmethod
    def from_str(ref: str) -> "Ref":
        hash_type, hexdigest = ref.split("-")
        if hash_type == "sha224":
            return SHA224Ref(bytes_=bytearray.fromhex(hexdigest))
        else:
            raise Exception(f"Unsupported hash type {hash_type}")


class SHA224Ref(Ref):
    def get_digest_name(self) -> str:
        return "sha224"

    def get_new_hash(self) -> Hash:
        return hashlib.sha224()
