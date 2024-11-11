from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .candlestick import Candlestick
from .get_instrument_candles_response_200_granularity import (
    GetInstrumentCandlesResponse200Granularity,
)
from .get_instrument_candles_response_200_granularity import (
    check_get_instrument_candles_response_200_granularity,
)
from types import Unset
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="GetInstrumentCandlesResponse200")


@dataclasses.dataclass
class GetInstrumentCandlesResponse200:
    """Attributes:
    instrument (Union[Unset, str]): The instrument whose Prices are represented by the candlesticks.
    granularity (Union[Unset, GetInstrumentCandlesResponse200Granularity]): The granularity of the candlesticks
        provided.
    candles (Union[Unset, List['Candlestick']]): The list of candlesticks that satisfy the request."""

    instrument: Optional[str]
    granularity: Optional[GetInstrumentCandlesResponse200Granularity]
    candles: Optional[List["Candlestick"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .candlestick import Candlestick

        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        _granularity = d.pop("granularity", None)
        granularity: Optional[GetInstrumentCandlesResponse200Granularity]
        if isinstance(_granularity, Unset):
            granularity = None
        else:
            granularity = check_get_instrument_candles_response_200_granularity(
                _granularity
            )
        candles = []
        _candles = d.pop("candles", None)
        for candles_item_data in _candles or []:
            candles_item = Candlestick.from_dict(candles_item_data)
            candles.append(candles_item)
        get_instrument_candles_response_200 = cls(
            instrument=instrument, granularity=granularity, candles=candles
        )
        get_instrument_candles_response_200.additional_properties = d
        return get_instrument_candles_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
