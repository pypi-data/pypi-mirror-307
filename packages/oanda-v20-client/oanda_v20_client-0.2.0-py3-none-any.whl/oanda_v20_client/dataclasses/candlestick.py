from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .candlestick_data import CandlestickData
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="Candlestick")


@dataclasses.dataclass
class Candlestick:
    """The Candlestick representation

    Attributes:
        time (Optional[str]): The start time of the candlestick
        bid (Optional[CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        ask (Optional[CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        mid (Optional[CandlestickData]): The price data (open, high, low, close) for the Candlestick representation.
        volume (Optional[int]): The number of prices created during the time-range represented by the candlestick.
        complete (Optional[bool]): A flag indicating if the candlestick is complete. A complete candlestick is one
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
        if _bid is None:
            bid = None
        else:
            bid = CandlestickData.from_dict(_bid)
        _ask = d.pop("ask", None)
        ask: Optional[CandlestickData]
        if _ask is None:
            ask = None
        else:
            ask = CandlestickData.from_dict(_ask)
        _mid = d.pop("mid", None)
        mid: Optional[CandlestickData]
        if _mid is None:
            mid = None
        else:
            mid = CandlestickData.from_dict(_mid)
        volume = d.pop("volume", None)
        complete = d.pop("complete", None)
        candlestick = cls(
            time=time, bid=bid, ask=ask, mid=mid, volume=volume, complete=complete
        )
        return candlestick

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
