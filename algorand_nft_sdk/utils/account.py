from typing import Optional
from algosdk.account import address_from_private_key, generate_account


class Account:
    def __init__(
        self, private_key: Optional[str] = None, address: Optional[str] = None
    ) -> None:
        if private_key:
            self.private_key = private_key
            self.address = address_from_private_key(private_key=private_key)
        elif not (private_key and address):
            self.private_key, self.address = generate_account()
        else:
            self.private_key = None
            self.address = address

    def __str__(self) -> str:
        return f"private_address: {self.private_key if not self.private_key else '*********'}, address: {self.address}"
