# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["TransformUpdateParams"]


class TransformUpdateParams(TypedDict, total=False):
    _job_id: str

    auth_key: str

    callback_url: str

    include_reference: bool
