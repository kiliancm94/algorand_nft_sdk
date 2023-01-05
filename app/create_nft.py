from algosdk.v2client import algod
from algosdk.transaction import AssetConfigTxn
from algosdk import account

private_key, account_address = account.generate_account()

# preguntas que me van surgiendo:
# ¿Cómo se crea un cliente, que es token y address?
# 

# Kilian: written by me
# algod_client = AlgodClient(
#     algod_token="",
#     algod_address="",
# )

 # CREATE ASSET
# Get network params for transactions before every transaction.

params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True
# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
txn = AssetConfigTxn(
    sender=private_key,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=private_key,
    reserve=private_key,
    freeze=private_key,
    clawback=private_key,
    url="https://path/to/my/asset/details", 
    decimals=0,
)
# Sign with secret key of creator
stxn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
# print("Decoded note: {}".format(base64.b64decode(
#     confirmed_txn["txn"]["txn"]["note"]).decode()))
try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
except Exception as e:
    print(e)