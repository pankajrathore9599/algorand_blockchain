# import for creating new account
from algosdk import account, mnemonic

# import for making transaction
from algosdk.v2client import algod

# import for build transaction
from algosdk.future import transaction
from algosdk import constants

# import for submit transaction
import json
import base64


# Creating account 
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# Calling funtion for creating new account
# generate_algorand_keypair()


# Result after running
# My address: N26ZSEGX7M3QC7SNI4EOANGA5UZ55D5JEUWZOHOZQGALJZKPDMTKQWFC4I
# My private key: dhtBoMgTu1avIjHVlUt0OSk5LavNayKbwRoQPHVQ93BuvZkQ1/s3AX5NRwjgNMDtM96PqSUtlx3ZgYC05U8bJg==
# My passphrase: human afford expand develop involve stick betray couple rival comic riot near inch slender hood hint gold all aspect scissors tuna staff marble about tribe


# Creating first transaction
def first_transaction_example(private_key, my_address):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# Build Transaction

    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    note = "Hello World".encode()
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

# Sign Transaction

    signed_txn = unsigned_txn.sign(private_key)


    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

#replace private_key and my_address with your private key and your address
first_transaction_example("dhtBoMgTu1avIjHVlUt0OSk5LavNayKbwRoQPHVQ93BuvZkQ1/s3AX5NRwjgNMDtM96PqSUtlx3ZgYC05U8bJg==", "N26ZSEGX7M3QC7SNI4EOANGA5UZ55D5JEUWZOHOZQGALJZKPDMTKQWFC4I")

# OUTPUT RESULT AFTER RUN

# Account balance: 5000000 microAlgos

# Successfully sent transaction with txID: C2VSUJQZ4GBZH5GISU3SP2JYV5W57XL2BJY3WMFGNRYGZVM2FKPA
# Transaction information: {
#     "confirmed-round": 19821324,
#     "pool-error": "",
#     "txn": {
#         "sig": "c2IJRQX0zyG2LevehKbyZzn/b9XhJnWJWllIT1XUnP39SyFiE2WUiBD07Ydzis1jMjKjclnYvoUZI6d0yzYECg==",
#         "txn": {
#             "amt": 1000000,
#             "fee": 1000,
#             "fv": 19821322,
#             "gen": "testnet-v1.0",
#             "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#             "lv": 19822322,
#             "note": "SGVsbG8gV29ybGQ=",
#             "rcv": "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA",
#             "snd": "N26ZSEGX7M3QC7SNI4EOANGA5UZ55D5JEUWZOHOZQGALJZKPDMTKQWFC4I",
#             "type": "pay"
#         }
#     }
# }
# Decoded note: Hello World
# Starting Account balance: 5000000 microAlgos
# Amount transfered: 1000000 microAlgos
# Fee: 1000 microAlgos
# Final Account balance: 3999000 microAlgos
