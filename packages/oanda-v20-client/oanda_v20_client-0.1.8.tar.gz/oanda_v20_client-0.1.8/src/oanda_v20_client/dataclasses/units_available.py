from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .units_available_details import UnitsAvailableDetails
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="UnitsAvailable")


@dataclasses.dataclass
class UnitsAvailable:
    """Representation of how many units of an Instrument are available to be traded by an Order depending on its
    postionFill option.

        Attributes:
            default (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available to be
                traded for both long and short Orders.
            reduce_first (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available
                to be traded for both long and short Orders.
            reduce_only (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available
                to be traded for both long and short Orders.
            open_only (Union[Unset, UnitsAvailableDetails]): Representation of many units of an Instrument are available to
                be traded for both long and short Orders."""

    default: Optional["UnitsAvailableDetails"]
    reduce_first: Optional["UnitsAvailableDetails"]
    reduce_only: Optional["UnitsAvailableDetails"]
    open_only: Optional["UnitsAvailableDetails"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .units_available_details import UnitsAvailableDetails

        d = src_dict.copy()
        _default = d.pop("default", None)
        default: Optional[UnitsAvailableDetails]
        if isinstance(_default, Unset):
            default = None
        else:
            default = UnitsAvailableDetails.from_dict(_default)
        _reduce_first = d.pop("reduceFirst", None)
        reduce_first: Optional[UnitsAvailableDetails]
        if isinstance(_reduce_first, Unset):
            reduce_first = None
        else:
            reduce_first = UnitsAvailableDetails.from_dict(_reduce_first)
        _reduce_only = d.pop("reduceOnly", None)
        reduce_only: Optional[UnitsAvailableDetails]
        if isinstance(_reduce_only, Unset):
            reduce_only = None
        else:
            reduce_only = UnitsAvailableDetails.from_dict(_reduce_only)
        _open_only = d.pop("openOnly", None)
        open_only: Optional[UnitsAvailableDetails]
        if isinstance(_open_only, Unset):
            open_only = None
        else:
            open_only = UnitsAvailableDetails.from_dict(_open_only)
        units_available = cls(
            default=default,
            reduce_first=reduce_first,
            reduce_only=reduce_only,
            open_only=open_only,
        )
        units_available.additional_properties = d
        return units_available

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
