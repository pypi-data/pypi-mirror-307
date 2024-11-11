from typing import Literal, Set, cast

TradePL = Literal["NEGATIVE", "POSITIVE", "ZERO"]

TRADE_PL_VALUES: Set[TradePL] = {
    "NEGATIVE",
    "POSITIVE",
    "ZERO",
}


def check_trade_pl(value: str) -> TradePL:
    if value in TRADE_PL_VALUES:
        return cast(TradePL, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TRADE_PL_VALUES!r}")
