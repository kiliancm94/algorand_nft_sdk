import json
from typing import Optional

from algosdk import account
from algosdk.future import transaction
from algosdk.transaction import AssetConfigTxn
from algosdk.v2client import algod

from algorand_nft_sdk_old.transaction.create import Account
from algorand_nft_sdk_old.utils.logger import get_logger

log = get_logger()


def create_asset_config(
    algod_client: algod.AlgodClient,
    source_account: Account,
    total: int = 1000, # to remove harcoding later
    url: str = "https://path/to/my/asset/details",  # to remove harcoding later
    unit_name: str = "LATINUM",  # to remove harcoding later
    asset_name: str = "latinum", # to remove harcoding later
    decimals: int = 0,
    default_frozen: bool = False,
    fee: Optional[int] = None,
    flat_fee: Optional[bool] = None,
    manager_account: Optional[Account] = None
):
    params = algod_client.suggested_params()

    if fee:
        params.fee = fee
    if flat_fee:
        params.flat_fee = flat_fee
    
    if not manager_account:
        manager_account = source_account
    # Account 1 creates an asset called latinum and
    # sets Account 2 as the manager, reserve, freeze, and clawback address.
    
    # Asset Creation transaction
    txn = AssetConfigTxn(
        sender=source_account.private_key,
        sp=params,
        total=total,
        default_frozen=default_frozen,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=manager_account.private_key,
        reserve=manager_account.private_key,
        freeze=manager_account.private_key,
        clawback=manager_account.private_key,
        url=url,
        decimals=decimals,
    )
    # Sign with secret key of creator
    stxn = txn.sign(source_account.private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        log.info(f"Signed transaction with txID: {txid}")
        # Wait for the transaction to be confirmed
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
        log.info(f"TXID: {txid}")
        log.info(f"Result confirmed in round: {confirmed_txn['confirmed-round']}")   
    except Exception as err:
        log.error(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.
    log.info(f"Transaction information: {json.dumps(confirmed_txn, indent=4)}")
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        # print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        # print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)
