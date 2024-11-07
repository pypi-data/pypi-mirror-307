# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["TransformAutoschemaResponse", "Data", "Metadata"]


class Data(BaseModel):
    id: Optional[str] = None

    column_name: Optional[str] = None

    column_type: Optional[str] = None

    task_description: Optional[str] = None

    transform_type: Optional[str] = None


class Metadata(BaseModel):
    total_generated: int


class TransformAutoschemaResponse(BaseModel):
    data: List[Data]

    message: str

    metadata: Metadata
