from pydantic import AnyUrl, validator
from typing import Literal, Optional

from algorand_nft_sdk.asset_schemas.arc3 import ARC3
from algorand_nft_sdk.nft import exceptions

ARC19_URL = "https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md"


class ARC19(ARC3):
    arc_type: Literal["arc19"]
    asset_url: Optional[AnyUrl]

    @validator("arc_type")
    def change_arc_type(cls, v: str) -> str:
        return "arc3"

    @validator("asset_url")
    def validate_asset_url(cls, v: AnyUrl) -> AnyUrl:
        if not v:
            return v

        if not v.startswith("template"):
            raise exceptions.ValueErrorAssetUrl(
                f"asst_url must start with template, please check {ARC19_URL}"
            )
        return v
