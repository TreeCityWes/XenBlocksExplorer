# XenBlocks Blockchain Tools

## Overview

XenBlocks Blockchain Tools is a suite of Python scripts crafted to interact, analyze, and visualize blockchain data. Run SyncNode to create the XenBlocks blockchain.db file. The indexer.py will index blockchain.db and create blockchainindex.db. Chart.py and Explorer.py scripts are designed to work seamlessly with the `blockchainindex.db` database. 

### 1. **indexer.py**
This script reads data from the `blockchain.db` database and constructs an optimized, indexed version of the database, named `blockchainindex.db`. The creation of this indexed serves as the backbone for `chart.py` and `explorer.py`, enabling them to show charts and blockchain data efficiently.

### 2. **chart.py**
Chart.py transforms blockchain data from the `blockchainindex.db` database into charts and graphs. It leverages libraries like `matplotlib` and `seaborn` to generate the following charts:
   - Total Network Blocks Over Time
   - Total Network Super Blocks Over Time
   - Total Network XUNI Blocks Over Time
   - Total Network Distribution (Pie Chart)
   - Blocks by Account
   - XUNI Blocks by Account
   - Superblocks by Account
   - Daily Block Distribution for Account
   - Daily XUNI Block Distribution for Account
   - Daily Super Block Distribution for Account
   - Daily Blocks Distribution

### 3. **explorer.py**
Serving as an block explorer within a python script, this script allows users to delve deep into the data in the `blockchainindex.db` database. It provides a user-friendly interface to:
   - Search for specific blocks by their ID
   - Explore account statistics, including total blocks, XUNI blocks, and super blocks
   - View the latest blocks
   - Discover the top 20 total block holders
   - Uncover the top 20 super block holders
   - Identify the top 20 XUNI block holders

## Usage

### indexer.py
Before leveraging the functionalities of `chart.py` and `explorer.py`, please run `indexer.py` to index the blockchain data. This script creates the `blockchainindex.db` database, which is required for the other scripts.

To run `indexer.py`, execute the script without any additional parameters.

### chart.py
To run `chart.py`, execute the script. It will render a menu enabling you to select from various charting options.

### explorer.py
To run `explorer.py`, execute the script and comply with the on-screen options. 

## Dependencies

The following Python libraries are essential for all scripts:
- `sqlite3`: Essential for connecting to and querying the indexed database.
- `pandas`: Crucial for data manipulation and analysis.
- `matplotlib` and `seaborn`: Paramount for creating diverse charts and visualizations.
- `tabulate`: Vital for rendering tabular data in a readable format.
- `colorama`: Integral for enhancing the command-line interface with colors.

## Acknowledgments

Developed with precision by TreeCityWes.eth. If you find these tools useful, please consider expressing your support by buying a coffee on HashHead.io.
