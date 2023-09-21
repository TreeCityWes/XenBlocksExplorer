# XenBlocks Python Explorer and Chart Creator

XenBlocks Python Explorer is a simple tool for exploring XenBlocks blockchain data. It consists of two main Python scripts: `indexer.py` and `chaincheck.py`.

This requires syncnode with a synchronized blockchain.db. The indexer.py will index blockchain.db and create a readable blockchainindex.db. Once blockchainindex.db is populated and has good size, run chaincheck.py from the same directory to gather data. 



## Features

- **Block Search**: Search for blocks by their ID.
- **Account Search**: Search for accounts and get detailed information including total blocks and total super blocks.
- **Last 10 Blocks**: View the last 10 blocks in the blockchain. 
- **Last 5 Super Blocks**: View the last 5 super blocks in the blockchain. 

## Prerequisites

- Python 3.x
- SQLite3

## Installation

Clone this repository to your local machine.

git clone https://github.com/YourUsername/XenBlocks-Python-Explorer.git


## Usage

### Step 1: Build the Index Database

Run the `indexer.py` script to build the index database (`blockchainindex.db`). Make sure you have `blockchain.db` (your blockchain data) available in the same directory.

python indexer.py

The script will continue running to index new blocks as they are added. Wait until the database is built before proceeding to the next step.

### Step 2: Explore the Blockchain

Once the index database is built, you can run the `chaincheck.py` script to explore the blockchain data.

python chaincheck.py


Follow the on-screen prompts to navigate through the blockchain data.

## Contributing

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

The code in this project is licensed under MIT license.
