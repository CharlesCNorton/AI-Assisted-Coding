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
lock = threading.Lock()

def pretty_print(data):
    with lock:
        console.print(JSON(json.dumps(data, indent=4, sort_keys=True)))

def get_block_overview():
    block_height = input("Enter block height (or 'latest' for the latest block): ")

    if block_height == 'latest':
        # Fetch the current block height first
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            block_height = data["height"] # Assuming 'height' is the correct key for block height in the returned data
        except requests.exceptions.HTTPError as errh:
            console.print(f"HTTP Error: {errh}")
            return
        except requests.exceptions.ConnectionError as errc:
            console.print(f"Error Connecting: {errc}")
            return
        except requests.exceptions.Timeout as errt:
            console.print(f"Timeout Error: {errt}")
            return
        except requests.exceptions.RequestException as err:
            console.print(f"Something went wrong: {err}")
            return
    try:
        response = requests.get(f"{API_URL}/blocks/{block_height}")
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.HTTPError as errh:
        console.print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        console.print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        console.print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        console.print(f"Something went wrong: {err}")


def get_transaction_overview():
    tx_hash = input("Enter transaction hash: ")
    try:
        response = requests.get(f"{API_URL}/txs/{tx_hash}")
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.HTTPError as errh:
        console.print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        console.print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        console.print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        console.print(f"Something went wrong: {err}")

def get_address_overview():
    address = input("Enter Bitcoin address: ")
    try:
        response = requests.get(f"{API_URL}/addrs/{address}")
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.HTTPError as errh:
        console.print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        console.print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        console.print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        console.print(f"Something went wrong: {err}")

def live_block_feed():
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
            for i in range(3):  # retry 3 times
                try:
                    ws.send(json.dumps({"op":"blocks_sub"}))
                    time.sleep(5)
                    ws.ping("keepalive")  # send a ping
                    break
                except Exception as e:
                    console.print(f"An error occurred: {e}")
                    if i < 2:  # don't sleep on the last attempt
                        time.sleep(10)
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
