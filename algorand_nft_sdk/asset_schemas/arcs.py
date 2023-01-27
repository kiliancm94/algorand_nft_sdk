from enum import Enum
from typing import Union

from .arc3 import ARC3, ARC3Metadata
from .arc19 import ARC19
from .arc69 import ARC69, ARC69Metadata


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
    def get_arc_class(cls, arc_type: str) -> Union[ARC3, ARC19, ARC69]:
        if arc_type == cls.ARC_3:
            return ARC3
        elif arc_type == cls.ARC_19:
            return ARC19
        elif arc_type == cls.ARC_69:
            return ARC69
        else:
            raise ValueError(
                f"arc_type not supported, supported values are {SUPPORTED_ARC_TYPES}"
            )

    @classmethod
    def get_arc_metadata_validator(
        cls, arc_type: str
    ) -> Union[ARC3Metadata, ARC69Metadata]:
        if arc_type == cls.ARC_3 or arc_type == cls.ARC_19:
            return ARC3Metadata
        elif arc_type == cls.ARC_69:
            return ARC69Metadata
        else:
            raise ValueError(
                f"arc_type not supported, supported values are {SUPPORTED_ARC_TYPES}"
            )


SUPPORTED_ARC_TYPES = {ARCType.ARC_3, ARCType.ARC_19, ARCType.ARC_69}
