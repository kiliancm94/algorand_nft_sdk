import pytest

from algorand_nft_sdk.core.arc import NFT
from unittest import mock
from algorand_nft_sdk.asset_schemas.arcs import ARCType
from algorand_nft_sdk.utils.account import generate_account, Account
from hamcrest import assert_that, equal_to, has_items


@pytest.fixture(scope="session")
def test_account():
    return Account(*generate_account())


@pytest.fixture
def asset_created() -> dict:
    return (
        "KP2EYGAE474PGKJRAQ6GP7Q66JPG5STJUCOXSTUMMMKOANA44THU",
        {
            "asset-index": 157248650,
            "confirmed-round": 27523768,
            "pool-error": "",
            "txn": {
                "sig": "0JWoEVcGOAYe+aOpuG8chEzpJvHpNgKNu4RinPyYVx4wCrQClGJZgNtlvMAQzVWSJVRql/UGlT0vwak5h81zDA==",
                "txn": {
                    "apar": {
                        "an": "kilian",
                        "au": "http://google.es/one-nft",
                        "m": "TNKODXNI6FZPGWTVWLA7PAIT5MFNOC7LKDTS6NDMN4TX3PGM63SZ7IAXEY",
                        "t": 1,
                        "un": "kil",
                    },
                    "fee": 1000,
                    "fv": 27523766,
                    "gen": "testnet-v1.0",
                    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
                    "lv": 27524766,
                    "snd": "TNKODXNI6FZPGWTVWLA7PAIT5MFNOC7LKDTS6NDMN4TX3PGM63SZ7IAXEY",
                    "type": "acfg",
                },
            },
        },
    )


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


#  asset_url="https://myasset.io#arc3" test without
