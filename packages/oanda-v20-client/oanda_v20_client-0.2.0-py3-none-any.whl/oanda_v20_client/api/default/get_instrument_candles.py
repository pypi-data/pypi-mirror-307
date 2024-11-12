from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_instrument_candles_response_200 import (
    GetInstrumentCandlesResponse200,
)
from ...types import Unset


def _get_kwargs(
    instrument: str,
    *,
    price: Union[Unset, str] = UNSET,
    granularity: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    from_: Union[Unset, str] = UNSET,
    to: Union[Unset, str] = UNSET,
    smooth: Union[Unset, bool] = UNSET,
    include_first: Union[Unset, bool] = UNSET,
    daily_alignment: Union[Unset, int] = UNSET,
    alignment_timezone: Union[Unset, str] = UNSET,
    weekly_alignment: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["Authorization"] = authorization

    if not isinstance(accept_datetime_format, Unset):
        headers["Accept-Datetime-Format"] = accept_datetime_format

    params: Dict[str, Any] = {}

    params["price"] = price

    params["granularity"] = granularity

    params["count"] = count

    params["from"] = from_

    params["to"] = to

    params["smooth"] = smooth

    params["includeFirst"] = include_first

    params["dailyAlignment"] = daily_alignment

    params["alignmentTimezone"] = alignment_timezone

    params["weeklyAlignment"] = weekly_alignment

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/instruments/{instrument}/candles".format(
            instrument=instrument,
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetInstrumentCandlesResponse200]]:
    if response.status_code == 200:
        response_200 = GetInstrumentCandlesResponse200.from_dict(response.json())

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
) -> Response[Union[Any, GetInstrumentCandlesResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    price: Union[Unset, str] = UNSET,
    granularity: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    from_: Union[Unset, str] = UNSET,
    to: Union[Unset, str] = UNSET,
    smooth: Union[Unset, bool] = UNSET,
    include_first: Union[Unset, bool] = UNSET,
    daily_alignment: Union[Unset, int] = UNSET,
    alignment_timezone: Union[Unset, str] = UNSET,
    weekly_alignment: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetInstrumentCandlesResponse200]]:
    """Get Candlesticks

     Fetch candlestick data for an instrument.

    Args:
        instrument (str):
        price (Union[Unset, str]):
        granularity (Union[Unset, str]):
        count (Union[Unset, int]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        smooth (Union[Unset, bool]):
        include_first (Union[Unset, bool]):
        daily_alignment (Union[Unset, int]):
        alignment_timezone (Union[Unset, str]):
        weekly_alignment (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetInstrumentCandlesResponse200]]
    """

    kwargs = _get_kwargs(
        instrument=instrument,
        price=price,
        granularity=granularity,
        count=count,
        from_=from_,
        to=to,
        smooth=smooth,
        include_first=include_first,
        daily_alignment=daily_alignment,
        alignment_timezone=alignment_timezone,
        weekly_alignment=weekly_alignment,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    price: Union[Unset, str] = UNSET,
    granularity: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    from_: Union[Unset, str] = UNSET,
    to: Union[Unset, str] = UNSET,
    smooth: Union[Unset, bool] = UNSET,
    include_first: Union[Unset, bool] = UNSET,
    daily_alignment: Union[Unset, int] = UNSET,
    alignment_timezone: Union[Unset, str] = UNSET,
    weekly_alignment: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetInstrumentCandlesResponse200]]:
    """Get Candlesticks

     Fetch candlestick data for an instrument.

    Args:
        instrument (str):
        price (Union[Unset, str]):
        granularity (Union[Unset, str]):
        count (Union[Unset, int]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        smooth (Union[Unset, bool]):
        include_first (Union[Unset, bool]):
        daily_alignment (Union[Unset, int]):
        alignment_timezone (Union[Unset, str]):
        weekly_alignment (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetInstrumentCandlesResponse200]
    """

    return sync_detailed(
        instrument=instrument,
        client=client,
        price=price,
        granularity=granularity,
        count=count,
        from_=from_,
        to=to,
        smooth=smooth,
        include_first=include_first,
        daily_alignment=daily_alignment,
        alignment_timezone=alignment_timezone,
        weekly_alignment=weekly_alignment,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    ).parsed


async def asyncio_detailed(
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    price: Union[Unset, str] = UNSET,
    granularity: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    from_: Union[Unset, str] = UNSET,
    to: Union[Unset, str] = UNSET,
    smooth: Union[Unset, bool] = UNSET,
    include_first: Union[Unset, bool] = UNSET,
    daily_alignment: Union[Unset, int] = UNSET,
    alignment_timezone: Union[Unset, str] = UNSET,
    weekly_alignment: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Response[Union[Any, GetInstrumentCandlesResponse200]]:
    """Get Candlesticks

     Fetch candlestick data for an instrument.

    Args:
        instrument (str):
        price (Union[Unset, str]):
        granularity (Union[Unset, str]):
        count (Union[Unset, int]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        smooth (Union[Unset, bool]):
        include_first (Union[Unset, bool]):
        daily_alignment (Union[Unset, int]):
        alignment_timezone (Union[Unset, str]):
        weekly_alignment (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetInstrumentCandlesResponse200]]
    """

    kwargs = _get_kwargs(
        instrument=instrument,
        price=price,
        granularity=granularity,
        count=count,
        from_=from_,
        to=to,
        smooth=smooth,
        include_first=include_first,
        daily_alignment=daily_alignment,
        alignment_timezone=alignment_timezone,
        weekly_alignment=weekly_alignment,
        authorization=authorization,
        accept_datetime_format=accept_datetime_format,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    instrument: str,
    *,
    client: Union[AuthenticatedClient, Client],
    price: Union[Unset, str] = UNSET,
    granularity: Union[Unset, str] = UNSET,
    count: Union[Unset, int] = UNSET,
    from_: Union[Unset, str] = UNSET,
    to: Union[Unset, str] = UNSET,
    smooth: Union[Unset, bool] = UNSET,
    include_first: Union[Unset, bool] = UNSET,
    daily_alignment: Union[Unset, int] = UNSET,
    alignment_timezone: Union[Unset, str] = UNSET,
    weekly_alignment: Union[Unset, str] = UNSET,
    authorization: str,
    accept_datetime_format: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, GetInstrumentCandlesResponse200]]:
    """Get Candlesticks

     Fetch candlestick data for an instrument.

    Args:
        instrument (str):
        price (Union[Unset, str]):
        granularity (Union[Unset, str]):
        count (Union[Unset, int]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        smooth (Union[Unset, bool]):
        include_first (Union[Unset, bool]):
        daily_alignment (Union[Unset, int]):
        alignment_timezone (Union[Unset, str]):
        weekly_alignment (Union[Unset, str]):
        authorization (str):
        accept_datetime_format (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetInstrumentCandlesResponse200]
    """

    return (
        await asyncio_detailed(
            instrument=instrument,
            client=client,
            price=price,
            granularity=granularity,
            count=count,
            from_=from_,
            to=to,
            smooth=smooth,
            include_first=include_first,
            daily_alignment=daily_alignment,
            alignment_timezone=alignment_timezone,
            weekly_alignment=weekly_alignment,
            authorization=authorization,
            accept_datetime_format=accept_datetime_format,
        )
    ).parsed
