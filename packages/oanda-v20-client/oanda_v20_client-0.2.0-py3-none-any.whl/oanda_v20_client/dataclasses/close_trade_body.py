from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CloseTradeBody")


@dataclasses.dataclass
class CloseTradeBody:
    """Attributes:
    units (Optional[str]): Indication of how much of the Trade to close. Either the string "ALL" (indicating
        that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade
        to Close using a TradeClose MarketOrder. The units specified must always be positive, and the magnitude of the
        value cannot exceed the magnitude of the Trade's open units."""

    units: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units", None)
        close_trade_body = cls(units=units)
        return close_trade_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
