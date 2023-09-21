## XenBlocks Python Explorer and Chart Creator

XenBlocks Python Explorer is a comprehensive tool for exploring and visualizing XenBlocks blockchain data. It consists of three main Python scripts: `indexer.py`, `chaincheck.py`, and `chart.py`.

This requires syncnode with a synchronized `blockchain.db`. The `indexer.py` will index `blockchain.db` and create a readable `blockchainindex.db`. Once `blockchainindex.db` is populated and has a good size, run `chaincheck.py` and `chart.py` from the same directory to gather and visualize data.

## Features

- **Block Search**: Search for blocks by their ID.
- **Account Search**: Search for accounts and get detailed information including total blocks and total super blocks.
- **Last 10 Blocks**: View the last 10 blocks in the blockchain.
- **Last 5 Super Blocks**: View the last 5 super blocks in the blockchain.

- NEW: **Data Visualization**: Visualize blockchain data with different charts with charts.py

## Prerequisites

- Python 3.x
- SQLite3
- pandas
- matplotlib

## Installation

Clone this repository to your local machine.

```sh
git clone https://github.com/YourUsername/XenBlocks-Python-Explorer.git
```

## Usage

### Step 1: Build the Index Database

Run the `indexer.py` script to build the index database (`blockchainindex.db`). Make sure you have `blockchain.db` (your blockchain data) available in the same directory.

```sh
python indexer.py
```

The script will continue running to index new blocks as they are added. Wait until the database is built before proceeding to the next step.

### Step 2: Explore the Blockchain with chaincheck.py

`chaincheck.py` allows you to explore the blockchain by searching for blocks by their ID, searching for accounts, viewing the last 10 blocks, and viewing the last 5 super blocks.

```sh
python chaincheck.py
```

Follow the on-screen prompts to navigate through the blockchain data.

### Step 3: Visualize Blockchain Data with chart.py

`chart.py` allows you to visualize the blockchain data with different charts, including total network blocks over time, total network super blocks over time, total blocks by account, and total superblocks by account.

```sh
python chart.py
```

Follow the on-screen prompts to select and display charts.

## Contributing

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

The code in this project is licensed under MIT license.
```
