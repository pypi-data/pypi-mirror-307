from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.instrument_type import check_instrument_type
from ..models.instrument_type import InstrumentType
from typing import Union

if TYPE_CHECKING:
    from ..models.instrument_commission import InstrumentCommission


T = TypeVar("T", bound="Instrument")


@_attrs_define
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
            commission
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        display_name = self.display_name

        pip_location = self.pip_location

        display_precision = self.display_precision

        trade_units_precision = self.trade_units_precision

        minimum_trade_size = self.minimum_trade_size

        maximum_trailing_stop_distance = self.maximum_trailing_stop_distance

        minimum_trailing_stop_distance = self.minimum_trailing_stop_distance

        maximum_position_size = self.maximum_position_size

        maximum_order_units = self.maximum_order_units

        margin_rate = self.margin_rate

        commission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.commission, Unset):
            commission = self.commission.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if pip_location is not UNSET:
            field_dict["pipLocation"] = pip_location
        if display_precision is not UNSET:
            field_dict["displayPrecision"] = display_precision
        if trade_units_precision is not UNSET:
            field_dict["tradeUnitsPrecision"] = trade_units_precision
        if minimum_trade_size is not UNSET:
            field_dict["minimumTradeSize"] = minimum_trade_size
        if maximum_trailing_stop_distance is not UNSET:
            field_dict["maximumTrailingStopDistance"] = maximum_trailing_stop_distance
        if minimum_trailing_stop_distance is not UNSET:
            field_dict["minimumTrailingStopDistance"] = minimum_trailing_stop_distance
        if maximum_position_size is not UNSET:
            field_dict["maximumPositionSize"] = maximum_position_size
        if maximum_order_units is not UNSET:
            field_dict["maximumOrderUnits"] = maximum_order_units
        if margin_rate is not UNSET:
            field_dict["marginRate"] = margin_rate
        if commission is not UNSET:
            field_dict["commission"] = commission

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instrument_commission import InstrumentCommission

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, InstrumentType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_instrument_type(_type)

        display_name = d.pop("displayName", UNSET)

        pip_location = d.pop("pipLocation", UNSET)

        display_precision = d.pop("displayPrecision", UNSET)

        trade_units_precision = d.pop("tradeUnitsPrecision", UNSET)

        minimum_trade_size = d.pop("minimumTradeSize", UNSET)

        maximum_trailing_stop_distance = d.pop("maximumTrailingStopDistance", UNSET)

        minimum_trailing_stop_distance = d.pop("minimumTrailingStopDistance", UNSET)

        maximum_position_size = d.pop("maximumPositionSize", UNSET)

        maximum_order_units = d.pop("maximumOrderUnits", UNSET)

        margin_rate = d.pop("marginRate", UNSET)

        _commission = d.pop("commission", UNSET)
        commission: Union[Unset, InstrumentCommission]
        if isinstance(_commission, Unset):
            commission = UNSET
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

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
