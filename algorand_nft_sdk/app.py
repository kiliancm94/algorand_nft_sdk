import os
from typing import Optional

from algosdk.v2client import algod
from algosdk.account import address_from_private_key

from algorand_nft_sdk.nft import arc3
from algorand_nft_sdk.utils.account import Account, get_private_key_from_file_or_string

# FIXME: FROM HERE
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)
# FIXME: UNTIL HERE


def mint_nft_arc3(
    private_key: str,
    unit_name: str,
    asset_name: str,
    asset_url: str,
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
):
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )

    arc3_nft = arc3.NFT(
        algod_client,
        source_account=source_account,
        unit_name=unit_name,
        asset_name=asset_name,
        asset_url=asset_url,
        asset_metadata_hash=asset_metadata_hash,
        total=total,
        decimals=decimals,
        default_frozen=default_frozen,
        fee=fee,
        flat_fee=flat_fee,
        manager_account=manager_account,
        reserve_account=reserve_account,
        freeze_account=freeze_account,
        clawback_account=clawback_account,
        strict_empty_address_check=strict_empty_address_check,
        overrides_suggested_params=overrides_suggested_params,
    )

    arc3_nft.validate_asset_url()
    arc3_nft.create()


def transfer_nft_arc3(
    private_key: str,
    receiver_address: str,
    asset_id: int,
    amount: int,
):
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )
    arc3_nft = arc3.NFT(
        algod_client=algod_client,
        asset_id=asset_id,
        source_account=source_account,
    )

    receiver_account = Account(address=receiver_address)

    arc3_nft.transfer(receiver=receiver_account, amount=amount)
