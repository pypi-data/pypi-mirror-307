from __future__ import annotations
from typing import Literal, Set, cast

CandlestickGranularity = Literal[
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
CANDLESTICK_GRANULARITY_VALUES: Set[CandlestickGranularity] = {
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


def check_candlestick_granularity(value: str) -> CandlestickGranularity:
    if value in CANDLESTICK_GRANULARITY_VALUES:
        return cast(CandlestickGranularity, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CANDLESTICK_GRANULARITY_VALUES!r}"
    )
