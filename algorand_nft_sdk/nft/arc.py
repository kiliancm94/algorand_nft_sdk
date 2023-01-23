import json
from typing import Optional
import requests

from algosdk.future import transaction
from algosdk.v2client import algod

from algorand_nft_sdk.utils.logger import get_logger
from algorand_nft_sdk.nft import exceptions

# from algorand_nft_sdk.asset_schemas.arc3 import ARC3
from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.utils.account import Account
from algorand_nft_sdk.utils.transaction import sign_and_send_transaction

log = get_logger()


class NFT:
    """
    NFT of type ARC3. You can find all the features and more extensive explanation in the offical docs.
    https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md
    """

    def __init__(
        self,
        algod_client: algod.AlgodClient,
        source_account: Account,
        arc_type: ARCType = ARCType.ARC_3,
        unit_name: Optional[str] = None,
        asset_name: Optional[str] = None,
        asset_url: Optional[str] = None,
        asset_id: Optional[str] = None,
        asset_metadata_hash: Optional[str] = None,
        total: int = 1,
        decimals: int = 0,
        default_frozen: bool = False,
        fee: Optional[int] = None,
        flat_fee: Optional[bool] = None,
        manager_account: Optional[Account] = None,
        reserve_account: Optional[Account] = None,
        freeze_account: Optional[Account] = None,
        clawback_account: Optional[Account] = None,
        strict_empty_address_check: bool = True,
        overrides_suggested_params: Optional[dict] = None,
    ) -> None:
        """
        *   algod_client: Client of Algorand.
        *   source_account: It's the account that will be the owner of the asset.
        *   arc_type: Type of ARC, supported values are 'arc3', 'arc19'.
        *   unit_name: The name of a unit of this asset. Supplied on creation. Max size is 8 bytes. Example: USDT
        *   asset_name: The name of the asset. Supplied on creation. Max size is 32 bytes. Example: Tether
        *   asset_url: Specifies a URL where more information about the asset can be retrieved. Max size is 96 bytes.
        *   asset_metadata_hash: This field is intended to be a 32-byte hash of some metadata that is relevant to your asset and/or asset holders. The format of this metadata is up to the application. This field can only be specified upon creation. An example might be the hash of some certificate that acknowledges the digitized asset as the official representation of a particular real-world asset.
        *   total: The total number of base units of the asset to create. This number cannot be changed.
        *   decimals: The number of digits to use after the decimal point when displaying the asset. If 0, the asset is not divisible. If 1, the base unit of the asset is in tenths. If 2, the base unit of the asset is in hundredths, if 3, the base unit of the asset is in thousandths, and so on up to 19 decimal places.
        *   default_frozen: True to freeze holdings for this asset by default.
        *   fee: Paid by the sender to the FeeSink to prevent denial-of-service. The minimum fee on Algorand is currently 1000 microAlgos.
        *   flat_fee: A flat fee is a fee that does not depend on the size of the transaction.
        *   manager_account: The account that can manage the configuration of the asset and destroy it.
        *   reserve_account: The account that holds the reserve (non-minted) units of the asset. This address has no specific authority in the protocol itself. It is used in the case where you want to signal to holders of your asset that the non-minted units of the asset reside in an account that is different from the default creator account (the sender).
        *   freeze_account: The account used to freeze holdings of this asset. If empty, freezing is not permitted.
        *   clawback_account The account that can clawback holdings of this asset. If empty, clawback is not permitted.
        *   strict_empty_address_check: If False, permits empty addresses.
        *   overrides_suggested_params: For advance users, you can provide additional attributes you want to overwrite over the suggested params.

        By default, if no manager and no reserve account are provided, the source account will inherate all those privilages.

        For more information about the parameters you can check https://developer.algorand.org/docs/get-details/transactions/transactions/
        """

        self.algod_client = algod_client
        self.source_account = source_account

        ARC = ARCType.get_arc_class(arc_type=arc_type)
        arc_dict = dict(
            unit_name=unit_name,
            asset_name=asset_name,
            asset_url=asset_url,
            asset_metadata_hash=asset_metadata_hash,
        )
        self.arc_schema = ARC.parse_obj({k: v for k, v in arc_dict.items() if v})
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
        self.reserve_account = reserve_account if reserve_account else source_account
        self.freeze_account = freeze_account
        self.clawback_account = clawback_account

        self.strict_empty_address_check = strict_empty_address_check
        self.asset_id = asset_id

    def validate_asset_is_created(self):
        if not self.asset_id:
            raise exceptions.AssetIdIsNone(
                "Send the asset_id when it's initialized or create it first."
            )

    def create(self) -> str:
        """Sends a transaction to create the asset"""
        # Asset Creation transaction
        txn = transaction.AssetConfigTxn(
            sender=self.source_account.address,
            sp=self.params,
            total=self.total,
            default_frozen=self.default_frozen,
            unit_name=self.unit_name,
            asset_name=self.arc_schema.asset_name,
            manager=self.manager_account.address,
            reserve=self.reserve_account.address,
            freeze=self.freeze_account.address if self.freeze_account else None,
            clawback=self.clawback_account.address if self.clawback_account else None,
            url=self.arc_schema.asset_url,
            decimals=self.decimals,
            strict_empty_address_check=self.strict_empty_address_check,
        )

        txid, confirmed_txn = sign_and_send_transaction(
            algod_client=self.algod_client,
            source_account=self.source_account,
            txn=txn,
            log=log,
        )
        log.info(f"Transaction information: {json.dumps(confirmed_txn, indent=4)}")
        try:
            ptx = self.algod_client.pending_transaction_info(txid)
            asset_id = ptx["asset-index"]

            self.asset_id = asset_id

            log.info(f"asset_id: {asset_id}")
        except Exception as e:
            print(e)

    def validate_asset_url(self) -> None:
        """Validates the asset url is accessible"""
        response = requests.get(self.arc_schema.asset_url)

        if not response.ok:
            raise exceptions.AssetUrlNotAccessible(
                f"The asset url {self.arc_schema.asset_url} it was not accessible."
                "Please, verify the url is still up."
            )

    def transfer(self, receiver: Account, amount: int) -> str:
        """
        Sends the NFT to an account

        *   receiver: Account of the receiver.
        *   amount: Amount to send to the receiver.
        """

        self.validate_asset_is_created()
        txn_transfer = transaction.AssetTransferTxn(
            sender=self.source_account.address,
            sp=self.params,
            receiver=receiver.address,
            amt=amount,
            index=self.asset_id,
        )

        txid, confirmed_txn = sign_and_send_transaction(
            algod_client=self.algod_client,
            source_account=self.source_account,
            txn=txn_transfer,
            log=log,
        )
        log.info(f"Transaction information: {json.dumps(confirmed_txn, indent=4)}")
        return txid

    def optin(self) -> None:
        """
        Holds an asset in order the asset can be sent to an address.
        https://developer.algorand.org/docs/get-details/asa/#receiving-an-asset
        """
        self.validate_asset_is_created()

        account_info = Account.get_account_info(
            self.source_account.address,
            self.algod_client,
        )

        for asset in account_info["assets"]:
            if asset["asset-id"] == self.asset_id:
                log.info("The account already opt in to the asset.")
                return

        txn_transfer = transaction.AssetTransferTxn(
            sender=self.source_account.address,
            sp=self.params,
            receiver=self.source_account.address,
            amt=0,
            index=self.asset_id,
        )

        _, confirmed_txn = sign_and_send_transaction(
            algod_client=self.algod_client,
            source_account=self.source_account,
            txn=txn_transfer,
            log=log,
        )
        log.info(f"Transaction information: {json.dumps(confirmed_txn, indent=4)}")
