BlockTalk

BlockTalk is a proof of concept that demonstrates how messages can be stored in the Bitcoin blockchain. This initial version implements the functionality using the Bitcoin testnet.

Overview

BlockTalk allows users to embed messages into the Bitcoin blockchain by utilizing the OP_RETURN field. This script helps in converting text messages to hexadecimal format, encrypting them, and creating raw Bitcoin transactions to include these messages.

Features

- Convert text messages to hexadecimal
- Encrypt messages using AES (Advanced Encryption Standard)
- Create raw Bitcoin transactions
- Fund and sign transactions
- Test message size for OP_RETURN

Installation

To install the required dependencies, run the following command in your terminal:

pip install requests pycryptodome colorama

Usage

1. Set Address

Before embedding a message, you need to set the address where unspent transaction outputs (UTXOs) are available. This address will also be used as the change address for any remaining funds after the transaction is completed.

1. Run the script:
    Open your terminal and navigate to the directory containing the BlockTalk script, then run:

    python blocktalk.py

2. Select option 1 to set the address:
    The main menu will appear. Enter 1 to select the option for setting the address.

3. Enter the new change address:
    You will be prompted to enter the Bitcoin address that will be used for change purposes. Ensure that this is a valid Bitcoin testnet address.

    Enter the new change address: YourNewAddressHere

2. Embed a New Message

Once the address is set, you can embed a new message into the blockchain. This involves several steps, from entering your message to broadcasting the transaction.

1. Run the script:
    Open your terminal and run the script:

    python blocktalk.py

2. Select option 2 to embed a new message:
    From the main menu, enter 2 to start the process of embedding a new message.

3. Enter your text message:
    You will be prompted to enter the text message you want to embed in the blockchain. This message will be converted to hexadecimal and encrypted using AES (Advanced Encryption Standard). AES is a symmetric encryption algorithm widely used for its security and efficiency. The script uses AES in CBC (Cipher Block Chaining) mode with a randomly generated initialization vector (IV) for each encryption.

    Enter the text message you want to embed: YourMessageHere

4. Select the UTXO index to use:
    The script will list available UTXOs for the set address. You need to select the index of the UTXO you want to use for the transaction. UTXOs are unspent transaction outputs that can be used as inputs in new transactions.

    Select the UTXO index to use: 0

5. Follow the generated commands:
    The script will generate several commands that need to be executed in your Bitcoin-Qt console. Each command corresponds to a step in the transaction process:

    - Create raw transaction: This command creates a raw Bitcoin transaction that includes your message in the OP_RETURN output.

        createrawtransaction '[{"txid":"your_txid","vout":0}]' '[{"data":"your_hex_message"}, {"your_change_address": 0.0001}]'

        - Explanation: This command constructs a raw transaction. The txid and vout refer to the selected UTXO, the data field includes your encrypted message, and the change_address receives any remaining funds.

    - Fund raw transaction: This command funds the raw transaction created in the previous step. You can specify the fee rate for this transaction.

        fundrawtransaction your_raw_transaction_hex

        - Explanation: This command ensures that the transaction has enough funds to cover the output values and transaction fees. The feeRate parameter allows you to specify the fee per kilobyte.

    - Sign raw transaction: This command signs the funded raw transaction with your wallet.

        signrawtransactionwithwallet your_funded_raw_transaction_hex

        - Explanation: This command adds the necessary cryptographic signatures to the transaction to authorize the spending of the UTXOs.

    - Send raw transaction: This command broadcasts the signed raw transaction to the Bitcoin network, embedding your message in the blockchain.

        sendrawtransaction your_signed_raw_transaction_hex

        - Explanation: This command sends the signed transaction to the network, where it will be included in a block by miners.

3. Test if a Message Can Fit in OP_RETURN

This feature allows you to check if a given message can fit within the size limits of an OP_RETURN output.

1. Run the script:
    Open your terminal and run the script:

    python blocktalk.py

2. Select option 3 to test if a message can fit in OP_RETURN:
    From the main menu, enter 3 to start the process of testing your message.

    Select an option: 3

3. Enter your text message:
    You will be prompted to enter the text message you want to test. The script will check if the message can fit within the OP_RETURN size limit. The maximum size for an OP_RETURN output is 80 bytes.

    Enter the text message to test: YourMessageHere

4. Exit

To exit the script, select option 4 from the main menu.

    Select an option: 4

Why Self-Transactions?

Purpose of Self-Transactions

In the context of BlockTalk, self-transactions are utilized to embed messages into the blockchain without requiring transfers to other parties. This method ensures that the funds remain under the user's control while allowing the inclusion of arbitrary data in the blockchain.

Benefits of Self-Transactions

- Control: Funds remain within your control, minimizing the risk of loss.
- Simplicity: Managing UTXOs and change addresses becomes straightforward.
- Efficiency: Reuse the same address for multiple transactions, simplifying tracking and management.

Detailed Explanation

- Self-Spending: Creating a transaction that spends outputs to the same address. This allows the use of UTXOs from your address to create transactions embedding messages in the blockchain.
- Self-Change: Sending any remaining funds from a transaction back to the same address. This ensures that any unspent funds are retained and can be used for future transactions.

Example Commands

Here are some example commands to help you understand how to use the script:

1. Set Address:
    python blocktalk.py
    - Select option 1 and follow the prompts to set your address

2. Embed a New Message:
    python blocktalk.py
    - Select option 2 and follow the prompts to embed your message

3. Test if a Message Can Fit in OP_RETURN:
    python blocktalk.py
    - Select option 3 and follow the prompts to test your message

Future Work

We plan to add the following features in future updates:

- Automated confirmation of the transaction.
- Automated decryption of the message once the transaction is confirmed in the blockchain.

Contributing

Contributions are welcome! If you would like to contribute to this project, please create a pull request with your proposed changes. Each pull request will be reviewed before being merged.

License

This project is licensed under the MIT License.

Author

Created by Charles Norton.