# Bitcoin Block Explorer

This program allows users to query the Bitcoin blockchain for information about blocks, transactions, and addresses, and to view a live feed of blocks being added to the blockchain. The live block feed utilizes a WebSocket connection for real-time updates. 

## Features

1. Block Overview: Query the blockchain for information about a specific block.
2. Transaction Overview: Query the blockchain for information about a specific transaction.
3. Address Overview: Query the blockchain for information about a specific Bitcoin address.
4. Live Block Feed: View a live feed of blocks being added to the blockchain.

## Requirements

- Python 3.7 or later
- requests library (pip install requests)
- websocket-client library (pip install websocket-client)
- rich library (pip install rich)

## Usage

Run the program in Python and follow the prompts.

    python block_explorer.py

Choose an option from the menu to query for block, transaction, or address information, or to view the live block feed. For the block, transaction, and address queries, you will be prompted to enter a hash or address.