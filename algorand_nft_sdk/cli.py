import os
from typing import Optional
import click
import json
import pydantic
from contextlib import contextmanager

from algorand_nft_sdk import algorand_nft_app
from algorand_nft_sdk.utils.account import Account
from algorand_nft_sdk.asset_schemas.arcs import ARCType

DEBUG_MODE = os.getenv(
    "DEBUG_MODE", False
)  # Fixme: Change to False by default when finished


class CLIExceptionManager:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if DEBUG_MODE:
            click.echo("Reraising exception since DEBUG MODE is active!")
            raise
        else:
            click.echo(f"{exc_type}: {exc_val}")
            return True


@click.group()
@click.option(
    "--private-key",
    type=str,
    required=False,
    help="File path of the private key or plain private key used to sign the transactions.",
)
@click.pass_context
def nft(ctx: click.Context, private_key: str):
    click.echo("Hello!")
    ctx.ensure_object(dict)
    ctx.obj["private_key"] = private_key


@nft.command
@click.pass_context
@click.option(
    "--arc-type",
    required=False,
    type=str,
    default=ARCType.ARC_3,
    help="ARC type. Supported values are 'arc3', 'arc19'",
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
@click.option(
    "--url-validation",
    type=bool,
    default=False,
    required=False,
    is_flag=True,
    help="It validates the url is accessible.",
)
@click.option(
    "--skip-metadata-validation",
    type=bool,
    default=False,
    is_flag=True,
    required=False,
    help="If it's sent it validates the JSON metadata file of the token.",
)
def mint_nft_arc(
    ctx: click.Context,
    **kwargs,
):
    kwargs["strict_empty_address_check"] = kwargs.pop("permit_empty_address") == False
    kwargs["do_metadata_validation"] = kwargs.pop("skip_metadata_validation") == False

    with CLIExceptionManager():
        try:
            algorand_nft_app.mint_nft_arc(
                private_key=ctx.obj["private_key"],
                **kwargs,
            )
        except Exception as error:
            if "url" in str(error):
                click.echo(str(error))

                click.echo(
                    "There was an error while validating url. "
                    "In case your url is not accessible and you want to skip the validation, "
                    "you can send the paramter --skip-metadata-validation."
                )

            raise


@nft.command
@click.pass_context
@click.option(
    "--receiver-address", type=str, required=True, help="Account of the receiver."
)
@click.option("--amount", type=int, required=True, help="Amount of tokens to transfer.")
@click.option(
    "--asset-id", type=int, required=True, help="Id of the asset to transfer."
)
def transfer_nft_arc(ctx, **kwargs):
    with CLIExceptionManager():
        algorand_nft_app.transfer_nft_arc(private_key=ctx.obj["private_key"], **kwargs)


@nft.command
@click.pass_context
@click.option(
    "--asset-id", type=int, required=True, help="Id of the asset to transfer."
)
def optin_nft_arc(ctx, **kwargs):
    with CLIExceptionManager():
        algorand_nft_app.optin_nft_arc(private_key=ctx.obj["private_key"], **kwargs)


@nft.command
@click.pass_context
@click.option(
    "--address",
    type=str,
    required=False,
    help="An account Address. If private key is passed, address is ignored!!!",
)
def account_assets(ctx, address: Optional[str] = None) -> None:
    if ctx.obj["private_key"] and address:
        click.echo("Private key is sent, hence address is ignored.")

    with CLIExceptionManager():
        click.echo(
            json.dumps(
                algorand_nft_app.account_assets(
                    private_key=ctx.obj["private_key"], address=address
                ),
                indent=2,
            )
        )


if __name__ == "__main__":
    nft(obj={})
