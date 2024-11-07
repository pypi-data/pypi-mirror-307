# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Required, TypedDict

__all__ = [
    "TransformCreateParams",
    "TransformParams",
    "TransformParamsOperation",
    "TransformParamsTablePreferences",
    "ValidationParam",
]


class TransformCreateParams(TypedDict, total=False):
    proj_id: Required[str]

    transform_params: Required[TransformParams]

    auth_key: str
    """
    The auth_key parameter is an optional parameter that will be an `Authorization`
    key that will be included in the header of the callback request to the
    `callback_url`. If not provided, the value of transform_name will be None.
    """

    callback_url: str
    """
    The callback_url parameter is an optional parameter that specifies a URL to
    which the transformation results will be sent upon completion. If provided, the
    callback_url parameter should be a valid URL. If not provided, the value of
    transform_name will be None.
    """

    include_reference: bool
    """
    The include_reference parameter is an optional parameter that specifies whether
    to include a reference to the original data in the transformation results. If
    set to True, the transformation results will include a reference to the original
    data. If set to False, the transformation results will not include a reference
    to the original data. The default value is True.
    """

    transform_name: str
    """
    The transform_name parameter is an optional parameter that provides a
    human-readable name or description for the transformation, which can be useful
    for identifying and referencing transformations. If provided, the transform_name
    parameter should be a string. If not provided, the value of transform_name will
    be None.
    """

    validation_params: Iterable[ValidationParam]


class TransformParamsOperation(TypedDict, total=False):
    column_name: Required[str]
    """Name of the column to be transformed.

    Only lower-case letters and underscores or dashes are allowed. No spaces.
    """

    column_type: Required[str]
    """Type of the column to be transformed.

    Must be one of 'boolean', 'numeric', or 'text'
    """

    task_description: Required[str]
    """Description of the task to be performed"""

    transform_type: Required[str]
    """Type of transformation to be applied.

    Must be one of 'extraction', 'classification', or 'generation'
    """

    output_values: Dict[str, str]
    """NOTE: only valid with classifcation tasks.

    Output values of the transformation operation. A dictionary where the keys
    represent the classification bucket and the values represent the classifcation
    meaning. Example: {'likely': 'This is a customer who has said they will make a
    purcahse in the next 30 days', 'unlikely': 'This is a customer who has said they
    will not make a purchase in the next 30 days', 'unsure': 'This is a customer who
    has not committed to anything'}.
    """


class TransformParamsTablePreferences(TypedDict, total=False):
    advanced_reasoning: bool
    """Using advanced reasoning when extracting rows from the tables.

    Transformation becomes slower and more computationally intensive
    """

    included_table_names: List[str]
    """Parameter that specifies the table names to be included for table transforms."""


class TransformParams(TypedDict, total=False):
    model: Required[str]
    """The model to be used for the transformation.

    Must be one of 'trellis-turbo', 'trellis-vertix', 'trellis-warp',
    'trellis-scale', 'trellis-turbo-32k', 'trellis-premium', or 'trellis-enterprise'
    """

    mode: str
    """The mode to be used for the transformation.

    Must be one of 'document' or 'table'
    """

    operations: Iterable[TransformParamsOperation]

    table_preferences: TransformParamsTablePreferences
    """Applicable for table transform mode only.

    Optional parameter that specifies the table names to be included for table
    transforms.
    """


class ValidationParam(TypedDict, total=False):
    validation_columns: Required[List[str]]
    """The columns to be used in validation"""

    validation_name: Required[str]
    """The name of the validation operation"""

    validation_endpoint: str
    """The URL of the validation API.

    If not provided, the validation_rule will be ran directly.
    """

    validation_rule: str
    """The rules to be applied to the column"""
