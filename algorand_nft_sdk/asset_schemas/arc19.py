from pydantic import AnyUrl, BaseModel, validator
from typing import Literal, Optional

from algorand_nft_sdk.asset_schemas.arc3 import ARC3
from algorand_nft_sdk.nft import exceptions
from multihash.constants import HASH_CODES

ARC19_URL = "https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0019.md"
ARC19_URL_VERSIONS = {0, 1}
ARC19_URL_MULTICODECS = {"raw", "dag-pb"}
ARC19_URL_FIELD_NAME = "reserve"


class ARC19(ARC3, BaseModel):
    """
    ARC 19 class validator, inherates from ARC3.
    There is an example of asset_url of this ARC19 here: https://testnet.algoexplorer.io/asset/66753108
    """

    asset_url: Optional[str]

    @validator("asset_url")
    def validate_asset_url(cls, v: str) -> str:
        if not v:
            return v

        if not v.startswith("template-ipfs://{ipfscid"):
            raise exceptions.ValueErrorAssetUrl(
                "asset_url must start with 'template-ipfs://{ipfscid', "
                f"please check {ARC19_URL}"
            )

        split_url = v.split("{")[-1].rstrip("}").split(":")
        if len(split_url) < 5:
            raise ValueError(
                f"URL is not formatted correctly, please check {ARC19_URL}"
            )
        (_, version, multicodec_content_type, field_name, hash_type, *_) = split_url

        if int(version) not in ARC19_URL_VERSIONS:
            raise exceptions.VersionError(
                f"The version {version} is not supported. Supported versions are {ARC19_URL_VERSIONS}"
            )
        if multicodec_content_type not in ARC19_URL_MULTICODECS:
            raise ValueError(
                f"Multicoded {multicodec_content_type} not supported. Supported values are {ARC19_URL_MULTICODECS}"
            )
        if field_name != ARC19_URL_FIELD_NAME:
            raise ValueError(f"Field name must be {ARC19_URL_FIELD_NAME}")
        if hash_type not in HASH_CODES:
            raise ValueError(f"Hash type not compatible, please check {ARC19_URL}")

        return v
