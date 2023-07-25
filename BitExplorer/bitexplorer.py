import requests
import time
from rich import print as rprint
from rich.panel import Panel
from rich.tree import Tree

# Base URL for the BlockCypher Bitcoin API
API_URL = "https://api.blockcypher.com/v1/btc/main"

# Function to pretty print JSON data in a tree structure
def pretty_print_json(data, tree=Tree("")):
    # Loop through each key-value pair in the data
    for key, value in data.items():
        # If value is a dictionary, create a new subtree for it
        if isinstance(value, dict):
            subtree = Tree(f"[blue]{key}[/blue]")
            pretty_print_json(value, subtree)
            tree.add(subtree)
        # If value is a list, loop through items in the list
        elif isinstance(value, list):
            for i, item in enumerate(value):
                # If item is a dictionary, create a new subtree for it
                if isinstance(item, dict):
                    subtree = Tree(f"[blue]{key} ({i+1})[/blue]")
                    pretty_print_json(item, subtree)
                    tree.add(subtree)
                else:
                    tree.add(f"[green]{key} ({i+1}):[/green] {item}")
        # If value is not a dictionary or list, just print it
        else:
            tree.add(f"[green]{key}:[/green] {value}")
    # Use rich library to print the tree in a pretty way
    rprint(Panel(tree))

# Function to get the height of the latest block
def get_latest_block_height():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data['height']
    else:
        rprint(f'Error {response.status_code}: Could not get latest block height')
        return None

# Function to get overview of a specific block
def get_block_overview(block_height='latest'):
    # If the user wants the latest block, get the height of the latest block
    if block_height == 'latest':
        block_height = get_latest_block_height()
        if block_height is None:
            return
    # Send a GET request to the API
    response = requests.get(f'{API_URL}/blocks/{block_height}')
    if response.status_code != 200:
        rprint(f'Error {response.status_code}: Could not get block {block_height} overview')
    else:
        # Convert the response to JSON and pretty print it
        block_data = response.json()
        pretty_print_json(block_data)

# Function to get overview of a specific transaction
def get_transaction_overview(tx_hash):
    response = requests.get(f'{API_URL}/txs/{tx_hash}')
    if response.status_code != 200:
        rprint(f'Error {response.status_code}: Could not get transaction {tx_hash} overview')
    else:
        transaction_data = response.json()
        pretty_print_json(transaction_data)

# Main function to run the block explorer
def run_bit_explorer():
    while True:
        rprint('BitExplorer - Your Bitcoin Block Explorer')
        rprint('1. Get block overview')
        rprint('2. Get transaction overview')
        rprint('3. Quit')
        user_choice = input('Enter your choice: ')

        # Handle the user's choice
        if user_choice == '1':
            block_height = input("Enter block height (or 'latest' for the latest block): ")
            get_block_overview(block_height)
        elif user_choice == '2':
            tx_hash = input("Enter transaction hash: ")
            get_transaction_overview(tx_hash)
        elif user_choice == '3':
            break
        else:
            rprint('Invalid choice. Please choose a valid option.')

        # Delay to prevent rate limiting
        time.sleep(1)

run_bit_explorer()
