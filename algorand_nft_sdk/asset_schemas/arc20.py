from pydantic import BaseModel

AR20_URL = "https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0020.md"


class ARC20(BaseModel):
    default_frozen: bool = True
    clawback_address: str
    # todo: cehck and understand https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0020.md#specifying-the-controlling-smart-contract
