# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["TransformSummarizeParams"]


class TransformSummarizeParams(TypedDict, total=False):
    operation_ids: Required[List[str]]
    """The columns to be summarized"""

    result_ids: List[str]
    """The IDs of the results to be summarized"""
