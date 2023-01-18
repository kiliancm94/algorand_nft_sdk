import base64
import hashlib
import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator, AnyUrl

from algorand_nft_sdk.utils.logger import get_logger
from algorand_nft_sdk.nft import exceptions
import requests


log = get_logger()
ARC3_URL: str = "https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md"


class ARC3(BaseModel):
    unit_name: Optional[str]
    asset_name: Optional[str]
    asset_url: Optional[AnyUrl]
    asset_metadata_hash: Optional[str]

    @validator("asset_name")
    def validate_asset_name(cls, v: str) -> str:
        if v == "arc3" or v.endswith("@arc3"):
            log.warning(
                f"Asset name contains conventions NOT RECOMMENDED, please check {ARC3_URL}"
            )
        return v

    @validator("asset_url")
    def validate_asset_url(cls, v: str, values: dict):
        if "{id}" not in v:
            try:
                response = requests.get(v.rstrip("#arc3"))
                if not response.ok:
                    log.warning(
                        f"Error downloading asset url, asset url SHOULD be downloadable, please check {ARC3_URL}"
                    )
            except Exception as error:
                log.error(error)
                log.warning(
                    f"Error downloading asset url, asset url SHOULD be downloadable, please check {ARC3_URL}"
                )
        else:
            log.warning(
                "Validation of url download skipped because the url contains '{id}'"
            )

        if not "https" in v or not "ipfs" in v:
            log.warning(f"The url should be https or ipfs, check {ARC3_URL}")

        asset_name = values.get("asset_name")
        if asset_name != "arc3" or not asset_name.endswith("@arc3"):
            if not v.endswith("#arc3"):
                raise exceptions.ValueErrorAssetUrl(
                    f"Asset name must end with #arc3 based on your asset_name, please check {ARC3_URL}"
                )
        return v


class LocalizationParams(BaseModel):
    uri: str
    default: str
    locales: list[str]
    integrity: Optional[dict]


class ARC3Metadata(BaseModel):
    name: Optional[str]
    decimals: Optional[int]
    description: Optional[str]
    image: Optional[AnyUrl]
    image_integrity: Optional[str]
    image_mimetype: Optional[str]
    background_color: Optional[str]
    external_url: Optional[AnyUrl]
    animation_url: Optional[AnyUrl]
    animation_url_integrity: Optional[str]
    animation_url_mimetype: Optional[str]
    properties: Optional[dict]
    extra_metadata: Optional[str]
    localization: Optional[LocalizationParams]

    @validator("extra_metadata")
    def validate_base65(cls, v) -> str:
        try:
            base64.b64decode(v)
            return v
        except:
            raise ValueError("extra_metadata field must be a string in base64")

    @validator("background_color")
    def validate_background_color(cls, v: str):
        if not v.startswith("#"):
            raise ValueError(
                f"background_color must start with '#', please check {ARC3_URL}"
            )
        return v


def calculate_hash_metadata(arc3_metadata: ARC3Metadata) -> bytes:
    h = hashlib.new("sha512_256")
    h.update(b"arc0003/amj")
    h.update(json.dumps(arc3_metadata.to_dict().encode("utf-8")))
    json_metadata_hash = h.digest()
    h = hashlib.new("sha512_256")
    h.update(b"arc0003/am")
    h.update(json_metadata_hash)
    h.update(base64.b64decode(arc3_metadata.extra_metadata))
    am = h.digest()

    return base64.b64encode(am).decode("utf-8")
