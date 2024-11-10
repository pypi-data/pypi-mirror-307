# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ListDatabaseColumnUniqueValuesResponse", "Data"]


class Data(BaseModel):
    name: Optional[str] = None

    value: Optional[str] = None


class ListDatabaseColumnUniqueValuesResponse(BaseModel):
    data: List[Data]
