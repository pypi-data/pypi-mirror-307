from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .candlestick import Candlestick
from .get_instrument_candles_response_200_granularity import (
    GetInstrumentCandlesResponse200Granularity,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="GetInstrumentCandlesResponse200")


@dataclasses.dataclass
class GetInstrumentCandlesResponse200:
    """Attributes:
    instrument (Union[Unset, str]): The instrument whose Prices are represented by the candlesticks.
    granularity (Union[Unset, GetInstrumentCandlesResponse200Granularity]): The granularity of the candlesticks
        provided.
    candles (Union[Unset, List['Candlestick']]): The list of candlesticks that satisfy the request."""

    instrument: Union[Unset, str] = UNSET
    granularity: Union[Unset, GetInstrumentCandlesResponse200Granularity] = UNSET
    candles: Union[Unset, List["Candlestick"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetInstrumentCandlesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
