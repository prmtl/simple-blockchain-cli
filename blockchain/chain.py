import hashlib
import typing as T

from blockchain.block import Block, is_genesis_block
from blockchain.exceptions import MissingBlockError


class Blockchain:
    def __init__(
        self, data_buffer: T.List[str] = None, chain: T.List[Block] = None
    ):
        if chain is None:
            chain = [Block.genesis()]
        self.chain = chain

        if data_buffer is None:
            data_buffer = []
        self.data_buffer = data_buffer

    def __getitem__(self, index: int) -> Block:
        return self.get_block_by_index(index)

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (last: {self.last_block})"

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    @property
    def size(self) -> int:
        """Approx. size in bytes of the chain"""
        return sum(b.size for b in self.chain)

    @property
    def length(self) -> int:
        """Number of blocks"""
        return len(self.chain)

    def add_new_data(self, data: str):
        self.data_buffer.append(data)

    def get_block_by_index(self, index: int) -> Block:
        try:
            return self.chain[index]
        except IndexError:
            raise MissingBlockError

    def get_hash_for_block(self, block: Block) -> str:
        # naive approach to create hashes as only bunch of
        # strings is serializied and not the whole block itself
        hashable_data = "".join(block.data).encode()
        hashable_block = (
            f"{block.index}{block.previous_hash}{hashable_data}".encode()
        )
        return hashlib.sha256(hashable_block).hexdigest()

    def create_new_block(self) -> Block:
        new_index = self.length
        last_block = self.last_block

        new_block = Block(
            index=new_index,
            data=self.data_buffer,
            previous_hash=last_block.hash,
            hash="",
        )

        new_hash = self.get_hash_for_block(new_block)
        new_block.hash = new_hash

        self.chain.append(new_block)
        self.data_buffer = []

        return new_block

    def check(self) -> bool:
        genesis = self.chain[0]

        if not is_genesis_block(genesis):
            return False

        last_block = genesis
        for block in self.chain[1:]:

            block_hash = self.get_hash_for_block(block)
            if block_hash != block.hash:
                return False

            if last_block.hash != block.previous_hash:
                return False

            last_block = block

        return True

    def to_dict(self) -> T.Dict[str, T.Any]:
        return {
            "data_buffer": self.data_buffer,
            "chain": [block.to_dict() for block in self.chain],
        }

    @classmethod
    def from_dict(cls, dump: T.Dict[str, T.Any]) -> "Blockchain":
        chain = [Block(**block) for block in dump["chain"]]
        return cls(data_buffer=dump["data_buffer"], chain=chain)
