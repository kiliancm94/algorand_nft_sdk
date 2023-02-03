import os
from typing import Optional

from algosdk.account import address_from_private_key
from algosdk.v2client import algod

from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.nft import arc
from algorand_nft_sdk.utils.account import Account, get_private_key_from_file_or_string

ALGOD_ADDRESS = os.getenv("ALGOD_API_URL")
ALGOD_API_KEY = os.getenv("ALGOD_API_KEY")

if not (ALGOD_ADDRESS and ALGOD_API_KEY):
    raise EnvironmentError(
        f"Environment variables API_URL and ALGOD_API_KEY must be configured."
    )
algod_client = algod.AlgodClient(
    "", ALGOD_ADDRESS, headers={"X-API-Key": ALGOD_API_KEY}
)


def mint_nft_arc(
    private_key: str,
    arc_type: ARCType,
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
    url_validation: bool = False,
    do_metadata_validation: bool = True,
):
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )

    arc_nft = arc.NFT(
        algod_client,
        source_account=source_account,
        arc_type=arc_type,
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
        do_metadata_validation=do_metadata_validation,
    )

    if url_validation:
        arc_nft.validate_asset_url()
    arc_nft.create()


def transfer_nft_arc(
    private_key: str,
    receiver_address: str,
    asset_id: int,
    amount: int,
) -> None:
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )
    arc_nft = arc.NFT(
        algod_client=algod_client,
        asset_id=asset_id,
        source_account=source_account,
    )

    receiver_account = Account(address=receiver_address)

    arc_nft.transfer(receiver=receiver_account, amount=amount)


def optin_nft_arc(
    private_key: str,
    asset_id: int,
) -> None:
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )
    arc_nft = arc.NFT(
        algod_client=algod_client,
        asset_id=asset_id,
        source_account=source_account,
    )

    arc_nft.optin()


def account_assets(private_key: Optional[str], address: Optional[str]):
    if private_key:
        private_key = get_private_key_from_file_or_string(private_key)

    account = Account(
        private_key=private_key,
        address=address,
    )

    return account.get_assets_of_account(algod_client=algod_client)


def update_nft_arc(
    private_key: str,
    asset_id: int,
    fee: Optional[int] = None,
    flat_fee: Optional[bool] = None,
    manager_account: Optional[str] = None,
    reserve_account: Optional[Account] = None,
    freeze_account: Optional[Account] = None,
    clawback_account: Optional[Account] = None,
    strict_empty_address_check: bool = True,
    overrides_suggested_params: Optional[dict] = None,
):
    """
    Once an asset is created only the manager, reserve, freeze and
    clawback accounts of the asset can be modified.
    """
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )

    # FIXME: Add this in all the places
    manager_account = Account(address=manager_account) if manager_account else None

    arc_nft = arc.NFT(
        algod_client=algod_client,
        asset_id=asset_id,
        source_account=source_account,
        fee=fee,
        flat_fee=flat_fee,
        manager_account=manager_account,
        reserve_account=reserve_account,
        freeze_account=freeze_account,
        clawback_account=clawback_account,
        strict_empty_address_check=strict_empty_address_check,
        overrides_suggested_params=overrides_suggested_params,
    )

    arc_nft.update()
