class BlockchainError(Exception):
    pass


class MissingBlockError(BlockchainError):
    pass


class MissingDataError(BlockchainError):
    pass


class IntegrityError(BlockchainError):
    pass
