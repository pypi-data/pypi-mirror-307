from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.get_position_response_200 import GetPositionResponse200


def _get_kwargs(
    account_id: str,
    instrument: str,
    *,
    authorization: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/accounts/{account_id}/positions/{instrument}".format(
            account_id=account_id,
            instrument=instrument,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetPositionResponse200]]:
    if response.status_code == 200:
        response_200 = GetPositionResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetPositionResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
) -> Response[Union[Any, GetPositionResponse200]]:
    """Instrument Position

     Get the details of a single Instrument's Position in an Account. The Position may by open or not.

    Args:
        account_id (str):
        instrument (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPositionResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instrument=instrument,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
) -> Optional[Union[Any, GetPositionResponse200]]:
    """Instrument Position

     Get the details of a single Instrument's Position in an Account. The Position may by open or not.

    Args:
        account_id (str):
        instrument (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPositionResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        instrument=instrument,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
) -> Response[Union[Any, GetPositionResponse200]]:
    """Instrument Position

     Get the details of a single Instrument's Position in an Account. The Position may by open or not.

    Args:
        account_id (str):
        instrument (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetPositionResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        instrument=instrument,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
) -> Optional[Union[Any, GetPositionResponse200]]:
    """Instrument Position

     Get the details of a single Instrument's Position in an Account. The Position may by open or not.

    Args:
        account_id (str):
        instrument (str):
        authorization (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetPositionResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            instrument=instrument,
            client=client,
            authorization=authorization,
        )
    ).parsed
