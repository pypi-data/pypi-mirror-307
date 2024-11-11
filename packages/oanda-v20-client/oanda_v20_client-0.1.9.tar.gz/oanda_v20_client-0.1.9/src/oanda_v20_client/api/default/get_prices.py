from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_prices_response_200 import GetPricesResponse200
from ...types import Unset


def _get_kwargs(
    account_id: str,
    *,
    instruments: List[str],
    since: Union[Unset, str] = UNSET,
    include_units_available: Union[Unset, bool] = UNSET,
    include_home_conversions: Union[Unset, bool] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    params: Dict[str, Any] = {}

    json_instruments = instruments

    params["instruments"] = json_instruments

    params["since"] = since

    params["includeUnitsAvailable"] = include_units_available

    params["includeHomeConversions"] = include_home_conversions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{account_id}/pricing".format(
            account_id=account_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetPricesResponse200]]:
    if response.status_code == 200:
        response_200 = GetPricesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
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
) -> Response[Union[Any, GetPricesResponse200]]:
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
    instruments: List[str],
    since: Union[Unset, str] = UNSET,
    include_units_available: Union[Unset, bool] = UNSET,
    include_home_conversions: Union[Unset, bool] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetPricesResponse200]]:
    """Current Account Prices

     Get pricing information for a specified list of Instruments within an Account.

    Args:
        account_id (str):
        instruments (List[str]):
        since (Union[Unset, str]):
        include_units_available (Union[Unset, bool]):
        include_home_conversions (Union[Unset, bool]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPricesResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instruments=instruments,
        since=since,
        include_units_available=include_units_available,
        include_home_conversions=include_home_conversions,
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
    instruments: List[str],
    since: Union[Unset, str] = UNSET,
    include_units_available: Union[Unset, bool] = UNSET,
    include_home_conversions: Union[Unset, bool] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetPricesResponse200]]:
    """Current Account Prices

     Get pricing information for a specified list of Instruments within an Account.

    Args:
        account_id (str):
        instruments (List[str]):
        since (Union[Unset, str]):
        include_units_available (Union[Unset, bool]):
        include_home_conversions (Union[Unset, bool]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPricesResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        instruments=instruments,
        since=since,
        include_units_available=include_units_available,
        include_home_conversions=include_home_conversions,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instruments: List[str],
    since: Union[Unset, str] = UNSET,
    include_units_available: Union[Unset, bool] = UNSET,
    include_home_conversions: Union[Unset, bool] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetPricesResponse200]]:
    """Current Account Prices

     Get pricing information for a specified list of Instruments within an Account.

    Args:
        account_id (str):
        instruments (List[str]):
        since (Union[Unset, str]):
        include_units_available (Union[Unset, bool]):
        include_home_conversions (Union[Unset, bool]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPricesResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instruments=instruments,
        since=since,
        include_units_available=include_units_available,
        include_home_conversions=include_home_conversions,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instruments: List[str],
    since: Union[Unset, str] = UNSET,
    include_units_available: Union[Unset, bool] = UNSET,
    include_home_conversions: Union[Unset, bool] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetPricesResponse200]]:
    """Current Account Prices

     Get pricing information for a specified list of Instruments within an Account.

    Args:
        account_id (str):
        instruments (List[str]):
        since (Union[Unset, str]):
        include_units_available (Union[Unset, bool]):
        include_home_conversions (Union[Unset, bool]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPricesResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            instruments=instruments,
            since=since,
            include_units_available=include_units_available,
            include_home_conversions=include_home_conversions,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
        )
    ).parsed
