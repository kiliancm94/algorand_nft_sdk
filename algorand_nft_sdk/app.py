import os

import click
from algosdk.v2client import algod
from algosdk.account import address_from_private_key, generate_account

from algorand_nft_sdk.nft import arc3
from algorand_nft_sdk.utils.account import Account

# My account funded is CT66XA3T6G63NRP3HATPD3G4GPEEP4X42DE2NMUWJ72WVRVVTVQZ7F3BDA, private key
# can be found in a my_private_key file.
# ('Ha+zrQZPMVoEzdv0MB1nEoVanfQH2CsDEB61sVFZWyoU/euDc/G9tsX7OCbx7NwzyEfy/NDJprKWT/VqxrWdYQ==',
#  'CT66XA3T6G63NRP3HATPD3G4GPEEP4X42DE2NMUWJ72WVRVVTVQZ7F3BDA')


@click.group()
def nft():
    click.echo("Hello!")
    pass


def mint_nft_arc3(
    private_key: str,
    unit_name: str,
    asset_name: str,
    asset_url: str,
    # asset_metadata_hash: str,
    # total: int = 1,
    # decimals: int = 0,
    # default_frozen: bool = False,
    # fee: Optional[int] = None,
    # flat_fee: Optional[bool] = None,
    # manager_account: Optional[Account] = None,
    # overrides_suggested_params: Optional[dict] = None,
):
    # algod_client = algod.AlgodClient()

    # FIXME: FROM HERE
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    # FIXME: UNTIL HERE

    if os.path.isfile(private_key):
        with open(private_key, "r") as file:
            private_key = file.read().strip()

    source_account = Account(
        private_key=private_key,
        address=address_from_private_key(private_key=private_key),
    )

    print(source_account)

    arc3_nft = arc3.NFT(
        algod_client,
        source_account=source_account,
        unit_name=unit_name,
        asset_name=asset_name,
        asset_url=asset_url,
    )

    arc3_nft.validate_metadata()
    arc3_nft.create()
