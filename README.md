# simple-blockchain

Simple blockchain "engine" written in Python with CLI interface.
Data is kept on disk in JSON format.

## Running

CLI is wrapped in Docker container to simplify running the project.
To build container run:

  docker build -t bc-cli .

To keep blockchain data between runs, use Docker volumes to mount
file with blockchain data.
Run it from project root dir (or enywhere else, but make sure that "blockchain.db" exists):

docker run -v "$(pwd)/blockchain.db:/app/blockchain.db" --rm -it bc-cli

This will start Docker image with bash. `bc-cli` command will be avaiable:

  blockchain --help

Alternatively `bc-cli` can be called directly like that:

  docker run -v "$(pwd)/blockchain.db:/app/blockchain.db" --rm -it bc-cli blockchain --help

## Tests

  docker run --rm -it bc-cli make tests
