from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_trade_response_200 import GetTradeResponse200
from ...types import Unset


def _get_kwargs(
    account_id: str,
    trade_specifier: str,
    *,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{account_id}/trades/{trade_specifier}".format(
            account_id=account_id,
            trade_specifier=trade_specifier,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetTradeResponse200]]:
    if response.status_code == 200:
        response_200 = GetTradeResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
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
) -> Response[Union[Any, GetTradeResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    trade_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetTradeResponse200]]:
    """Trade Details

     Get the details of a specific Trade in an Account

    Args:
        account_id (str):
        trade_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetTradeResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        trade_specifier=trade_specifier,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    trade_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetTradeResponse200]]:
    """Trade Details

     Get the details of a specific Trade in an Account

    Args:
        account_id (str):
        trade_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetTradeResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        trade_specifier=trade_specifier,
        client=client,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    trade_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetTradeResponse200]]:
    """Trade Details

     Get the details of a specific Trade in an Account

    Args:
        account_id (str):
        trade_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetTradeResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        trade_specifier=trade_specifier,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    trade_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetTradeResponse200]]:
    """Trade Details

     Get the details of a specific Trade in an Account

    Args:
        account_id (str):
        trade_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetTradeResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            trade_specifier=trade_specifier,
            client=client,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
        )
    ).parsed
