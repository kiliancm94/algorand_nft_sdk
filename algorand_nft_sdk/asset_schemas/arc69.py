from typing import Dict, Literal, Optional

from pydantic import AnyUrl, BaseModel, validator

from algorand_nft_sdk.core import exceptions
from algorand_nft_sdk.utils.logger import get_logger

log = get_logger()
ARC69_URL: str = "https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0069.md"
ARC69_ASSET_URL_SUFFIXES = ("#i", "#v", "#a", "#p", "#h")


class ARC69(BaseModel):
    unit_name: Optional[str]
    asset_name: Optional[str]
    asset_url: Optional[AnyUrl]
    asset_metadata_hash: Optional[str]

    @validator("asset_url")
    def validate_asset_url(cls, v: str, values: dict) -> str:
        if " " in v:
            raise exceptions.ValueErrorAssetUrl(
                f"asset_url must not contain whitespaces, please check {ARC69_URL}"
            )

        if not v.endswith(ARC69_ASSET_URL_SUFFIXES) and v[-2] == "#":
            raise exceptions.ValueErrorAssetUrl(
                f"Suffix not supported, supported suffixes are {ARC69_ASSET_URL_SUFFIXES}"
            )

        if v.startswith("http://"):
            log.warning(f"Consider use https instead of http for security reasons.")

        return v


class ARC69Metadata(BaseModel):
    standard: Literal["arc69"]
    description: Optional[str]
    external_url: Optional[AnyUrl]
    media_url: Optional[AnyUrl]
    mime_type: Optional[AnyUrl]
    attributes: Optional[list]
    properties: Optional[Dict[str, str]]
