import json
from typing import Optional

from algosdk import account
from algosdk.future import transaction
from algosdk.transaction import AssetConfigTxn
from algosdk.v2client import algod

from algorand_nft_sdk_old.transaction.create import Account
from algorand_nft_sdk_old.utils.logger import get_logger
from algorand_nft_sdk_old.schemas.assets import ARC3

log = get_logger()

class NFT:
    def __init__(
        self,
        algod_client: algod.AlgodClient,
        source_account: Account,
        arc3_info: ARC3,
        unit_name: str,
        total: int = 1,
        decimals: int = 0,
        default_frozen: bool = False,
        fee: Optional[int] = None,
        flat_fee: Optional[bool] = None,
        manager_account: Optional[Account] = None,
        overrides_suggested_params: Optional[dict] = None,
    ) -> None:

        self.algod_client = algod_client
        self.source_account = source_account
        self.arc3_info = arc3_info
        self.unit_name = unit_name
        self.total = total
        self.decimals = decimals
        self.default_frozen = default_frozen

        self.params = algod_client.suggested_params()
        if fee:
            self.params.fee = fee
        if flat_fee:
            self.params.flat_fee = flat_fee

        if overrides_suggested_params:
            for key, value in overrides_suggested_params.items():
                setattr(self.params, key, value)

        self.manager_account = manager_account if manager_account else source_account


def create_arc3(
    algod_client: algod.AlgodClient,
    source_account: Account,
    arc3_info: ARC3,
    total: int = 1000, # to remove harcoding later
    unit_name: str = "LATINUM",  # to remove harcoding later
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
        asset_name=arc3_info.asset_name,
        manager=manager_account.private_key,
        reserve=manager_account.private_key,
        freeze=manager_account.private_key,
        clawback=manager_account.private_key,
        url=arc3_info.asset_url,
        decimals=decimals,
    )

    stxn = txn.sign(source_account.private_key)
    txid = algod_client.send_transaction(stxn)
    
    try:
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
