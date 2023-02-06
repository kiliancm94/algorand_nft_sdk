from unittest import mock

import pytest
from algosdk.error import EmptyAddressError
from hamcrest import assert_that, equal_to, has_items

from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.core import exceptions
from algorand_nft_sdk.core.arc import NFT
from algorand_nft_sdk.utils.account import Account, generate_account


def test_nft_create(test_account, asset_created, caplog):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            source_account=test_account,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}#arc3",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )

        nft_created = nft.create()

        assert_that(nft_created, equal_to(asset_created[-1]["asset-index"]))

        assert_that(
            caplog.messages,
            has_items(
                "Validation of url download skipped because the url contains '{id}'",
                "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
            ),
        )


def test_nft_validation_url(test_account, caplog):
    with pytest.raises(
        exceptions.ValueErrorAssetUrl,
        match=(
            "Asset name must end with #arc3 based on your asset_name, "
            "please check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md"
        ),
    ):
        NFT(
            algod_client=mock.MagicMock(),
            source_account=test_account,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )
    assert_that(
        caplog.messages,
        has_items(
            "Validation of url download skipped because the url contains '{id}'",
            "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
        ),
    )


def test_validate_asset_is_created(test_account, asset_created, caplog):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            source_account=test_account,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}#arc3",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )

        with pytest.raises(
            exceptions.AssetIdIsNone,
            match="Send the asset_id when it's initialized or create it first.",
        ):
            nft.validate_asset_is_created()


def test_transfer_nft(test_account, asset_created, caplog):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            asset_id=asset_created[-1]["asset-index"],
            source_account=test_account,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}#arc3",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )

        nft_transferred = nft.transfer(receiver=test_account, amount=1)

        assert_that(nft_transferred, equal_to(asset_created[0]))

        assert_that(
            caplog.messages,
            has_items(
                "Validation of url download skipped because the url contains '{id}'",
                "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
            ),
        )


def test_transfer_nft_with_no_asset_id(test_account, caplog):
    algod_client = mock.MagicMock()
    nft = NFT(
        algod_client=algod_client,
        source_account=test_account,
        arc_type=ARCType.ARC_3,
        unit_name="test-nft",
        asset_name="the asset name",
        asset_url="https://myasset.io/{id}#arc3",
        fee=30,
        flat_fee=1,
        do_metadata_validation=False,
        strict_empty_address_check=False,
    )

    with pytest.raises(
        exceptions.AssetIdIsNone,
        match="Send the asset_id when it's initialized or create it first.",
    ):
        nft.transfer(receiver=test_account, amount=1)

    assert_that(
        caplog.messages,
        has_items(
            "Validation of url download skipped because the url contains '{id}'",
            "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
        ),
    )


def test_optin_nft(test_account, asset_created, caplog):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            asset_id=asset_created[-1]["asset-index"],
            source_account=test_account,
            arc_type=ARCType.ARC_3,
            unit_name="test-nft",
            asset_name="the asset name",
            asset_url="https://myasset.io/{id}#arc3",
            fee=30,
            flat_fee=1,
            do_metadata_validation=False,
            strict_empty_address_check=False,
        )

        nft_optin_response = nft.optin()

        assert_that(nft_optin_response, equal_to(asset_created[0]))

        assert_that(
            caplog.messages,
            has_items(
                "Validation of url download skipped because the url contains '{id}'",
                "The url should be https or ipfs, check https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md",
            ),
        )


def test_update(test_account, asset_created):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            asset_id=asset_created[-1]["asset-index"],
            source_account=test_account,
            manager_account=test_account,
            fee=30,
            flat_fee=1,
            strict_empty_address_check=False,
        )

        nft_updated = nft.update()

        assert_that(nft_updated, equal_to(asset_created[0]))


def test_update_with_no_accounts_to_update(test_account, asset_created, caplog):
    nft = NFT(
        algod_client=mock.MagicMock(),
        asset_id=asset_created[-1]["asset-index"],
        source_account=test_account,
        fee=30,
        flat_fee=1,
        do_metadata_validation=False,
        strict_empty_address_check=False,
    )

    with pytest.raises(
        exceptions.AssetUpdateError,
        match=(
            "Manager, reserve, freeze and clawback accounts are not sent.\n"
            "Only those accounts can be modified."
        ),
    ):
        nft.update()

    assert_that(
        caplog.messages,
        has_items(
            "Manager, reserve, freeze and clawback accounts are not sent.\nOnly those accounts can be modified."
        ),
    )


def test_nft_transaction_without_restrict_to_empty_address(
    test_account, asset_created, caplog
):
    with mock.patch("algosdk.future.transaction") as transaction_mocked, mock.patch(
        "algorand_nft_sdk.core.arc.sign_and_send_transaction"
    ) as sign_and_send_transaction_mocked:
        algod_client = mock.MagicMock()
        transaction_mocked.side_effect = mock.MagicMock()

        sign_and_send_transaction_mocked.return_value = asset_created

        algod_client.pending_transaction_info.return_value = asset_created[-1]

        nft = NFT(
            algod_client=algod_client,
            asset_id=asset_created[-1]["asset-index"],
            source_account=test_account,
            manager_account=test_account,
            fee=30,
            flat_fee=1,
        )

        with pytest.raises(
            EmptyAddressError,
            match=(
                "manager, freeze, reserve, and clawback should not "
                "be empty unless strict_empty_address_check is set to False"
            ),
        ):
            nft.update()
