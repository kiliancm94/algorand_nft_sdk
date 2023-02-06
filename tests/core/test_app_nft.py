from unittest import mock

from hamcrest import assert_that, equal_to, has_item, has_items
import pytest

from algorand_nft_sdk.app import nft
from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.core.exceptions import AssetUpdateError


def test_mint_nft_arc(test_account, asset_created, caplog):
    with mock.patch(
        "algorand_nft_sdk.app.nft.algod_client"
    ) as algod_client_mocked, mock.patch(
        "algosdk.future.transaction"
    ) as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        sign_and_send_transaction_mocked.return_value = asset_created
        algod_client_mocked.pending_transaction_info.return_value = asset_created[-1]

        minted_nft = nft.mint_nft_arc(
            private_key=test_account.private_key,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}#arc3",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )

        assert_that(minted_nft, equal_to(asset_created[-1]["asset-index"]))
        assert_that(
            caplog.messages,
            has_items(
                "Validation of url download skipped because the url contains '{id}'",
                "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
            ),
        )


def test_transfer_nft_arc(test_account, asset_created):
    with mock.patch(
        "algorand_nft_sdk.app.nft.algod_client"
    ) as algod_client_mocked, mock.patch(
        "algosdk.future.transaction"
    ) as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        sign_and_send_transaction_mocked.return_value = asset_created
        algod_client_mocked.pending_transaction_info.return_value = asset_created[-1]

        transferred_nft = nft.transfer_nft_arc(
            private_key=test_account.private_key,
            asset_id=asset_created[-1]["asset-index"],
            amount=1,
            receiver_address=test_account,
        )

        assert_that(transferred_nft, equal_to(asset_created[0]))


def test_optin_nft_arc(test_account, asset_created):
    with mock.patch(
        "algorand_nft_sdk.app.nft.algod_client"
    ) as algod_client_mocked, mock.patch(
        "algosdk.future.transaction"
    ) as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        sign_and_send_transaction_mocked.return_value = asset_created
        algod_client_mocked.pending_transaction_info.return_value = asset_created[-1]

        optin_nft = nft.optin_nft_arc(
            private_key=test_account.private_key,
            asset_id=asset_created[-1]["asset-index"],
        )

        assert_that(optin_nft, equal_to(asset_created[0]))


def test_update_nft(test_account, asset_created):
    with mock.patch(
        "algorand_nft_sdk.app.nft.algod_client"
    ) as algod_client_mocked, mock.patch(
        "algosdk.future.transaction"
    ) as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        sign_and_send_transaction_mocked.return_value = asset_created
        algod_client_mocked.pending_transaction_info.return_value = asset_created[-1]

        updated_nft = nft.update_nft_arc(
            private_key=test_account.private_key,
            asset_id=asset_created[-1]["asset-index"],
            reserve_account=test_account,
            strict_empty_address_check=False,
        )

        assert_that(updated_nft, equal_to(asset_created[0]))


def test_update_nft_failing_because_no_addresses(test_account, asset_created, caplog):
    with mock.patch(
        "algorand_nft_sdk.app.nft.algod_client"
    ) as algod_client_mocked, mock.patch(
        "algosdk.future.transaction"
    ) as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        sign_and_send_transaction_mocked.return_value = asset_created
        algod_client_mocked.pending_transaction_info.return_value = asset_created[-1]

        with pytest.raises(
            AssetUpdateError,
            match=(
                "Manager, reserve, freeze and clawback accounts are not sent.\n"
                "Only those accounts can be modified."
            ),
        ):
            nft.update_nft_arc(
                private_key=test_account.private_key,
                asset_id=asset_created[-1]["asset-index"],
            )

        assert_that(
            caplog.messages,
            has_item(
                "Manager, reserve, freeze and clawback accounts are not sent.\nOnly those accounts can be modified."
            ),
        )
