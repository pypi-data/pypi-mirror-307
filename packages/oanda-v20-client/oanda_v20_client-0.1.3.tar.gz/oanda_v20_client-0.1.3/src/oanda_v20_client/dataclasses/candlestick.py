from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .candlestick_data import CandlestickData
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="Candlestick")


@dataclasses.dataclass
class Candlestick:
    """The Candlestick representation

    Attributes:
        time (Union[Unset, str]): The start time of the candlestick
        bid (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        ask (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        mid (Union[Unset, CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        volume (Union[Unset, int]): The number of prices created during the time-range represented by the candlestick.
        complete (Union[Unset, bool]): A flag indicating if the candlestick is complete. A complete candlestick is one
            whose ending time is not in the future."""

    time: Union[Unset, str] = UNSET
    bid: Union[Unset, "CandlestickData"] = UNSET
    ask: Union[Unset, "CandlestickData"] = UNSET
    mid: Union[Unset, "CandlestickData"] = UNSET
    volume: Union[Unset, int] = UNSET
    complete: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candlestick":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
