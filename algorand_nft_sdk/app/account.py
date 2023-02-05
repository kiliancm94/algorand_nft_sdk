from typing import Optional

from algorand_nft_sdk.app import algod_client
from algorand_nft_sdk.utils.account import Account, get_private_key_from_file_or_string


def account_assets(private_key: Optional[str], address: Optional[str]):
    if private_key:
        private_key = get_private_key_from_file_or_string(private_key)

    account = Account(
        private_key=private_key,
        address=address,
    )

    return account.get_assets_of_account(algod_client=algod_client)
