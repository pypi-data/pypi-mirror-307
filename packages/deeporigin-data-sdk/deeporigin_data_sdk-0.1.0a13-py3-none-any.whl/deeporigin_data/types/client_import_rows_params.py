# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ..types import client_import_rows_params
from .._utils import PropertyInfo

__all__ = ["ClientImportRowsParams"]


class ClientImportRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    add_columns: Annotated[Iterable[client_import_rows_params.AddColumn], PropertyInfo(alias="addColumns")]
    """Optionally add additional columns to the database during import."""

    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]
