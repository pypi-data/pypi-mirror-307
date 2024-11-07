# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["Usage", "ProjectUsage"]


class ProjectUsage(BaseModel):
    proj_id: str

    proj_name: str

    total_assets: int

    total_transformations: int

    total_usage: int


class Usage(BaseModel):
    cust_id: str

    project_usage: List[ProjectUsage]

    total_files: int

    total_records: int

    total_usage: int

    usage: List[Usage]
