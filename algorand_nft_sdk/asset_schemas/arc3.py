import base64
import hashlib
import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from algorand_nft_sdk.utils.logger import get_logger


class ARC3(BaseModel):
    unit_name: str
    asset_name: str
    asset_url: str
    asset_metadata_hash: Optional[str]


class LocalizationParams(BaseModel):
    uri: str
    default: str
    locales: list[str]
    integrity: Optional[dict]


class ARC3Metadata(BaseModel):
    name: Optional[str]
    decimals: Optional[int]
    description: Optional[str]
    image: Optional[str]
    image_integrity: Optional[str]
    image_mimetype: Optional[str]
    background_color: Optional[str]
    external_url: Optional[str]
    animation_url: Optional[str]
    animation_url_integrity: Optional[str]
    animation_url_mimetype: Optional[str]
    properties: Optional[str]
    extra_metadata: Optional[str]
    localization: Optional[LocalizationParams]

    @validator("extra_metadata")
    def validate_base65(cls, v) -> str:
        try:
            base64.b64decode(v)
            return v
        except:
            raise ValueError("extra_metadata field must be a string in base64")


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
