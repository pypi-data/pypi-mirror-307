# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..types import client_add_database_column_params
from .._utils import PropertyInfo

__all__ = ["ClientAddDatabaseColumnParams"]


class ClientAddDatabaseColumnParams(TypedDict, total=False):
    column: Required[client_add_database_column_params.Column]

    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]
