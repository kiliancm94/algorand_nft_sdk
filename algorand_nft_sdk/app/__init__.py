import os
from algosdk.v2client import algod

ALGOD_ADDRESS = os.getenv("ALGOD_API_URL")
ALGOD_API_KEY = os.getenv("ALGOD_API_KEY")

if not (ALGOD_ADDRESS and ALGOD_API_KEY):
    raise EnvironmentError(
        f"Environment variables ALGOD_API_URL and ALGOD_API_KEY must be configured."
    )
algod_client = algod.AlgodClient(
    "", ALGOD_ADDRESS, headers={"X-API-Key": ALGOD_API_KEY}
)
