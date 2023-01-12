from typing import Optional

import click
from algosdk.algod import AlgodClient

from algorand_nft_sdk_old.nft import create
from algorand_nft_sdk_old.schemas.assets import ARC3
from algorand_nft_sdk_old.transaction.create import Account


@click.command()
def create_nft(
    source_account: Account,
    arc3_info: ARC3,
    unit_name: str,
    total: int = 1,
    decimals: int = 0,
    default_frozen: bool = False,
    fee: Optional[int] = None,
    flat_fee: Optional[bool] = None,
    manager_account: Optional[Account] = None,
):
    create.create_arc3(
        algod_client=AlgodClient(),
        source_account=source_account,
        arc3_info=arc3_info,
        total=total,
        unit_name=unit_name,
        decimals=decimals,
        default_frozen=default_frozen,
        fee=fee,
        flat_fee=flat_fee,
        manager_account=manager_account,
    )
