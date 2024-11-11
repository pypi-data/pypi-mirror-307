from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .units_available_details import UnitsAvailableDetails
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    default: Union[Unset, "UnitsAvailableDetails"] = UNSET
    reduce_first: Union[Unset, "UnitsAvailableDetails"] = UNSET
    reduce_only: Union[Unset, "UnitsAvailableDetails"] = UNSET
    open_only: Union[Unset, "UnitsAvailableDetails"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnitsAvailable":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
