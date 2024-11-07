# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["AssetsExtractExtractParams"]


class AssetsExtractExtractParams(TypedDict, total=False):
    asset_ids: List[str]

    auth_key: str

    callback_url: str

    log_level: Literal["verbose", "concise"]
    """An enumeration."""

    parse_strategy: Literal["optimized", "ocr", "markdown", "xml"]
    """An enumeration."""

    proj_id: str

    run_on_all_assets: bool
