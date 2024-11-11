from __future__ import annotations
from typing import Literal, Set, cast

PositionAggregationMode = Literal["ABSOLUTE_SUM", "MAXIMAL_SIDE", "NET_SUM"]
POSITION_AGGREGATION_MODE_VALUES: Set[PositionAggregationMode] = {
    "ABSOLUTE_SUM",
    "MAXIMAL_SIDE",
    "NET_SUM",
}


def check_position_aggregation_mode(value: str) -> PositionAggregationMode:
    if value in POSITION_AGGREGATION_MODE_VALUES:
        return cast(PositionAggregationMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {POSITION_AGGREGATION_MODE_VALUES!r}"
    )
