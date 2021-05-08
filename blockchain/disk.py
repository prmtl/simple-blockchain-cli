import contextlib
import json
import typing as T

from blockchain.chain import Blockchain


def save_to_disk(obj: Blockchain, path: str):
    dump = obj.to_dict()
    with open(path, "w") as f:
        json.dump(dump, f)


def load_from_disk(path: str) -> T.Any:
    with open(path, "r") as f:
        data = f.read()
        if data:
            return json.loads(data)
        else:
            return None


@contextlib.contextmanager
def autosave(obj: Blockchain, path):
    yield
    save_to_disk(obj, path)
