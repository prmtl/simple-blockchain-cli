import click

from blockchain.chain import Blockchain
from blockchain.disk import autosave, load_from_disk
from blockchain.exceptions import MissingBlockError, MissingDataError


@click.group()
@click.option(
    "--path",
    default="blockchain.db",
    help="where the blockchain is stored",
    type=click.Path(resolve_path=True),
)
@click.version_option("1.0")
@click.pass_context
def main(ctx, path):
    """Simple blockchain implementation with CLI interface"""
    dump = load_from_disk(path)
    if dump:
        blockchain = Blockchain.from_dict(dump)
    else:
        blockchain = Blockchain()
    ctx.obj = {"blockchain": blockchain, "path": path}


@click.group()
def chain():
    """Manipulate whole blockchain"""
    pass


@chain.command()
@click.pass_context
def stats(ctx):
    """Get blockchain statistics"""
    blockchain = ctx.obj["blockchain"]
    click.echo(
        f"""
Number of blocks: {blockchain.length}
Size in bytes: {blockchain.size}
"""
    )


@chain.command()
@click.pass_context
def integrity(ctx):
    """Check blockchain integrity"""
    blockchain = ctx.obj["blockchain"]
    click.echo("ok" if blockchain.check() else "not ok")


@click.group()
def data():
    """Manipulate data"""
    pass


@data.command("add")
@click.argument("data")
@click.pass_context
def add_data(ctx, data):
    """Add new datta elements to the buffer"""
    blockchain = ctx.obj["blockchain"]
    path = ctx.obj["path"]
    with autosave(blockchain, path):
        blockchain.add_new_data(data)


@data.command("get")
@click.argument("block_index", type=click.INT)
@click.argument("data_index", type=click.INT)
@click.pass_context
def get_data(
    ctx,
    block_index,
    data_index,
):
    """Get specific element of specific block"""
    blockchain = ctx.obj["blockchain"]
    try:
        block = blockchain.get_block_by_index(block_index)
        data = block.get_data_by_index(data_index)
        click.echo(data)
    except MissingBlockError:
        raise click.UsageError(f"Cannot find block with index {block_index}")
    except MissingDataError:
        raise click.UsageError(
            f"Cannot find data with index {data_index} for block {block_index}"
        )


@click.group()
def block():
    """Manipulate blocks"""
    pass


@block.command("new")
@click.pass_context
def new_block(ctx):
    """Generate new block from buffered data"""
    blockchain = ctx.obj["blockchain"]
    path = ctx.obj["path"]
    with autosave(blockchain, path):
        block = blockchain.create_new_block()
    click.echo(block)


@block.command("get")
@click.argument("index", type=click.INT)
@click.pass_context
def get_block(ctx, index):
    """Get block by its index"""
    blockchain = ctx.obj["blockchain"]
    try:
        block = blockchain.get_block_by_index(index)
        click.echo(block)
    except MissingBlockError:
        raise click.UsageError(f"Cannot find block with index {index}")


main.add_command(block)
main.add_command(data)
main.add_command(chain)


if __name__ == "__main__":
    main()
