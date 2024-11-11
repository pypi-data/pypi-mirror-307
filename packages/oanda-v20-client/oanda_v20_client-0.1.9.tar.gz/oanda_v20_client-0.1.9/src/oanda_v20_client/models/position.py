from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.position_side import PositionSide


T = TypeVar("T", bound="Position")


@_attrs_define
class Position:
    """The specification of a Position within an Account.

    Attributes:
        instrument (Union[Unset, str]): The Position's Instrument.
        pl (Union[Unset, str]): Profit/loss realized by the Position over the lifetime of the Account.
        unrealized_pl (Union[Unset, str]): The unrealized profit/loss of all open Trades that contribute to this
            Position.
        margin_used (Union[Unset, str]): Margin currently used by the Position.
        resettable_pl (Union[Unset, str]): Profit/loss realized by the Position since the Account's resettablePL was
            last reset by the client.
        financing (Union[Unset, str]): The total amount of financing paid/collected for this instrument over the
            lifetime of the Account.
        commission (Union[Unset, str]): The total amount of commission paid for this instrument over the lifetime of the
            Account.
        guaranteed_execution_fees (Union[Unset, str]): The total amount of fees charged over the lifetime of the Account
            for the execution of guaranteed Stop Loss Orders for this instrument.
        long (Union[Unset, PositionSide]): The representation of a Position for a single direction (long or short).
        short (Union[Unset, PositionSide]): The representation of a Position for a single direction (long or short).
    """

    instrument: Union[Unset, str] = UNSET
    pl: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    resettable_pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    commission: Union[Unset, str] = UNSET
    guaranteed_execution_fees: Union[Unset, str] = UNSET
    long: Union[Unset, "PositionSide"] = UNSET
    short: Union[Unset, "PositionSide"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        pl = self.pl

        unrealized_pl = self.unrealized_pl

        margin_used = self.margin_used

        resettable_pl = self.resettable_pl

        financing = self.financing

        commission = self.commission

        guaranteed_execution_fees = self.guaranteed_execution_fees

        long: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long, Unset):
            long = self.long.to_dict()

        short: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short, Unset):
            short = self.short.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if pl is not UNSET:
            field_dict["pl"] = pl
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used
        if resettable_pl is not UNSET:
            field_dict["resettablePL"] = resettable_pl
        if financing is not UNSET:
            field_dict["financing"] = financing
        if commission is not UNSET:
            field_dict["commission"] = commission
        if guaranteed_execution_fees is not UNSET:
            field_dict["guaranteedExecutionFees"] = guaranteed_execution_fees
        if long is not UNSET:
            field_dict["long"] = long
        if short is not UNSET:
            field_dict["short"] = short

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position_side import PositionSide

        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        pl = d.pop("pl", UNSET)

        unrealized_pl = d.pop("unrealizedPL", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        resettable_pl = d.pop("resettablePL", UNSET)

        financing = d.pop("financing", UNSET)

        commission = d.pop("commission", UNSET)

        guaranteed_execution_fees = d.pop("guaranteedExecutionFees", UNSET)

        _long = d.pop("long", UNSET)
        long: Union[Unset, PositionSide]
        if isinstance(_long, Unset):
            long = UNSET
        else:
            long = PositionSide.from_dict(_long)

        _short = d.pop("short", UNSET)
        short: Union[Unset, PositionSide]
        if isinstance(_short, Unset):
            short = UNSET
        else:
            short = PositionSide.from_dict(_short)

        position = cls(
            instrument=instrument,
            pl=pl,
            unrealized_pl=unrealized_pl,
            margin_used=margin_used,
            resettable_pl=resettable_pl,
            financing=financing,
            commission=commission,
            guaranteed_execution_fees=guaranteed_execution_fees,
            long=long,
            short=short,
        )

        position.additional_properties = d
        return position

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
