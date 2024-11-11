from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .instrument_commission import InstrumentCommission
from .instrument_type import InstrumentType
from .instrument_type import check_instrument_type
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="Instrument")


@dataclasses.dataclass
class Instrument:
    """Full specification of an Instrument.

    Attributes:
        name (Optional[str]): The name of the Instrument
        type (Optional[InstrumentType]): The type of the Instrument
        display_name (Optional[str]): The display name of the Instrument
        pip_location (Optional[int]): The location of the "pip" for this instrument. The decimal position of the pip
            in this Instrument's price can be found at 10 ^ pipLocation (e.g. -4 pipLocation results in a decimal pip
            position of 10 ^ -4 = 0.0001).
        display_precision (Optional[int]): The number of decimal places that should be used to display prices for
            this instrument. (e.g. a displayPrecision of 5 would result in a price of "1" being displayed as "1.00000")
        trade_units_precision (Optional[int]): The amount of decimal places that may be provided when specifying the
            number of units traded for this instrument.
        minimum_trade_size (Optional[str]): The smallest number of units allowed to be traded for this instrument.
        maximum_trailing_stop_distance (Optional[str]): The maximum trailing stop distance allowed for a trailing
            stop loss created for this instrument. Specified in price units.
        minimum_trailing_stop_distance (Optional[str]): The minimum trailing stop distance allowed for a trailing
            stop loss created for this instrument. Specified in price units.
        maximum_position_size (Optional[str]): The maximum position size allowed for this instrument. Specified in
            units.
        maximum_order_units (Optional[str]): The maximum units allowed for an Order placed for this instrument.
            Specified in units.
        margin_rate (Optional[str]): The margin rate for this instrument.
        commission (Optional[InstrumentCommission]): An InstrumentCommission represents an instrument-specific
            commission"""

    name: Optional[str]
    type: Optional[InstrumentType]
    display_name: Optional[str]
    pip_location: Optional[int]
    display_precision: Optional[int]
    trade_units_precision: Optional[int]
    minimum_trade_size: Optional[str]
    maximum_trailing_stop_distance: Optional[str]
    minimum_trailing_stop_distance: Optional[str]
    maximum_position_size: Optional[str]
    maximum_order_units: Optional[str]
    margin_rate: Optional[str]
    commission: Optional["InstrumentCommission"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .instrument_commission import InstrumentCommission

        d = src_dict.copy()
        name = d.pop("name", None)
        _type = d.pop("type", None)
        type: Optional[InstrumentType]
        if _type is None:
            type = None
        else:
            type = check_instrument_type(_type)
        display_name = d.pop("displayName", None)
        pip_location = d.pop("pipLocation", None)
        display_precision = d.pop("displayPrecision", None)
        trade_units_precision = d.pop("tradeUnitsPrecision", None)
        minimum_trade_size = d.pop("minimumTradeSize", None)
        maximum_trailing_stop_distance = d.pop("maximumTrailingStopDistance", None)
        minimum_trailing_stop_distance = d.pop("minimumTrailingStopDistance", None)
        maximum_position_size = d.pop("maximumPositionSize", None)
        maximum_order_units = d.pop("maximumOrderUnits", None)
        margin_rate = d.pop("marginRate", None)
        _commission = d.pop("commission", None)
        commission: Optional[InstrumentCommission]
        if _commission is None:
            commission = None
        else:
            commission = InstrumentCommission.from_dict(_commission)
        instrument = cls(
            name=name,
            type=type,
            display_name=display_name,
            pip_location=pip_location,
            display_precision=display_precision,
            trade_units_precision=trade_units_precision,
            minimum_trade_size=minimum_trade_size,
            maximum_trailing_stop_distance=maximum_trailing_stop_distance,
            minimum_trailing_stop_distance=minimum_trailing_stop_distance,
            maximum_position_size=maximum_position_size,
            maximum_order_units=maximum_order_units,
            margin_rate=margin_rate,
            commission=commission,
        )
        instrument.additional_properties = d
        return instrument

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
