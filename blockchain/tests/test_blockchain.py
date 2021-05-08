import pytest

from blockchain.block import Block, is_genesis_block
from blockchain.chain import Blockchain
from blockchain.exceptions import MissingBlockError, MissingDataError


@pytest.fixture
def simple_blockchain():
    return Blockchain()


@pytest.fixture
def simple_block():
    return Block(
        index=42,
        hash="0000",
        previous_hash="9999",
        data=["Hello World!", "2315667", "rick roll"],
    )


def test_get_block(simple_blockchain):
    index = 0  # genesis

    block = simple_blockchain.get_block_by_index(index)
    assert block.index == index


def test_get_non_existing_block(simple_blockchain):
    index = simple_blockchain.length + 100

    with pytest.raises(MissingBlockError):
        simple_blockchain.get_block_by_index(index)


def test_get_block_data(simple_block):
    index = 0
    assert simple_block.get_data_by_index(index) == simple_block.data[index]


def test_get_non_existing_block_data(simple_block):
    index = len(simple_block.data) + 100
    with pytest.raises(MissingDataError):
        simple_block.get_data_by_index(index)


@pytest.mark.parametrize(
    "block,expected",
    (
        (Block.genesis(), True),
        (Block(index=100, hash="hash", data=[], previous_hash="hash"), False),
    ),
)
def test_is_genesis(block, expected):
    assert is_genesis_block(block) is expected


BLOCKCHAIN_DUMP = {
    "chain": [
        {
            "data": [],
            "hash": "__genesis__",
            "index": 0,
            "previous_hash": "",
        },
        {
            "data": ["data-in-block"],
            "hash": "4bc9739b0f4a30e4d40657e95a6bca8474e97e2c0858f9550e5feb4be72187ce",  # noqa: E501
            "index": 1,
            "previous_hash": "__genesis__",
        },
    ],
    "data_buffer": ["data-in-buffer"],
}


def test_to_dict(simple_blockchain):
    simple_blockchain.add_new_data("data-in-block")
    simple_blockchain.create_new_block()
    simple_blockchain.add_new_data("data-in-buffer")

    assert simple_blockchain.to_dict() == BLOCKCHAIN_DUMP


def test_from_dict():
    blockchain = Blockchain.from_dict(BLOCKCHAIN_DUMP)

    assert blockchain.check()
    assert blockchain.last_block == Block(
        index=1,
        previous_hash="__genesis__",
        data=["data-in-block"],
        hash="4bc9739b0f4a30e4d40657e95a6bca8474e97e2c0858f9550e5feb4be72187ce",  # noqa: E501
    )
    assert blockchain.data_buffer == ["data-in-buffer"]


def test_size(simple_blockchain):
    assert simple_blockchain.length == 1
