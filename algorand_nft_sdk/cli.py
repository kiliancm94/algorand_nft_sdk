import click

from algorand_nft_sdk import app

# My account funded is CT66XA3T6G63NRP3HATPD3G4GPEEP4X42DE2NMUWJ72WVRVVTVQZ7F3BDA, private key
# can be found in a my_private_key file.
# ('Ha+zrQZPMVoEzdv0MB1nEoVanfQH2CsDEB61sVFZWyoU/euDc/G9tsX7OCbx7NwzyEfy/NDJprKWT/VqxrWdYQ==',
#  'CT66XA3T6G63NRP3HATPD3G4GPEEP4X42DE2NMUWJ72WVRVVTVQZ7F3BDA')


@click.group()
def nft():
    click.echo("Hello!")
    pass


@click.command()
@click.option(
    "--private-key",
    type=str,
    required=True,
    help="File path of the private key or plain private key used to sign the transactions.",
)
@click.option(
    "--unit-name",
    required=True,
    type=str,
    help="Name of an unit of this asset",
)
@click.option("--asset-name", required=True, type=str, help="Name of the asset")
@click.option(
    "--asset-url",
    required=True,
    type=str,
    help="URL where to find the Asset, it must be accessible",
)
# @click.option(
#     "--asset-metadata-hash",
#     required=True,
#     type=str,
#     help="The calculated has of the metadata of the asset."
# )
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
    app.mint_nft_arc3(
        private_key=private_key,
        unit_name=unit_name,
        asset_name=asset_name,
        asset_url=asset_url,
    )


nft.add_command(mint_nft_arc3)


if __name__ == "__main__":
    nft()
