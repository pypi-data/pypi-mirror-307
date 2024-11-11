from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CandlestickData")


@dataclasses.dataclass
class CandlestickData:
    """The price data (open, high, low, close) for the Candlestick representation.

    Attributes:
        o (Union[Unset, str]): The first (open) price in the time-range represented by the candlestick.
        h (Union[Unset, str]): The highest price in the time-range represented by the candlestick.
        l (Union[Unset, str]): The lowest price in the time-range represented by the candlestick.
        c (Union[Unset, str]): The last (closing) price in the time-range represented by the candlestick."""

    o: Optional[str]
    h: Optional[str]
    l: Optional[str]
    c: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        o = d.pop("o", None)
        h = d.pop("h", None)
        l = d.pop("l", None)
        c = d.pop("c", None)
        candlestick_data = cls(o=o, h=h, l=l, c=c)
        candlestick_data.additional_properties = d
        return candlestick_data

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
