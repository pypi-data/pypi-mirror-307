# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import (
    client_describe_database_params,
    client_describe_workspace_params,
    client_list_database_column_unique_values_v2_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.client_describe_database_response import ClientDescribeDatabaseResponse
from ..types.client_describe_workspace_response import ClientDescribeWorkspaceResponse
from ..types.client_list_database_column_unique_values_v2_response import ClientListDatabaseColumnUniqueValuesV2Response

__all__ = ["ClientResource", "AsyncClientResource"]


class ClientResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ClientResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deeporiginbio/deeporigin-data-sdk#accessing-raw-response-data-eg-headers
        """
        return ClientResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClientResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deeporiginbio/deeporigin-data-sdk#with_streaming_response
        """
        return ClientResourceWithStreamingResponse(self)

    def describe_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientDescribeDatabaseResponse:
        """
        Describe a database

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/DescribeDatabase",
            body=maybe_transform(
                {"database_id": database_id}, client_describe_database_params.ClientDescribeDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientDescribeDatabaseResponse,
        )

    def describe_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientDescribeWorkspaceResponse:
        """
        Describe a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/DescribeWorkspace",
            body=maybe_transform(
                {"workspace_id": workspace_id}, client_describe_workspace_params.ClientDescribeWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientDescribeWorkspaceResponse,
        )

    def list_database_column_unique_values_v2(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientListDatabaseColumnUniqueValuesV2Response:
        """
        Returns the unique values for every cell within the column.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/ListDatabaseColumnUniqueValuesV2",
            body=maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_list_database_column_unique_values_v2_params.ClientListDatabaseColumnUniqueValuesV2Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientListDatabaseColumnUniqueValuesV2Response,
        )


class AsyncClientResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncClientResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deeporiginbio/deeporigin-data-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncClientResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClientResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deeporiginbio/deeporigin-data-sdk#with_streaming_response
        """
        return AsyncClientResourceWithStreamingResponse(self)

    async def describe_database(
        self,
        *,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientDescribeDatabaseResponse:
        """
        Describe a database

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/DescribeDatabase",
            body=await async_maybe_transform(
                {"database_id": database_id}, client_describe_database_params.ClientDescribeDatabaseParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientDescribeDatabaseResponse,
        )

    async def describe_workspace(
        self,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientDescribeWorkspaceResponse:
        """
        Describe a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/DescribeWorkspace",
            body=await async_maybe_transform(
                {"workspace_id": workspace_id}, client_describe_workspace_params.ClientDescribeWorkspaceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientDescribeWorkspaceResponse,
        )

    async def list_database_column_unique_values_v2(
        self,
        *,
        column_id: str,
        database_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientListDatabaseColumnUniqueValuesV2Response:
        """
        Returns the unique values for every cell within the column.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/ListDatabaseColumnUniqueValuesV2",
            body=await async_maybe_transform(
                {
                    "column_id": column_id,
                    "database_id": database_id,
                },
                client_list_database_column_unique_values_v2_params.ClientListDatabaseColumnUniqueValuesV2Params,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ClientListDatabaseColumnUniqueValuesV2Response,
        )


class ClientResourceWithRawResponse:
    def __init__(self, client: ClientResource) -> None:
        self._client = client

        self.describe_database = to_raw_response_wrapper(
            client.describe_database,
        )
        self.describe_workspace = to_raw_response_wrapper(
            client.describe_workspace,
        )
        self.list_database_column_unique_values_v2 = to_raw_response_wrapper(
            client.list_database_column_unique_values_v2,
        )


class AsyncClientResourceWithRawResponse:
    def __init__(self, client: AsyncClientResource) -> None:
        self._client = client

        self.describe_database = async_to_raw_response_wrapper(
            client.describe_database,
        )
        self.describe_workspace = async_to_raw_response_wrapper(
            client.describe_workspace,
        )
        self.list_database_column_unique_values_v2 = async_to_raw_response_wrapper(
            client.list_database_column_unique_values_v2,
        )


class ClientResourceWithStreamingResponse:
    def __init__(self, client: ClientResource) -> None:
        self._client = client

        self.describe_database = to_streamed_response_wrapper(
            client.describe_database,
        )
        self.describe_workspace = to_streamed_response_wrapper(
            client.describe_workspace,
        )
        self.list_database_column_unique_values_v2 = to_streamed_response_wrapper(
            client.list_database_column_unique_values_v2,
        )


class AsyncClientResourceWithStreamingResponse:
    def __init__(self, client: AsyncClientResource) -> None:
        self._client = client

        self.describe_database = async_to_streamed_response_wrapper(
            client.describe_database,
        )
        self.describe_workspace = async_to_streamed_response_wrapper(
            client.describe_workspace,
        )
        self.list_database_column_unique_values_v2 = async_to_streamed_response_wrapper(
            client.list_database_column_unique_values_v2,
        )
