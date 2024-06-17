import requests
import json
from colorama import Fore, Style, init
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import binascii
import re

init(autoreset=True)

BASE_URL = 'https://blockstream.info/testnet/api'
SELF_SEND_ADDRESS = None

def convert_text_to_hex(text_message):
    try:
        return text_message.encode('utf-8').hex()
    except Exception as e:
        print(Fore.RED + f"Error converting text to hex: {str(e)}")
        return None

def encrypt_message(text_message, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        padded_message = pad(text_message.encode('utf-8'), AES.block_size)
        ct_bytes = cipher.encrypt(padded_message)
        iv = binascii.hexlify(cipher.iv).decode('utf-8')
        encrypted_message = binascii.hexlify(ct_bytes).decode('utf-8')
        return iv + encrypted_message
    except Exception as e:
        print(Fore.RED + f"Error encrypting message: {str(e)}")
        return None

def create_raw_transaction(txid, vout, hex_message, change_address):
    try:
        return f"createrawtransaction '[{{\"txid\":\"{txid}\",\"vout\":{vout}}}]' '[{{\"data\":\"{hex_message}\"}}, {{\"{change_address}\": 0.0001}}]'"
    except Exception as e:
        print(Fore.RED + f"Error creating raw transaction: {str(e)}")
        return None

def fund_raw_transaction(raw_transaction_hex, fee_rate=None):
    try:
        if fee_rate:
            return f"fundrawtransaction {raw_transaction_hex} '{{\"feeRate\": {fee_rate}}}'"
        return f"fundrawtransaction {raw_transaction_hex}"
    except Exception as e:
        print(Fore.RED + f"Error creating fundrawtransaction command: {str(e)}")
        return None

def sign_raw_transaction(funded_raw_transaction_hex):
    try:
        return f"signrawtransactionwithwallet {funded_raw_transaction_hex}"
    except Exception as e:
        print(Fore.RED + f"Error creating signrawtransactionwithwallet command: {str(e)}")
        return None

def send_raw_transaction(signed_raw_transaction_hex):
    try:
        return f"sendrawtransaction {signed_raw_transaction_hex}"
    except Exception as e:
        print(Fore.RED + f"Error creating sendrawtransaction command: {str(e)}")
        return None

def get_input(prompt, validator):
    while True:
        try:
            value = input(prompt)
            if validator(value):
                return value
            else:
                print(Fore.RED + "Invalid input. Please try again.")
        except Exception as e:
            print(Fore.RED + f"Error getting input: {str(e)}")

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
    except Exception as e:
        print(Fore.RED + f"Error validating hex: {str(e)}")
        return False

def is_valid_txid(txid):
    try:
        return len(txid) == 64 and is_hex(txid)
    except Exception as e:
        print(Fore.RED + f"Error validating txid: {str(e)}")
        return False

def is_valid_vout(vout):
    try:
        return vout.isdigit() and int(vout) >= 0
    except Exception as e:
        print(Fore.RED + f"Error validating vout: {str(e)}")
        return False

def is_valid_address(address):
    try:
        if re.match(r'^(tb1|[2mn])[a-zA-HJ-NP-Z0-9]{25,39}$', address):
            return True
        return False
    except Exception as e:
        print(Fore.RED + f"Error validating address: {str(e)}")
        return False

def get_unspent_outputs(address):
    try:
        url = f"{BASE_URL}/address/{address}/utxo"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(Fore.RED + f"Error fetching unspent outputs: {str(e)}")
        return []

def can_fit_in_op_return(message):
    try:
        key = get_random_bytes(16)
        encrypted_message = encrypt_message(message, key)
        if len(encrypted_message) > 160:
            return False, 0
        tx_size_bytes = 250 + len(encrypted_message) // 2
        return True, tx_size_bytes
    except Exception as e:
        print(Fore.RED + f"Error checking if message can fit in OP_RETURN: {str(e)}")
        return False, 0

def main_menu():
    print(Fore.CYAN + Style.BRIGHT + "\nBlockTalk - Bitcoin OP_RETURN Embedding Script" + Style.RESET_ALL)
    menu_options = [
        "1. Set address",
        "2. Embed a new message",
        "3. Test if a message can fit in OP_RETURN",
        "4. Exit"
    ]
    for option in menu_options:
        print(Fore.YELLOW + Style.BRIGHT + option + Style.RESET_ALL)

def main():
    global SELF_SEND_ADDRESS
    try:
        key = get_random_bytes(16)
        print(Fore.GREEN + f"Generated 128-bit key for encryption (keep this safe for decryption): {binascii.hexlify(key).decode('utf-8')}")
    except Exception as e:
        print(Fore.RED + f"Error generating encryption key: {str(e)}")
        return

    while True:
        try:
            main_menu()
            choice = input(Fore.GREEN + "Select an option: ")

            if choice == '1':
                new_address = get_input(Fore.CYAN + "Enter the new self-send/change address: ", is_valid_address)
                SELF_SEND_ADDRESS = new_address
                print(Fore.GREEN + f"Self-send/change address updated to: {SELF_SEND_ADDRESS}")

            elif choice == '2':
                if SELF_SEND_ADDRESS is None:
                    print(Fore.RED + "Error: Self-send address is not set. Please set the address first.")
                    continue

                text_message = get_input(Fore.CYAN + "Enter the text message you want to embed: ", lambda s: len(s) > 0)

                hex_message = convert_text_to_hex(text_message)
                if hex_message is None or len(hex_message) > 64:
                    print(Fore.RED + "Error: The hex-encoded message exceeds 64 characters. Please enter a shorter message.")
                    continue

                address = SELF_SEND_ADDRESS
                utxos = get_unspent_outputs(address)
                if not utxos:
                    print(Fore.RED + "Error: No unspent outputs found for the address.")
                    continue

                print(Fore.GREEN + "Available UTXOs:")
                for idx, utxo in enumerate(utxos):
                    print(Fore.YELLOW + f"{idx}: txid: {utxo['txid']}, vout: {utxo['vout']}, value: {utxo['value']} satoshis")

                utxo_index = get_input(Fore.CYAN + "Select the UTXO index to use: ", lambda s: s.isdigit() and int(s) >= 0 and int(s) < len(utxos))
                selected_utxo = utxos[int(utxo_index)]

                txid = selected_utxo['txid']
                vout = selected_utxo['vout']

                encrypted_message = encrypt_message(text_message, key)
                if encrypted_message is None or len(encrypted_message) > 160:
                    print(Fore.RED + "Error: The encrypted hex-encoded message exceeds 80 bytes. Please enter a shorter message.")
                    continue

                raw_transaction_command = create_raw_transaction(txid, vout, encrypted_message, SELF_SEND_ADDRESS)
                if raw_transaction_command is None:
                    continue

                print(Fore.MAGENTA + "\nStep 1: Run the following command in your Bitcoin-Qt console to create the raw transaction:")
                print(Fore.WHITE + raw_transaction_command)

                funded_raw_transaction_hex = get_input(Fore.CYAN + "\nStep 2: Enter the output from the 'createrawtransaction' command: ", is_hex)
                fee_rate = get_input(Fore.CYAN + "Enter the fee rate (in BTC per kB) to use for funding the transaction: ", lambda s: s.replace('.', '', 1).isdigit() and float(s) > 0)
                fund_transaction_command = fund_raw_transaction(funded_raw_transaction_hex, fee_rate)
                if fund_transaction_command is None:
                    continue

                print(Fore.MAGENTA + "\nStep 3: Run the following command in your Bitcoin-Qt console to fund the raw transaction:")
                print(Fore.WHITE + fund_transaction_command)

                funded_raw_transaction_output = get_input(Fore.CYAN + "\nStep 4: Enter the JSON output from the 'fundrawtransaction' command: ", lambda s: s.strip().startswith('{') and s.strip().endswith('}'))
                try:
                    funded_raw_transaction = json.loads(funded_raw_transaction_output)
                    funded_raw_transaction_hex = funded_raw_transaction['hex']
                except (KeyError, json.JSONDecodeError) as e:
                    print(Fore.RED + f"Error parsing JSON: {str(e)}")
                    continue

                sign_transaction_command = sign_raw_transaction(funded_raw_transaction_hex)
                if sign_transaction_command is None:
                    continue

                print(Fore.MAGENTA + "\nStep 5: Run the following command in your Bitcoin-Qt console to sign the raw transaction:")
                print(Fore.WHITE + sign_transaction_command)

                signed_raw_transaction_output = get_input(Fore.CYAN + "\nStep 6: Enter the JSON output from the 'signrawtransactionwithwallet' command: ", lambda s: s.strip().startswith('{') and s.strip().endswith('}'))
                try:
                    signed_raw_transaction = json.loads(signed_raw_transaction_output)
                    signed_raw_transaction_hex = signed_raw_transaction['hex']
                except (KeyError, json.JSONDecodeError) as e:
                    print(Fore.RED + f"Error parsing JSON: {str(e)}")
                    continue

                send_transaction_command = send_raw_transaction(signed_raw_transaction_hex)
                if send_transaction_command is None:
                    continue

                print(Fore.MAGENTA + "\nStep 7: Run the following command in your Bitcoin-Qt console to broadcast the transaction:")
                print(Fore.WHITE + send_transaction_command)

            elif choice == '3':
                test_message = get_input(Fore.CYAN + "Enter the text message to test: ", lambda s: len(s) > 0)
                fits, tx_size_bytes = can_fit_in_op_return(test_message)
                if fits:
                    print(Fore.GREEN + "The message can fit in an OP_RETURN output.")
                else:
                    print(Fore.RED + "The message cannot fit in an OP_RETURN output. Please enter a shorter message.")

            elif choice == '4':
                print(Fore.GREEN + "Exiting the script. Goodbye!")
                break

            else:
                print(Fore.RED + "Invalid choice. Please select a valid option.")
        except Exception as e:
            if "Fee estimation failed. Fallbackfee is disabled" in str(e):
                print(Fore.RED + "Error: Fee estimation failed. Fallbackfee is disabled. Please enable fallback fee in Bitcoin-Qt by adding 'fallbackfee=<amount>' to your bitcoin.conf file and restarting the client.")
            else:
                print(Fore.RED + f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
