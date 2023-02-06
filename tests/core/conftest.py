import pytest
from algosdk.account import generate_account

from algorand_nft_sdk.utils.account import Account


@pytest.fixture(scope="session")
def test_account() -> Account:
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
