import os
from algosdk.v2client import algod
from algosdk import account
from algosdk import transaction
from algosdk.future.transaction import wait_for_confirmation as transaction_wait_for_confirmation
from algosdk import constants
import base64
import json

from typing import Tuple, Optional
from collections import namedtuple

import logging

Account = namedtuple("Account", ["private_key", "address"])

import sys

file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

log = logging.getLogger(__name__)

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
        confirmed_txn = transaction_wait_for_confirmation(algod_client, txid, 4)  
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
