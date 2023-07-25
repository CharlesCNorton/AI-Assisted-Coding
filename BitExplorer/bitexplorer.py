import requests
import json
import websocket
import threading
import time
from rich.console import Console
from rich.json import JSON

API_URL = "https://api.blockcypher.com/v1/btc/main"
WS_URL = "wss://ws.blockchain.info/inv"

console = Console()

def pretty_print(data):
    console.print(JSON(json.dumps(data, indent=4, sort_keys=True)))

def get_block_overview():
    block_height = input("Enter block height (or 'latest' for the latest block): ")
    response = requests.get(f"{API_URL}/blocks/{block_height}")
    if response.status_code == 200:
        pretty_print(response.json())
    else:
        console.print(f"Error {response.status_code}: Could not get block {block_height} overview")

def get_transaction_overview():
    tx_hash = input("Enter transaction hash: ")
    response = requests.get(f"{API_URL}/txs/{tx_hash}")
    if response.status_code == 200:
        pretty_print(response.json())
    else:
        console.print(f"Error {response.status_code}: Could not get transaction {tx_hash} overview")

def get_address_overview():
    address = input("Enter Bitcoin address: ")
    response = requests.get(f"{API_URL}/addrs/{address}")
    if response.status_code == 200:
        pretty_print(response.json())
    else:
        console.print(f"Error {response.status_code}: Could not get address {address} overview")

def live_block_feed():
    def on_message(ws, message):
        message_json = json.loads(message)
        if 'x' in message_json:
            console.print(JSON(json.dumps(message_json['x'], indent=4)))

    def on_error(ws, error):
        print(f"Error occurred: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"### Block feed closed ###\nClose code: {close_status_code}\nClose message: {close_msg}")

    def on_open(ws):
        def run(*args):
            while True:
                try:
                    ws.send(json.dumps({"op":"blocks_sub"}))
                    time.sleep(5)  # wait for 5 seconds
                    ws.ping("keepalive")  # send a ping
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break
        threading.Thread(target=run).start()

    ws = websocket.WebSocketApp(WS_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

def main():
    while True:
        print("Bitcoin Block Explorer")
        print("1. Get block overview")
        print("2. Get transaction overview")
        print("3. Get address overview")
        print("4. Live block feed")
        print("5. Quit")
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
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
