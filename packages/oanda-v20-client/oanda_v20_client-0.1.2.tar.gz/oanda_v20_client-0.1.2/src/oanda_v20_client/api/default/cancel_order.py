from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.cancel_order_response_200 import CancelOrderResponse200
from ...models.cancel_order_response_404 import CancelOrderResponse404
from ...types import Unset


def _get_kwargs(
    account_id: str,
    order_specifier: str,
    *,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
    client_request_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    if not isinstance(client_request_id, Unset):
        headers["ClientRequestID"] = client_request_id

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/accounts/{account_id}/orders/{order_specifier}/cancel".format(
            account_id=account_id,
            order_specifier=order_specifier,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    if response.status_code == 200:
        response_200 = CancelOrderResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = CancelOrderResponse404.from_dict(response.json())

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
) -> Response[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    order_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
    client_request_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    """Cancel Order

     Cancel a pending Order in an Account

    Args:
        account_id (str):
        order_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        client_request_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        order_specifier=order_specifier,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
        client_request_id=client_request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    order_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
    client_request_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    """Cancel Order

     Cancel a pending Order in an Account

    Args:
        account_id (str):
        order_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        client_request_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CancelOrderResponse200, CancelOrderResponse404]
    """

    return sync_detailed(
        account_id=account_id,
        order_specifier=order_specifier,
        client=client,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
        client_request_id=client_request_id,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    order_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
    client_request_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    """Cancel Order

     Cancel a pending Order in an Account

    Args:
        account_id (str):
        order_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        client_request_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        order_specifier=order_specifier,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
        client_request_id=client_request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    order_specifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
    client_request_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, CancelOrderResponse200, CancelOrderResponse404]]:
    """Cancel Order

     Cancel a pending Order in an Account

    Args:
        account_id (str):
        order_specifier (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        client_request_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CancelOrderResponse200, CancelOrderResponse404]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            order_specifier=order_specifier,
            client=client,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
            client_request_id=client_request_id,
        )
    ).parsed
