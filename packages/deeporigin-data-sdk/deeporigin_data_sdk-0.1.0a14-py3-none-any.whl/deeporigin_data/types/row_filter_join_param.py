# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "RowFilterJoinParam",
    "Condition",
    "ConditionRowFilterText",
    "ConditionRowFilterNumber",
    "ConditionRowFilterBoolean",
    "ConditionRowFilterNullity",
    "ConditionRowFilterSet",
    "ConditionRowFilterSubstructure",
]


class ConditionRowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "contains", "notContains", "startsWith", "endsWith"]]


class ConditionRowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal["equals", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"]
    ]


class ConditionRowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual"]]


class ConditionRowFilterNullity(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["nullity"], PropertyInfo(alias="filterType")]]

    operator: Required[Literal["isNull", "isNotNull"]]


class ConditionRowFilterSet(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["set"], PropertyInfo(alias="filterType")]]

    values: Required[Iterable[None]]


class ConditionRowFilterSubstructure(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["substructure"], PropertyInfo(alias="filterType")]]

    substructure: Required[str]
    """A SMARTS or SMILES string to match against."""


Condition: TypeAlias = Union[
    ConditionRowFilterText,
    ConditionRowFilterNumber,
    ConditionRowFilterBoolean,
    ConditionRowFilterNullity,
    ConditionRowFilterSet,
    ConditionRowFilterSubstructure,
    RowFilterJoinParam,
]


class RowFilterJoinParam(TypedDict, total=False):
    conditions: Required[Iterable[Condition]]

    filter_type: Required[Annotated[Literal["join"], PropertyInfo(alias="filterType")]]

    join_type: Required[Annotated[Literal["and", "or"], PropertyInfo(alias="joinType")]]
