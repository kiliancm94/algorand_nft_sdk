# Algorand NFT SDK

Welcome to the Algorand NFT SDK! The Algorand NFT SDK is software to help you to manage and interact with Algorand Non-Fungible Tokens (NFTs) in the Algorand network. The project comes in 2 flavours, one is more for developers and the other one for non-developers. The first flavour is a Python package that you can use for managing the NFTs by coding and use it for your own applications. The second flavour is a command line interface (CLI).

## Motivation

The main motivation of this project is to provide great tooling to help developers and non-developers to manage their NFTs in the Algorand network by minimizing the learning curve. And of course, to have fun while building for others and learning about a great project, Algorand.

## How to use CLI

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
  get-address-from-private-key
  mint-nft-arc
  optin-nft-arc
  transfer-nft-arc
  update-nft-arc
```


### Installing the CLI

To install the CLI you need to donwload first git package, you can clone it by executing the next command in the

TODO:
[x] Finished with ARC3
[x] Repair when do anything that is not creating a token and it fails because
 of missing paramters
[x] Change the current NFT class to decide the ARC type
[x] Change how we decide the type to avoid issues with pydantic, better one function to decide the type.
[x] ARC19
[ ] ARC20 -- Pending
[ ] ARC18 -- Pending
[x] ARC69
[x] Solve the issues with update nft method. Now it is failing because the address provided
should be Address, not str. Check it.
[x] Add tests
[x] Improve the naming of the libraries
[ ] Create the documentation
[ ] Create the video
[x] Add license
[ ] Add contributors file

[ ] Extra! Needs to confirm where should be located the metadata json file

How to create a pip package https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
