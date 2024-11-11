from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    commission: Union[Unset, str] = UNSET
    units_traded: Union[Unset, str] = UNSET
    minimum_commission: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstrumentCommission":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
