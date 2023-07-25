# BitExplorer

BitExplorer is a simple Python-based Bitcoin block explorer. It uses the BlockCypher Bitcoin API to fetch information about blocks and transactions.

## Features
1. Get block overview: Enter a block height or type 'latest' to get information about the latest block.
2. Get transaction overview: Enter a transaction hash to get information about the transaction.

## Usage

Run the BitExplorer with the following command:

python bitexplorer.py

Then, select an option from the menu. You can get an overview of a block, get an overview of a transaction, or quit the program.

## Requirements

- Python 3.6+
- `requests` library
- `rich` library

To install the required libraries, run the following command:

pip install -r requirements.txt

