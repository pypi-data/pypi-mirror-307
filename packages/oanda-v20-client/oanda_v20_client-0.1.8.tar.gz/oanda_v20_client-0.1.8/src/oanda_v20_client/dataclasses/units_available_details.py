from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="UnitsAvailableDetails")


@dataclasses.dataclass
class UnitsAvailableDetails:
    """Representation of many units of an Instrument are available to be traded for both long and short Orders.

    Attributes:
        long (Union[Unset, str]): The units available for long Orders.
        short (Union[Unset, str]): The units available for short Orders."""

    long: Optional[str]
    short: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        long = d.pop("long", None)
        short = d.pop("short", None)
        units_available_details = cls(long=long, short=short)
        units_available_details.additional_properties = d
        return units_available_details

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
