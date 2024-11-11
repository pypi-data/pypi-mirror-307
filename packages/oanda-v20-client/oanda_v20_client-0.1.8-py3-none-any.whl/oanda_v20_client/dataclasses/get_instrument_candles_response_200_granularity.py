from __future__ import annotations
from typing import Literal, Set, cast

GetInstrumentCandlesResponse200Granularity = Literal[
    "D",
    "H1",
    "H12",
    "H2",
    "H3",
    "H4",
    "H6",
    "H8",
    "M",
    "M1",
    "M10",
    "M15",
    "M2",
    "M30",
    "M4",
    "M5",
    "S10",
    "S15",
    "S30",
    "S5",
    "W",
]
GET_INSTRUMENT_CANDLES_RESPONSE_200_GRANULARITY_VALUES: Set[
    GetInstrumentCandlesResponse200Granularity
] = {
    "D",
    "H1",
    "H12",
    "H2",
    "H3",
    "H4",
    "H6",
    "H8",
    "M",
    "M1",
    "M10",
    "M15",
    "M2",
    "M30",
    "M4",
    "M5",
    "S10",
    "S15",
    "S30",
    "S5",
    "W",
}


def check_get_instrument_candles_response_200_granularity(
    value: str,
) -> GetInstrumentCandlesResponse200Granularity:
    if value in GET_INSTRUMENT_CANDLES_RESPONSE_200_GRANULARITY_VALUES:
        return cast(GetInstrumentCandlesResponse200Granularity, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_INSTRUMENT_CANDLES_RESPONSE_200_GRANULARITY_VALUES!r}"
    )
