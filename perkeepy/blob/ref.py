from typing import Protocol
from typing import runtime_checkable

import abc
import hashlib


class Hash(Protocol):
    def update(self, bytes: bytes) -> None:
        ...

    def digest(self) -> bytes:
        ...

    def hexdigest(self) -> str:
        ...


class DigestAlgorithm(Protocol):
    def get_new_hash(self) -> Hash:
        ...

    def get_digest_name(self) -> str:
        ...


class Ref(abc.ABC):
    def __init__(self, bytes_: bytes) -> None:
        self.bytes = bytes_

    @abc.abstractclassmethod
    def get_digest_algorithm(self) -> DigestAlgorithm:
        ...

    def get_new_hash(self) -> Hash:
        return self.get_digest_algorithm().get_new_hash()

    def get_bytes(self) -> bytes:
        return self.bytes

    def get_hexdigest(self) -> str:
        return self.get_bytes().hex()

    def get_digest_name(self) -> str:
        return self.get_digest_algorithm().get_digest_name()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ref):
            return False
        return (
            self.get_digest_name() == other.get_digest_name()
            and self.get_bytes() == other.get_bytes()
        )

    def to_str(self) -> str:
        digest_name: str = self.get_digest_name()
        hexdigest: str = self.get_hexdigest()
        return f"{digest_name}-{hexdigest}"

    @staticmethod
    def get_currently_recommended_digest_algorithm() -> DigestAlgorithm:
        return SHA224()

    @staticmethod
    def from_ref_str(ref: str) -> "Ref":
        """Creates a ref from a 'digalg-blobref' string"""

        hash_type, hexdigest = ref.split("-")
        if hash_type == "sha224":
            return SHA224Ref(bytes_=bytearray.fromhex(hexdigest))
        else:
            raise Exception(f"Unsupported hash type {hash_type}")

    @classmethod
    def from_contents_str(cls, data: str) -> "Ref":
        return cls.from_contents_bytes(data.encode("utf-8"))

    @classmethod
    def from_contents_bytes(cls, data: bytes) -> "Ref":
        """Returns a blobref using the currently recommended hash function"""
        digest_alg = cls.get_currently_recommended_digest_algorithm()
        hasher = digest_alg.get_new_hash()
        hasher.update(data)
        return Ref.from_ref_str(
            f"{digest_alg.get_digest_name()}-{hasher.hexdigest()}"
        )


class SHA224:
    @staticmethod
    def get_digest_name() -> str:
        return "sha224"

    @staticmethod
    def get_new_hash() -> Hash:
        return hashlib.sha224()

    @staticmethod
    def _assert_implements_digest_algorithm(sha224: "SHA224") -> None:
        f: DigestAlgorithm = sha224


class SHA224Ref(Ref):
    def get_digest_algorithm(self) -> DigestAlgorithm:
        return SHA224()
