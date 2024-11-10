from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_orders_response_200 import ListOrdersResponse200
from ...types import Unset


def _get_kwargs(
    account_id: str,
    *,
    ids: Union[Unset, List[str]] = UNSET,
    state: Union[Unset, str] = UNSET,
    instrument: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    before_id: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    params: Dict[str, Any] = {}

    json_ids: Union[Unset, List[str]] = UNSET
    if not isinstance(ids, Unset):
        json_ids = ids

    params["ids"] = json_ids

    params["state"] = state

    params["instrument"] = instrument

    params["count"] = count

    params["beforeID"] = before_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{account_id}/orders".format(
            account_id=account_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ListOrdersResponse200]]:
    if response.status_code == 200:
        response_200 = ListOrdersResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 405:
        response_405 = cast(Any, None)
        return response_405
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ListOrdersResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    ids: Union[Unset, List[str]] = UNSET,
    state: Union[Unset, str] = UNSET,
    instrument: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    before_id: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ListOrdersResponse200]]:
    """List Orders

     Get a list of Orders for an Account

    Args:
        account_id (str):
        ids (Union[Unset, List[str]]):
        state (Union[Unset, str]):
        instrument (Union[Unset, str]):
        count (Union[Unset, int]):
        before_id (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListOrdersResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        ids=ids,
        state=state,
        instrument=instrument,
        count=count,
        before_id=before_id,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    ids: Union[Unset, List[str]] = UNSET,
    state: Union[Unset, str] = UNSET,
    instrument: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    before_id: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ListOrdersResponse200]]:
    """List Orders

     Get a list of Orders for an Account

    Args:
        account_id (str):
        ids (Union[Unset, List[str]]):
        state (Union[Unset, str]):
        instrument (Union[Unset, str]):
        count (Union[Unset, int]):
        before_id (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListOrdersResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        ids=ids,
        state=state,
        instrument=instrument,
        count=count,
        before_id=before_id,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    ids: Union[Unset, List[str]] = UNSET,
    state: Union[Unset, str] = UNSET,
    instrument: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    before_id: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ListOrdersResponse200]]:
    """List Orders

     Get a list of Orders for an Account

    Args:
        account_id (str):
        ids (Union[Unset, List[str]]):
        state (Union[Unset, str]):
        instrument (Union[Unset, str]):
        count (Union[Unset, int]):
        before_id (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListOrdersResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        ids=ids,
        state=state,
        instrument=instrument,
        count=count,
        before_id=before_id,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    ids: Union[Unset, List[str]] = UNSET,
    state: Union[Unset, str] = UNSET,
    instrument: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    before_id: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ListOrdersResponse200]]:
    """List Orders

     Get a list of Orders for an Account

    Args:
        account_id (str):
        ids (Union[Unset, List[str]]):
        state (Union[Unset, str]):
        instrument (Union[Unset, str]):
        count (Union[Unset, int]):
        before_id (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListOrdersResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            ids=ids,
            state=state,
            instrument=instrument,
            count=count,
            before_id=before_id,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
        )
    ).parsed
