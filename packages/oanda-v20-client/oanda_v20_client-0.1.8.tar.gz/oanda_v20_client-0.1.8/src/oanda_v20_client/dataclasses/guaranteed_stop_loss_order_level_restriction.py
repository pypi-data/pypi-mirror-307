from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    volume: Optional[str]
    price_range: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        volume = d.pop("volume", None)
        price_range = d.pop("priceRange", None)
        guaranteed_stop_loss_order_level_restriction = cls(
            volume=volume, price_range=price_range
        )
        guaranteed_stop_loss_order_level_restriction.additional_properties = d
        return guaranteed_stop_loss_order_level_restriction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
