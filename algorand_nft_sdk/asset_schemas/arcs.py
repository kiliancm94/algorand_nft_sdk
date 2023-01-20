from enum import Enum
from pydantic import BaseModel

from .arc3 import ARC3


class ARCType(str, Enum):
    """
    Standards for NFT of Algorand Network. You can find each specifications
    in the following link:
    https://github.com/algorandfoundation/ARCs/blob/main/ARCs/
    """

    ARC_3 = "arc3"
    ARC_18 = "arc18"
    ARC_19 = "arc19"
    ARC_20 = "arc20"
    ARC_69 = "arc69"


class ARC(BaseModel):
    arc: ARC3
