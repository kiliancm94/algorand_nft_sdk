import logging
from algosdk.future import transaction
from algosdk import algod

from algorand_nft_sdk.utils.account import Account


def sign_and_send_transaction(
    algod_client: algod.AlgodClient,
    source_account: Account,
    txn: transaction.Transaction,
    log: logging.Logger,
) -> dict:
    stxn = txn.sign(source_account.private_key)
    txid = algod_client.send_transaction(stxn)

    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)

        log.info(f"TXID: {txid}")
        log.info(f"Result confirmed in round: {confirmed_txn['confirmed-round']}")

        return txid, confirmed_txn
    except Exception as err:
        log.error(err)
        raise
