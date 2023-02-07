from algorand_nft_sdk.app import nft as nft_app
from algorand_nft_sdk.asset_schemas.arcs import ARCType


with open("my_private_key_3", "r") as f:
    private_key_3: str = f.read()

nft_minted = nft_app.mint_nft_arc(
    private_key=private_key_3,
    arc_type=ARCType.ARC_69,
    unit_name="kitten",
    asset_name="kitten",
    asset_url="http://google.es/one-nft",
    total=1,
    strict_empty_address_check=False,
    do_metadata_validation=False,
    manager_account="X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
)

# [2023-02-07 23:32:30,509] {arc69.py:32} WARNING - Consider use https instead of http for security reasons.
# [2023-02-07 23:32:35,402] {transaction.py:21} INFO - TXID: JJCVWDNQ22CBT3XTOCJ5MUT3QJQSBQ4IBEMUKOF5QPHZDD6YKRRA
# [2023-02-07 23:32:35,403] {transaction.py:22} INFO - Result confirmed in round: 27575228
# [2023-02-07 23:32:35,403] {arc.py:161} INFO - Transaction information: {
#     "asset-index": 157629566,
#     "confirmed-round": 27575228,
#     "pool-error": "",
#     "txn": {
#         "sig": "TzYacdZ2R6anKL6TTaLIdgkn2YTQ/mZ1euRYLOZDdzk2KVPVD/eE+9l6HHBrTzX7tQV/qMKtbZZYyCXhA78lAA==",
#         "txn": {
#             "apar": {
#                 "an": "kitten",
#                 "au": "http://google.es/one-nft",
#                 "m": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
#                 "t": 1,
#                 "un": "kitten"
#             },
#             "fee": 1000,
#             "fv": 27575226,
#             "gen": "testnet-v1.0",
#             "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#             "lv": 27576226,
#             "snd": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
#             "type": "acfg"
#         }
#     }
# }
# [2023-02-07 23:32:35,666] {arc.py:166} INFO - asset_id: 157629566

with open("my_private_key_4", "r") as f:
    private_key_4: str = f.read()

optin_nft = nft_app.optin_nft_arc(
    private_key=private_key_4,
    asset_id=nft_minted,
)

# In [3]: with open("my_private_key_4", "r") as f:
#    ...:     private_key_4: str = f.read()
#    ...:
#    ...: optin_nft = nft_app.optin_nft_arc(
#    ...:     private_key=private_key_4,
#    ...:     asset_id=nft_minted,
#    ...: )
# [2023-02-07 23:33:15,710] {transaction.py:21} INFO - TXID: C7EKN4EPW4L2Q4OEYCWP5C5KHRS4667DTISCN4RJ6JFN2DMYD72A
# [2023-02-07 23:33:15,713] {transaction.py:22} INFO - Result confirmed in round: 27575239
# [2023-02-07 23:33:15,713] {arc.py:229} INFO - Transaction information: {
#     "confirmed-round": 27575239,
#     "pool-error": "",
#     "txn": {
#         "sig": "HKtSgjbDUDUR9UuvXtIcy798ZDNTL+2inKJvU1I6hxgTUTO0nx7+rgvcZg0Id3oBDauXP2ZmXNESpesEXg6QAA==",
#         "txn": {
#             "arcv": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
#             "fee": 1000,
#             "fv": 27575236,
#             "gen": "testnet-v1.0",
#             "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#             "lv": 27576236,
#             "snd": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
#             "type": "axfer",
#             "xaid": 157629566
#         }
#     }
# }

transferred_nft = nft_app.transfer_nft_arc(
    private_key=private_key_3,
    receiver_address="R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
    asset_id=nft_minted,
    amount=1,
)

# In [5]: transferred_nft = nft_app.transfer_nft_arc(
#    ...:     private_key=private_key_3,
#    ...:     receiver_address="R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
#    ...:     asset_id=nft_minted,
#    ...:     amount=1,
#    ...: )
# [2023-02-07 23:33:59,691] {transaction.py:21} INFO - TXID: IDBL4255YTPZXUB5PMJE6W3VAUXJURRLTWHQRW2CDLF32WT5SZEA
# [2023-02-07 23:33:59,693] {transaction.py:22} INFO - Result confirmed in round: 27575251
# [2023-02-07 23:33:59,694] {arc.py:195} INFO - Transaction information: {
#     "confirmed-round": 27575251,
#     "pool-error": "",
#     "txn": {
#         "sig": "eNB9jkUS/XHNdvmKZkO6ERnkQs3xGBW+EhiexLzzivUXPI5S0LJUcc02TZkbJdxNxqfFH/I9D3s8ONsViIxpBw==",
#         "txn": {
#             "aamt": 1,
#             "arcv": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
#             "fee": 1000,
#             "fv": 27575249,
#             "gen": "testnet-v1.0",
#             "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#             "lv": 27576249,
#             "snd": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
#             "type": "axfer",
#             "xaid": 157629566
#         }
#     }
# }
