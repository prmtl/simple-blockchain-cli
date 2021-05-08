import sys
import typing as T
from dataclasses import asdict, dataclass

from blockchain.exceptions import MissingDataError


@dataclass
class Block:
    index: int
    previous_hash: str
    data: T.List[str]
    hash: str

    @property
    def size(self):
        return sum(sys.getsizeof(i) for i in self.__dict__.values())

    @classmethod
    def genesis(cls):
        return cls(index=0, previous_hash="", data=[], hash="__genesis__")

    def get_data_by_index(self, index):
        try:
            return self.data[index]
        except IndexError:
            raise MissingDataError

    def to_dict(self):
        return asdict(self)


def is_genesis_block(block):
    return (
        block.index == 0
        and block.hash == "__genesis__"
        and block.data == []
        and block.previous_hash == ""
    )
