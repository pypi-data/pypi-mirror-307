# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["AssetUploadParams"]


class AssetUploadParams(TypedDict, total=False):
    asset_ids: List[str]

    chunk_strategy: str

    ext_file_names: List[str]

    ext_ids: List[str]

    file_type: str

    file_types: List[str]

    include_header: bool

    main_keys: List[str]

    proj_id: str

    urls: List[str]
