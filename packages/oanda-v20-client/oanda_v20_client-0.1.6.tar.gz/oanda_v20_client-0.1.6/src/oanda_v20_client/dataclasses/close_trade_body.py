from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="CloseTradeBody")


@dataclasses.dataclass
class CloseTradeBody:
    """Attributes:
    units (Union[Unset, str]): Indication of how much of the Trade to close. Either the string "ALL" (indicating
        that all of the Trade should be closed), or a DecimalNumber representing the number of units of the open Trade
        to Close using a TradeClose MarketOrder. The units specified must always be positive, and the magnitude of the
        value cannot exceed the magnitude of the Trade's open units."""

    units: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CloseTradeBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
