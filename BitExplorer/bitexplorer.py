import requests
import json
import websocket
import threading
import time
from rich.console import Console
from rich.json import JSON

# Constants
API_URL = "https://api.blockcypher.com/v1/btc/main"
WS_URL = "wss://ws.blockchain.info/inv"
MAX_RETRIES = 3
RETRY_SLEEP_TIME = 10

console = Console()
lock = threading.Lock()

def pretty_print(data):
    """
    Pretty prints JSON data using the Rich library.
    """
    with lock:
        console.print(JSON(json.dumps(data, indent=4, sort_keys=True)))

def handle_request_errors(func):
    """
    Decorator to handle errors for requests.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as errh:
            console.print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            console.print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            console.print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            console.print(f"Something went wrong: {err}")
    return wrapper

@handle_request_errors
def get_api_data(url):
    """
    Fetches data from the given API URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_block_overview():
    """
    Fetches and displays an overview of a specified block.
    """
    block_height = input("Enter block height (or 'latest' for the latest block): ")

    if block_height == 'latest':
        data = get_api_data(API_URL)
        if data:
            block_height = data.get("height", None)

    if block_height:
        block_data = get_api_data(f"{API_URL}/blocks/{block_height}")
        if block_data:
            pretty_print(block_data)

def get_transaction_overview():
    """
    Fetches and displays an overview of a specified transaction.
    """
    tx_hash = input("Enter transaction hash: ")
    transaction_data = get_api_data(f"{API_URL}/txs/{tx_hash}")
    if transaction_data:
        pretty_print(transaction_data)

def get_address_overview():
    """
    Fetches and displays an overview of a specified Bitcoin address.
    """
    address = input("Enter Bitcoin address: ")
    address_data = get_api_data(f"{API_URL}/addrs/{address}")
    if address_data:
        pretty_print(address_data)

def live_block_feed():
    """
    Starts a live feed of Bitcoin blocks using WebSocket.
    """
    def on_message(ws, message):
        message_json = json.loads(message)
        if 'x' in message_json:
            pretty_print(message_json['x'])

    def on_error(ws, error):
        console.print(f"Error occurred: {error}")

    def on_close(ws, close_status_code, close_msg):
        console.print(f"### Block feed closed ###\nClose code: {close_status_code}\nClose message: {close_msg}")

    def on_open(ws):
        def run(*args):
            for i in range(MAX_RETRIES):
                try:
                    ws.send(json.dumps({"op":"blocks_sub"}))
                    time.sleep(5)
                    ws.ping("keepalive")
                    break
                except Exception as e:
                    console.print(f"An error occurred: {e}")
                    if i < MAX_RETRIES - 1:
                        time.sleep(RETRY_SLEEP_TIME)
        threading.Thread(target=run).start()

    ws = websocket.WebSocketApp(WS_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

def main():
    while True:
        console.print("Bitcoin Block Explorer")
        console.print("1. Get block overview")
        console.print("2. Get transaction overview")
        console.print("3. Get address overview")
        console.print("4. Live block feed")
        console.print("5. Quit")
        choice = input("Enter your choice: ")
        if choice == '1':
            get_block_overview()
        elif choice == '2':
            get_transaction_overview()
        elif choice == '3':
            get_address_overview()
        elif choice == '4':
            live_block_feed()
        elif choice == '5':
            break
        else:
            console.print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
