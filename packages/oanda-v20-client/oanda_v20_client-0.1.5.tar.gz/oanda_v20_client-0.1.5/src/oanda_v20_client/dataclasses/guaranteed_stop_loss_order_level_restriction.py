from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="GuaranteedStopLossOrderLevelRestriction")


@dataclasses.dataclass
class GuaranteedStopLossOrderLevelRestriction:
    """A GuaranteedStopLossOrderLevelRestriction represents the total position size that can exist within a given price
    window for Trades with guaranteed Stop Loss Orders attached for a specific Instrument.

        Attributes:
            volume (Union[Unset, str]): Applies to Trades with a guaranteed Stop Loss Order attached for the specified
                Instrument. This is the total allowed Trade volume that can exist within the priceRange based on the trigger
                prices of the guaranteed Stop Loss Orders.
            price_range (Union[Unset, str]): The price range the volume applies to. This value is in price units."""

    volume: Union[Unset, str] = UNSET
    price_range: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "GuaranteedStopLossOrderLevelRestriction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
