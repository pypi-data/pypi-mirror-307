from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .candlestick_data import CandlestickData
from types import Unset
from typing import Optional, Type, TypeVar

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

    time: Optional[str]
    bid: Optional["CandlestickData"]
    ask: Optional["CandlestickData"]
    mid: Optional["CandlestickData"]
    volume: Optional[int]
    complete: Optional[bool]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .candlestick_data import CandlestickData

        d = src_dict.copy()
        time = d.pop("time", None)
        _bid = d.pop("bid", None)
        bid: Optional[CandlestickData]
        if isinstance(_bid, Unset):
            bid = None
        else:
            bid = CandlestickData.from_dict(_bid)
        _ask = d.pop("ask", None)
        ask: Optional[CandlestickData]
        if isinstance(_ask, Unset):
            ask = None
        else:
            ask = CandlestickData.from_dict(_ask)
        _mid = d.pop("mid", None)
        mid: Optional[CandlestickData]
        if isinstance(_mid, Unset):
            mid = None
        else:
            mid = CandlestickData.from_dict(_mid)
        volume = d.pop("volume", None)
        complete = d.pop("complete", None)
        candlestick = cls(
            time=time, bid=bid, ask=ask, mid=mid, volume=volume, complete=complete
        )
        candlestick.additional_properties = d
        return candlestick

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
