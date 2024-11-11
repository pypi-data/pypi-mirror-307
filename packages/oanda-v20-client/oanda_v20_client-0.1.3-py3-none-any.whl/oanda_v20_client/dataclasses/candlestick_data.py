from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="CandlestickData")


@dataclasses.dataclass
class CandlestickData:
    """The price data (open, high, low, close) for the Candlestick representation.

    Attributes:
        o (Union[Unset, str]): The first (open) price in the time-range represented by the candlestick.
        h (Union[Unset, str]): The highest price in the time-range represented by the candlestick.
        l (Union[Unset, str]): The lowest price in the time-range represented by the candlestick.
        c (Union[Unset, str]): The last (closing) price in the time-range represented by the candlestick."""

    o: Union[Unset, str] = UNSET
    h: Union[Unset, str] = UNSET
    l: Union[Unset, str] = UNSET
    c: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CandlestickData":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
