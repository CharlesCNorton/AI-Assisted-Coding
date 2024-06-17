
# BlockTalk

BlockTalk is a proof of concept that demonstrates how messages can be stored in the Bitcoin blockchain. This initial version implements the functionality using the Bitcoin testnet.

## Overview

BlockTalk allows users to embed messages into the Bitcoin blockchain by utilizing the OP_RETURN field. This script helps in converting text messages to hexadecimal format, encrypting them, and creating raw Bitcoin transactions to include these messages.

## Features

- Convert text messages to hexadecimal
- Encrypt messages using AES
- Create raw Bitcoin transactions
- Fund and sign transactions
- Test message size for OP_RETURN

## Installation

To install the required dependencies, run the following command in your terminal:

```sh
pip install requests pycryptodome colorama
```

## Usage

### 1. Set Address

Before embedding a message, you need to set the address where unspent transaction outputs (UTXOs) are available. This address will also be used as the change address for any remaining funds after the transaction is completed.

1. **Run the script**:
    Open your terminal and navigate to the directory containing the BlockTalk script, then run:
    ```sh
    python blocktalk.py
    ```

2. **Select option `1` to set the address**:
    The main menu will appear. Enter `1` to select the option for setting the address.
    ```plaintext
    Select an option: 1
    ```

3. **Enter the new self-send/change address**:
    You will be prompted to enter the Bitcoin address that will be used for self-send and change purposes. Ensure that this is a valid Bitcoin testnet address.
    ```plaintext
    Enter the new self-send/change address: YourNewAddressHere
    ```

### 2. Embed a New Message

Once the address is set, you can embed a new message into the blockchain. This involves several steps, from entering your message to broadcasting the transaction.

1. **Run the script**:
    Open your terminal and run the script:
    ```sh
    python blocktalk.py
    ```

2. **Select option `2` to embed a new message**:
    From the main menu, enter `2` to start the process of embedding a new message.
    ```plaintext
    Select an option: 2
    ```

3. **Enter your text message**:
    You will be prompted to enter the text message you want to embed in the blockchain. This message will be converted to hexadecimal and encrypted.
    ```plaintext
    Enter the text message you want to embed: YourMessageHere
    ```

4. **Select the UTXO index to use**:
    The script will list available UTXOs for the set address. You need to select the index of the UTXO you want to use for the transaction.
    ```plaintext
    Select the UTXO index to use: 0
    ```

5. **Follow the generated commands**:
    The script will generate several commands that need to be executed in your Bitcoin-Qt console. Each command corresponds to a step in the transaction process.

    - **Create raw transaction**: This command creates a raw Bitcoin transaction that includes your message in the OP_RETURN output.
        ```plaintext
        createrawtransaction '[{"txid":"your_txid","vout":0}]' '[{"data":"your_hex_message"}, {"your_change_address": 0.0001}]'
        ```

    - **Fund raw transaction**: This command funds the raw transaction created in the previous step. You can specify the fee rate for this transaction.
        ```plaintext
        fundrawtransaction your_raw_transaction_hex
        ```

    - **Sign raw transaction**: This command signs the funded raw transaction with your wallet.
        ```plaintext
        signrawtransactionwithwallet your_funded_raw_transaction_hex
        ```

    - **Send raw transaction**: This command broadcasts the signed raw transaction to the Bitcoin network, embedding your message in the blockchain.
        ```plaintext
        sendrawtransaction your_signed_raw_transaction_hex
        ```

### 3. Test if a Message Can Fit in OP_RETURN

This feature allows you to check if a given message can fit within the size limits of an OP_RETURN output.

1. **Run the script**:
    Open your terminal and run the script:
    ```sh
    python blocktalk.py
    ```

2. **Select option `3` to test if a message can fit in OP_RETURN**:
    From the main menu, enter `3` to start the process of testing your message.
    ```plaintext
    Select an option: 3
    ```

3. **Enter your text message**:
    You will be prompted to enter the text message you want to test. The script will check if the message can fit within the OP_RETURN size limit.
    ```plaintext
    Enter the text message to test: YourMessageHere
    ```

### 4. Exit

To exit the script, select option `4` from the main menu.

```plaintext
Select an option: 4
```

## Example Commands

Here are some example commands to help you understand how to use the script:

1. **Set Address**:
    ```sh
    python blocktalk.py
    # Select option 1 and follow the prompts to set your address
    ```

2. **Embed a New Message**:
    ```sh
    python blocktalk.py
    # Select option 2 and follow the prompts to embed your message
    ```

3. **Test if a Message Can Fit in OP_RETURN**:
    ```sh
    python blocktalk.py
    # Select option 3 and follow the prompts to test your message
    ```

## Future Work

We plan to add the following features in future updates:

- Automated confirmation of the tx.
- Automated confirmatory decryption of the message once the tx is confirmed in the blockchain.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please create a pull request with your proposed changes. Each pull request will be reviewed before being merged.

## License

This project is licensed under the MIT License.

## Author

Created by Charles Norton.
