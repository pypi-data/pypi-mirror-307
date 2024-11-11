from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="InstrumentCommission")


@dataclasses.dataclass
class InstrumentCommission:
    """An InstrumentCommission represents an instrument-specific commission

    Attributes:
        commission (Union[Unset, str]): The commission amount (in the Account's home currency) charged per unitsTraded
            of the instrument
        units_traded (Union[Unset, str]): The number of units traded that the commission amount is based on.
        minimum_commission (Union[Unset, str]): The minimum commission amount (in the Account's home currency) that is
            charged when an Order is filled for this instrument."""

    commission: Optional[str]
    units_traded: Optional[str]
    minimum_commission: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstrumentCommission":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
