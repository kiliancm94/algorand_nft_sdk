from typing import Optional
import click
import json

from algorand_nft_sdk import app
from algorand_nft_sdk.utils.account import Account


@click.group()
@click.option(
    "--private-key",
    type=str,
    required=True,
    help="File path of the private key or plain private key used to sign the transactions.",
)
@click.pass_context
def nft(ctx: click.Context, private_key: str):
    click.echo("Hello!")
    ctx.ensure_object(dict)
    ctx.obj["private_key"] = private_key


@click.command
@click.pass_context
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
@click.option(
    "--asset-metadata-hash",
    required=False,
    type=str,
    help="The calculated has of the metadata of the asset.",
)
@click.option(
    "--total", required=False, type=int, default=1, help="Total amount of the asset."
)
@click.option(
    "--decimals",
    required=False,
    type=int,
    default=0,
    help="Total decimals of the asset.",
)
@click.option(
    "--default_frozen",
    required=False,
    type=bool,
    is_flag=True,
    default=False,
    help="If the token is by default frozen.",
)
@click.option(
    "--fee", required=False, type=int, default=None, help="The fee of the transaction."
)
@click.option(
    "--flat-fee",
    required=False,
    type=bool,
    is_flag=True,
    default=None,
    help="If it's a flat fee",
)
@click.option(
    "--manager-account",
    type=str,
    required=False,
    help="The account of the manager of the token.",
)
@click.option(
    "--reserve-account",
    type=str,
    required=False,
    help="The account for reserve token.",
)
@click.option(
    "--freeze-account",
    type=str,
    required=False,
    help="The account that can freeze the token.",
)
@click.option(
    "--clawback-account",
    type=str,
    required=False,
    help="The account that can clawback the token.",
)
@click.option(
    "--permit-empty-address",
    type=bool,
    required=False,
    default=False,
    is_flag=True,
    help="If it allows empty addresses.",
)
def mint_nft_arc3(
    ctx: click.Context,
    **kwargs,
):
    kwargs["strict_empty_address_check"] = kwargs.pop("permit_empty_address") == False
    app.mint_nft_arc3(
        private_key=ctx.obj["private_key"],
        **kwargs,
    )


@click.command
@click.pass_context
@click.option(
    "--receiver-address", type=str, required=True, help="Account of the receiver."
)
@click.option("--amount", type=int, required=True, help="Amount of tokens to transfer.")
@click.option(
    "--asset-id", type=int, required=True, help="Id of the asset to transfer."
)
def transfer_nft_arc3(ctx, **kwargs):
    app.transfer_nft_arc3(private_key=ctx.obj["private_key"], **kwargs)


@click.command
@click.pass_context
@click.option(
    "--asset-id", type=int, required=True, help="Id of the asset to transfer."
)
def opt_in_nft_arc3(ctx, **kwargs):
    app.opt_in_nft_arc3(private_key=ctx.obj["private_key"], **kwargs)


@click.command
@click.pass_context
def account_assets(ctx):
    click.echo(
        json.dumps(
            app.account_assets(private_key=ctx.obj["private_key"]),
            indent=2,
        )
    )


nft.add_command(mint_nft_arc3)
nft.add_command(transfer_nft_arc3)
nft.add_command(opt_in_nft_arc3)
nft.add_command(account_assets)


if __name__ == "__main__":
    nft(obj={})
