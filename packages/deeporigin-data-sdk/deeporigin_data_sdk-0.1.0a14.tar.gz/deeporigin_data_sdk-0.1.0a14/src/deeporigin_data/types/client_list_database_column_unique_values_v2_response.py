# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ClientListDatabaseColumnUniqueValuesV2Response", "Data"]


class Data(BaseModel):
    name: Optional[str] = None

    value: Optional[str] = None


class ClientListDatabaseColumnUniqueValuesV2Response(BaseModel):
    data: List[Data]
