import base64
import json
import logging
import os
import sys
from collections import namedtuple
from typing import Optional, Tuple

from algosdk import account
from algosdk.future import transaction
from algosdk.v2client import algod
from algorand_nft_sdk_old.utils.logger import get_logger

Account = namedtuple("Account", ["private_key", "address"])


log = get_logger()


def get_client():
    algod_address: str = os.getenv("ALGORAND_NETWORK_ADDRESS", "http://localhost:4001")
    algod_token: str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    return algod_client


def generate_algorand_keypair() -> Tuple[str, str]:
    private_key, address = account.generate_account()
    return Account(private_key, address)


def get_account_info(algod_client: algod.AlgodClient, account_address: str) -> dict:
    return algod_client.account_info(account_address)


def send_transaction(
    algod_client: algod.AlgodClient,
    source_address: str,
    private_key: str,
    amount: int = 1_000_000,
    receiver: str = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA",  # to undo kwarg
    flat_flee: Optional[bool] = None,
    fee: Optional[int] = None,
    note: str = "Hello world",    
):
    params = algod_client.suggested_params()

    if flat_flee:
        params.flat_fee = flat_flee
    if fee:
        params.fee =  fee

    unsigned_txn = transaction.PaymentTxn(
        source_address,
        params.fee,
        params.first,
        params.last,
        params.gh,
        receiver,
        amount,
        None,
        note.encode(),
    )

    signed_txn = unsigned_txn.sign(private_key)

    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    log.info(f"Successfully sent transaction with txID: {txid}")

    # wait for confirmation 
    account_info = get_account_info(algod_client=algod_client, account_address=source_address)
    log.info(f"Starting Account balance: {account_info.get('amount')} microAlgos")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        log.error(err)
        return

    account_info = get_account_info(algod_client=algod_client, account_address=source_address)

    log.info(f"Transaction information: {json.dumps(confirmed_txn, indent=4)}")
    log.info(f"Decoded note: {base64.b64decode(confirmed_txn['txn']['txn']['note']).decode()}")
    log.info(f"Amount transfered: {amount} microAlgos")    
    log.info(f"Fee: {params.fee} microAlgos") 

    log.info(f"Final Account balance: {account_info.get('amount')} microAlgos")


if __name__ == "__main__":
    my_account = Account(
        "dqoNuUd3l9kbpUzllkV16WxuIR64W1jypW/1XKr9xj9a1KWC2VfKKiuJ9g27oKGUjE9d+yRJQ9LLXPZSt+JrCQ==",
        "LLKKLAWZK7FCUK4J6YG3XIFBSSGE6XP3EREUHUWLLT3FFN7CNME2PNOI2Y"
    )
