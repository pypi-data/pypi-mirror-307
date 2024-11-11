from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        commission = d.pop("commission", None)
        units_traded = d.pop("unitsTraded", None)
        minimum_commission = d.pop("minimumCommission", None)
        instrument_commission = cls(
            commission=commission,
            units_traded=units_traded,
            minimum_commission=minimum_commission,
        )
        instrument_commission.additional_properties = d
        return instrument_commission

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
