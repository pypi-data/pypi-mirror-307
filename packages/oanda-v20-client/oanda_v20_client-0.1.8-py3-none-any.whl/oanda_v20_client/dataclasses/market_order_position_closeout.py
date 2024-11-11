from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="MarketOrderPositionCloseout")


@dataclasses.dataclass
class MarketOrderPositionCloseout:
    """A MarketOrderPositionCloseout specifies the extensions to a Market Order when it has been created to closeout a
    specific Position.

        Attributes:
            instrument (Union[Unset, str]): The instrument of the Position being closed out.
            units (Union[Unset, str]): Indication of how much of the Position to close. Either "ALL", or a DecimalNumber
                reflection a partial close of the Trade. The DecimalNumber must always be positive, and represent a number that
                doesn't exceed the absolute size of the Position."""

    instrument: Optional[str]
    units: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        market_order_position_closeout = cls(instrument=instrument, units=units)
        market_order_position_closeout.additional_properties = d
        return market_order_position_closeout

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
