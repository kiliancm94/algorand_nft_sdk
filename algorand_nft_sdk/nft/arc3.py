import json
from typing import Optional
import requests

from algosdk.future import transaction
from algosdk.transaction import AssetConfigTxn
from algosdk.v2client import algod

from algorand_nft_sdk.utils.logger import get_logger
from algorand_nft_sdk.nft import exceptions
from algorand_nft_sdk.asset_schemas.arc3 import ARC3, ARC3Metadata
from algorand_nft_sdk.utils.utils import Account

log = get_logger()

class NFT:
    def __init__(
        self,
        algod_client: algod.AlgodClient,
        source_account: Account,
        unit_name: str,
        asset_name: str,
        asset_url: str,
        asset_metadata_hash: str,
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
        self.arc3_schema = ARC3(
            unit_name=unit_name,
            asset_name=asset_name,
            asset_url=asset_url,
            asset_metadata_hash=asset_metadata_hash,
        ) 
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

    def create(self) -> None:
        # Asset Creation transaction
        txn = AssetConfigTxn(
            sender=self.source_account.private_key,
            sp=self.params,
            total=self.total,
            default_frozen=self.default_frozen,
            unit_name=self.unit_name,
            asset_name=self.arc3_schema.asset_name,
            manager=self.manager_account.private_key,
            reserve=self.manager_account.private_key,
            freeze=self.manager_account.private_key,
            clawback=self.manager_account.private_key,
            url=self.arc3_schema.asset_url,
            decimals=self.decimals,
        )

        stxn = txn.sign(self.source_account.private_key)
        txid = self.algod_client.send_transaction(stxn)
        
        try:
            confirmed_txn = transaction.wait_for_confirmation(
                self.algod_client,
                txid,
                4
            )
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
            ptx = self.algod_client.pending_transaction_info(txid)
            asset_id = ptx["asset-index"]
            # print_created_asset(algod_client, accounts[1]['pk'], asset_id)
            # print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
        except Exception as e:
            print(e)

    def validate_metadata(self) -> None:
        response = requests.get(self.arc3_schema.asset_url)

        if not response.ok:
            raise exceptions.AssetUrlNotAccessible(
                f"The asset url {self.arc3_schema.asset_url} it was not accessible."
                "Please, verify the url is still up."
            )
        
        try:
            ARC3Metadata(**response.json())
        except Exception as error:
            log.critical(
                "There was an exception validating the ARC3 metadata content."
                "Please, verify the algorand documenation, you can find it in the "
                "following link: https://github.com/algorandfoundation/ARCs/blob/main/ARCs/"
            )
            log.error(error)

            raise
