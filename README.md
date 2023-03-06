# farcaster-cli

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/farcaster-cli.svg)](https://pypi.org/project/farcaster-cli/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/badge/chat-telegram-blue)](https://t.me/+aW_ucWeBVUZiNThh)

farcaster-cli is a CLI client for the Farcaster protocol<br></br>

</div>

## Installation

```bash
pip install farcaster-cli
```

or install with [Poetry](https://python-poetry.org/):

```bash
poetry add farcaster-cli
```

## Usage

This client leverages the Warpcast API. [Warpcast](https://warpcast.com/) is one of many Farcaster [clients](https://github.com/a16z/awesome-farcaster#clients). As more APIs are created and hosted by different clients, these will be added to the CLI.

To use the Warpcast API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.

First, save your Farcaster mnemonic or private key to a $MNEMONIC environment variable. Now you can initialize the client, and automatically connect.


```bash
export MNEMONIC = <your custody seed phrase here>
```

```bash
farcaster-cli $MNEMONIC --watch-all
```

This subscribes to all recent casts. If you want only the casts of people you follow, remove `--watch-all`.
You can also include `--skip-existing` to only get new casts after the client starts.