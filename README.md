# Algorand NFT SDK

Welcome to the Algorand NFT SDK! The Algorand NFT SDK is software to help you to manage and interact with Algorand Non-Fungible Tokens (NFTs) in the Algorand network. The project comes in 2 flavours, one is more for developers and the other one for non-developers. The first flavour is a Python package that you can use for managing the NFTs by coding and use it for your own applications. The second flavour is a command line interface (CLI).

## Motivation

The main motivation of this project is to provide great tooling to help developers and non-developers to manage their NFTs in the Algorand network by minimizing the learning curve. And of course, to have fun while building for others and learning about a great project, Algorand.

## How to use CLI

### Installing CLI

Firstly, you should clone the github repository.

```bash
git clone <here the public link>
cd algorand_nft_sdk
```

Secondly, you need to run have to installed python, and I would recommend to create a virtual envrionment. Then, you can run the pip install command.

```bash
pip install .
```

Finally, you can call the CLI program as following:

```bash
algonft

Usage: algonft [OPTIONS] COMMAND [ARGS]...

Options:
  --private-key TEXT  File path of the private key or plain private key used
                      to sign the transactions.
  --help              Show this message and exit.

Commands:
  account-assets
  generate-an-account
  get-address-from-private-key
  mint-nft-arc
  optin-nft-arc
  transfer-nft-arc
  update-nft-arc
```

### Creation and transferring of a NFT ARC69
Here you can find an example of the creation and transferring of a NFT by using the ARC 69 type. First, you need to fund the address, we are going to fund the address `X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE`. Most of the transactions will require you to send the --private-key option.

```bash
algonft --private-key my_private_key_3  mint-nft-arc --unit-name kitten --asset-name kitten --asset-url 'http://google.es/one-nft' --permit-empty-address --arc-type arc69 --skip-metadata-validation --manager-account X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE
Hello!
[2023-02-07 22:55:17,217] {arc69.py:32} WARNING - Consider use https instead of http for security reasons.
[2023-02-07 22:55:24,774] {transaction.py:21} INFO - TXID: TIIGGIUBXNAL673D2KXQYZACFVIPHHTPAZIMKOGY73SRNHDHFH4Q
[2023-02-07 22:55:24,775] {transaction.py:22} INFO - Result confirmed in round: 27574612
[2023-02-07 22:55:24,776] {arc.py:161} INFO - Transaction information: {
    "asset-index": 157625814,
    "confirmed-round": 27574612,
    "pool-error": "",
    "txn": {
        "sig": "Kr4q0+RuLuUd3vK6L2nxkBPjvVCV06rGVqD1pJoMhjssa5RGZ3Lf/SfEbyU/VnyvZNdCpVhzjmEB2Y16E7DCBA==",
        "txn": {
            "apar": {
                "an": "kitten",
                "au": "http://google.es/one-nft",
                "m": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
                "t": 1,
                "un": "kitten"
            },
            "fee": 1000,
            "fv": 27574610,
            "gen": "testnet-v1.0",
            "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
            "lv": 27575610,
            "snd": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
            "type": "acfg"
        }
    }
}
[2023-02-07 22:55:25,039] {arc.py:166} INFO - asset_id: 157625814
```

Once the NFT is generated, we need to make to execute an optin to the receiver address of the NFT generated. Let's see what happens if the receiver doesn't optin to the NFT.

```bash
algonft --private-key my_private_key_3 transfer-nft-arc --receiver-address R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U --amount 1 --asset-id 157625814
Hello!
<class 'algosdk.error.AlgodHTTPError'>: TransactionPool.Remember: transaction 5IX3JRCL5WVRXTOKDEUEUFJMNIU7MTNWX63KYQYWT6KK54QQNG7A: receiver error: must optin, asset 157625814 missing from R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U
```

It failed, we need the receiver address to opt to the NFT. Let's do it. Remember to fund the second account!

```bash
algonft --private-key my_private_key_4 optin-nft-arc --asset-id 157625814
Hello!
[2023-02-07 23:06:59,690] {transaction.py:21} INFO - TXID: 2TK5VM4FZJJJ7H7E4F7PLOXSQATDZL34YBWCOZ7R2VVYEP7YH24A
[2023-02-07 23:06:59,692] {transaction.py:22} INFO - Result confirmed in round: 27574805
[2023-02-07 23:06:59,692] {arc.py:229} INFO - Transaction information: {
    "confirmed-round": 27574805,
    "pool-error": "",
    "txn": {
        "sig": "kTwFmYkYbX3xqLvyvig6Rpywlw0CsTBMR8itk7DNAJlBSyW0dmH+hgbH3sNwOZyVJMnsYcKt0Me+MTvMm+8QAA==",
        "txn": {
            "arcv": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
            "fee": 1000,
            "fv": 27574802,
            "gen": "testnet-v1.0",
            "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
            "lv": 27575802,
            "snd": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
            "type": "axfer",
            "xaid": 157625814
        }
    }
}
```

Finally, let's going to transfer the NFT.

```bash
algonft --private-key my_private_key_3 transfer-nft-arc --receiver-address R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U --amount 1 --asset-id 157625814

Hello!
[2023-02-07 23:07:53,828] {transaction.py:21} INFO - TXID: PRYLUF3HRIRGYIW6J6SEMKBODYYGSLTU27LQUVP2DLDAEYH4HHAA
[2023-02-07 23:07:53,830] {transaction.py:22} INFO - Result confirmed in round: 27574820
[2023-02-07 23:07:53,831] {arc.py:195} INFO - Transaction information: {
    "confirmed-round": 27574820,
    "pool-error": "",
    "txn": {
        "sig": "fzGpcmod4yHHYEnHVu7qVOwEJupSGgJ0Zq2yBtqa/Wuy0Lqgbj8AsPtK3Z5aua+iblbNOcqFjSvVckGqqjhCBg==",
        "txn": {
            "aamt": 1,
            "arcv": "R7TWWK7HPBDVK7A4E2JA2EL4DOKPBN6ZD4AG7OACKNYKBKFORVDKRD572U",
            "fee": 1000,
            "fv": 27574818,
            "gen": "testnet-v1.0",
            "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
            "lv": 27575818,
            "snd": "X2QMWT7XZJ6BYEPK3L74S4W3ZUO7VYM4FMH6MAK247JFBAQZRQ6EBVPSXE",
            "type": "axfer",
            "xaid": 157625814
        }
    }
}
```

The token was tranferred with success.
```bash
algonft --private-key my_private_key_4 account-assets
Hello!
{
  "157625814": {
    "amount": 1,
    "is-frozen": false
  }
}
```
