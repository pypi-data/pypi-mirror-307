from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.configure_account_body import ConfigureAccountBody
from ...models.configure_account_response_200 import ConfigureAccountResponse200
from ...models.configure_account_response_400 import ConfigureAccountResponse400
from ...models.configure_account_response_403 import ConfigureAccountResponse403
from ...types import Unset


def _get_kwargs(
    account_id: str,
    *,
    body: ConfigureAccountBody,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": "/accounts/{account_id}/configuration".format(
            account_id=account_id,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
    if response.status_code == 200:
        response_200 = ConfigureAccountResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ConfigureAccountResponse400.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = ConfigureAccountResponse403.from_dict(response.json())

        return response_403
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
) -> Response[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
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
    body: ConfigureAccountBody,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
    """Configure Account

     Set the client-configurable portions of an Account.

    Args:
        account_id (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        body (ConfigureAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConfigureAccountResponse200, ConfigureAccountResponse400, ConfigureAccountResponse403]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        body=body,
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
    body: ConfigureAccountBody,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
    """Configure Account

     Set the client-configurable portions of an Account.

    Args:
        account_id (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        body (ConfigureAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConfigureAccountResponse200, ConfigureAccountResponse400, ConfigureAccountResponse403]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        body=body,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ConfigureAccountBody,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
    """Configure Account

     Set the client-configurable portions of an Account.

    Args:
        account_id (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        body (ConfigureAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ConfigureAccountResponse200, ConfigureAccountResponse400, ConfigureAccountResponse403]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        body=body,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ConfigureAccountBody,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Any,
        ConfigureAccountResponse200,
        ConfigureAccountResponse400,
        ConfigureAccountResponse403,
    ]
]:
    """Configure Account

     Set the client-configurable portions of an Account.

    Args:
        account_id (str):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):
        body (ConfigureAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ConfigureAccountResponse200, ConfigureAccountResponse400, ConfigureAccountResponse403]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            body=body,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
        )
    ).parsed
