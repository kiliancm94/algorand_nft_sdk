from enum import Enum
from typing import Union

from .arc3 import ARC3
from .arc19 import ARC19


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

    @classmethod
    def get_arc_class(cls, arc_type: str) -> Union[ARC3, ARC19]:
        if arc_type == cls.ARC_3:
            return ARC3
        elif arc_type == cls.ARC_19:
            return ARC19
