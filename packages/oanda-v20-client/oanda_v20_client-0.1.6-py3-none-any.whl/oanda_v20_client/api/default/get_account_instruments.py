from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_account_instruments_response_200 import (
    GetAccountInstrumentsResponse200,
)
from ...types import Unset


def _get_kwargs(
    account_id: str,
    *,
    instruments: Union[Unset, List[str]] = UNSET,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    params: Dict[str, Any] = {}

    json_instruments: Union[Unset, List[str]] = UNSET
    if not isinstance(instruments, Unset):
        json_instruments = instruments

    params["instruments"] = json_instruments

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{account_id}/instruments".format(
            account_id=account_id,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetAccountInstrumentsResponse200]]:
    if response.status_code == 200:
        response_200 = GetAccountInstrumentsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 405:
        response_405 = cast(Any, None)
        return response_405
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetAccountInstrumentsResponse200]]:
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
    instruments: Union[Unset, List[str]] = UNSET,
    authorization: str,
) -> Response[Union[Any, GetAccountInstrumentsResponse200]]:
    """Account Instruments

     Get the list of tradeable instruments for the given Account. The list of tradeable instruments is
    dependent on the regulatory division that the Account is located in, thus should be the same for all
    Accounts owned by a single user.

    Args:
        account_id (str):
        instruments (Union[Unset, List[str]]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAccountInstrumentsResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instruments=instruments,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instruments: Union[Unset, List[str]] = UNSET,
    authorization: str,
) -> Optional[Union[Any, GetAccountInstrumentsResponse200]]:
    """Account Instruments

     Get the list of tradeable instruments for the given Account. The list of tradeable instruments is
    dependent on the regulatory division that the Account is located in, thus should be the same for all
    Accounts owned by a single user.

    Args:
        account_id (str):
        instruments (Union[Unset, List[str]]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAccountInstrumentsResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        instruments=instruments,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instruments: Union[Unset, List[str]] = UNSET,
    authorization: str,
) -> Response[Union[Any, GetAccountInstrumentsResponse200]]:
    """Account Instruments

     Get the list of tradeable instruments for the given Account. The list of tradeable instruments is
    dependent on the regulatory division that the Account is located in, thus should be the same for all
    Accounts owned by a single user.

    Args:
        account_id (str):
        instruments (Union[Unset, List[str]]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAccountInstrumentsResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instruments=instruments,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    instruments: Union[Unset, List[str]] = UNSET,
    authorization: str,
) -> Optional[Union[Any, GetAccountInstrumentsResponse200]]:
    """Account Instruments

     Get the list of tradeable instruments for the given Account. The list of tradeable instruments is
    dependent on the regulatory division that the Account is located in, thus should be the same for all
    Accounts owned by a single user.

    Args:
        account_id (str):
        instruments (Union[Unset, List[str]]):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAccountInstrumentsResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            instruments=instruments,
            authorization=authorization,
        )
    ).parsed
