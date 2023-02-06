from typing import Optional

from algosdk.account import address_from_private_key

from algorand_nft_sdk.app import algod_client
from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.core import arc
from algorand_nft_sdk.utils.account import Account, get_private_key_from_file_or_string


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
    do_metadata_validation: bool = True,
):
    private_key = get_private_key_from_file_or_string(private_key)

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )

    manager_account = Account(address=manager_account) if manager_account else None
    reserve_account = Account(address=reserve_account) if reserve_account else None
    freeze_account = Account(address=freeze_account) if freeze_account else None
    clawback_account = Account(address=clawback_account) if clawback_account else None

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
    return arc_nft.create()


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

    return arc_nft.transfer(receiver=receiver_account, amount=amount)


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

    return arc_nft.optin()


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

    manager_account = Account(address=manager_account) if manager_account else None
    reserve_account = Account(address=reserve_account) if reserve_account else None
    freeze_account = Account(address=freeze_account) if freeze_account else None
    clawback_account = Account(address=clawback_account) if clawback_account else None

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

    return arc_nft.update()
