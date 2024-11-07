# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ActionCreateParams", "Action"]


class ActionCreateParams(TypedDict, total=False):
    actions: Required[Iterable[Action]]


class Action(TypedDict, total=False):
    transform_id: Required[str]

    type: Required[Literal["refresh_transform", "run_extraction"]]
    """An enumeration."""
