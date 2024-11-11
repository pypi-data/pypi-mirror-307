from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .instrument_commission import InstrumentCommission
from .instrument_type import InstrumentType
from typing import TypeVar, Union

T = TypeVar("T", bound="Instrument")


@dataclasses.dataclass
class Instrument:
    """Full specification of an Instrument.

    Attributes:
        name (Union[Unset, str]): The name of the Instrument
        type (Union[Unset, InstrumentType]): The type of the Instrument
        display_name (Union[Unset, str]): The display name of the Instrument
        pip_location (Union[Unset, int]): The location of the "pip" for this instrument. The decimal position of the pip
            in this Instrument's price can be found at 10 ^ pipLocation (e.g. -4 pipLocation results in a decimal pip
            position of 10 ^ -4 = 0.0001).
        display_precision (Union[Unset, int]): The number of decimal places that should be used to display prices for
            this instrument. (e.g. a displayPrecision of 5 would result in a price of "1" being displayed as "1.00000")
        trade_units_precision (Union[Unset, int]): The amount of decimal places that may be provided when specifying the
            number of units traded for this instrument.
        minimum_trade_size (Union[Unset, str]): The smallest number of units allowed to be traded for this instrument.
        maximum_trailing_stop_distance (Union[Unset, str]): The maximum trailing stop distance allowed for a trailing
            stop loss created for this instrument. Specified in price units.
        minimum_trailing_stop_distance (Union[Unset, str]): The minimum trailing stop distance allowed for a trailing
            stop loss created for this instrument. Specified in price units.
        maximum_position_size (Union[Unset, str]): The maximum position size allowed for this instrument. Specified in
            units.
        maximum_order_units (Union[Unset, str]): The maximum units allowed for an Order placed for this instrument.
            Specified in units.
        margin_rate (Union[Unset, str]): The margin rate for this instrument.
        commission (Union[Unset, InstrumentCommission]): An InstrumentCommission represents an instrument-specific
            commission"""

    name: Union[Unset, str] = UNSET
    type: Union[Unset, InstrumentType] = UNSET
    display_name: Union[Unset, str] = UNSET
    pip_location: Union[Unset, int] = UNSET
    display_precision: Union[Unset, int] = UNSET
    trade_units_precision: Union[Unset, int] = UNSET
    minimum_trade_size: Union[Unset, str] = UNSET
    maximum_trailing_stop_distance: Union[Unset, str] = UNSET
    minimum_trailing_stop_distance: Union[Unset, str] = UNSET
    maximum_position_size: Union[Unset, str] = UNSET
    maximum_order_units: Union[Unset, str] = UNSET
    margin_rate: Union[Unset, str] = UNSET
    commission: Union[Unset, "InstrumentCommission"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Instrument":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
