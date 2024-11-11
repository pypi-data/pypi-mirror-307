from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="PositionSide")


@_attrs_define
class PositionSide:
    """The representation of a Position for a single direction (long or short).

    Attributes:
        units (Union[Unset, str]): Number of units in the position (negative value indicates short position, positive
            indicates long position).
        average_price (Union[Unset, str]): Volume-weighted average of the underlying Trade open prices for the Position.
        trade_i_ds (Union[Unset, List[str]]): List of the open Trade IDs which contribute to the open Position.
        pl (Union[Unset, str]): Profit/loss realized by the PositionSide over the lifetime of the Account.
        unrealized_pl (Union[Unset, str]): The unrealized profit/loss of all open Trades that contribute to this
            PositionSide.
        resettable_pl (Union[Unset, str]): Profit/loss realized by the PositionSide since the Account's resettablePL was
            last reset by the client.
        financing (Union[Unset, str]): The total amount of financing paid/collected for this PositionSide over the
            lifetime of the Account.
        guaranteed_execution_fees (Union[Unset, str]): The total amount of fees charged over the lifetime of the Account
            for the execution of guaranteed Stop Loss Orders attached to Trades for this PositionSide.
    """

    units: Union[Unset, str] = UNSET
    average_price: Union[Unset, str] = UNSET
    trade_i_ds: Union[Unset, List[str]] = UNSET
    pl: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    resettable_pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    guaranteed_execution_fees: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        units = self.units

        average_price = self.average_price

        trade_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.trade_i_ds, Unset):
            trade_i_ds = self.trade_i_ds

        pl = self.pl

        unrealized_pl = self.unrealized_pl

        resettable_pl = self.resettable_pl

        financing = self.financing

        guaranteed_execution_fees = self.guaranteed_execution_fees

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units
        if average_price is not UNSET:
            field_dict["averagePrice"] = average_price
        if trade_i_ds is not UNSET:
            field_dict["tradeIDs"] = trade_i_ds
        if pl is not UNSET:
            field_dict["pl"] = pl
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if resettable_pl is not UNSET:
            field_dict["resettablePL"] = resettable_pl
        if financing is not UNSET:
            field_dict["financing"] = financing
        if guaranteed_execution_fees is not UNSET:
            field_dict["guaranteedExecutionFees"] = guaranteed_execution_fees

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units", UNSET)

        average_price = d.pop("averagePrice", UNSET)

        trade_i_ds = cast(List[str], d.pop("tradeIDs", UNSET))

        pl = d.pop("pl", UNSET)

        unrealized_pl = d.pop("unrealizedPL", UNSET)

        resettable_pl = d.pop("resettablePL", UNSET)

        financing = d.pop("financing", UNSET)

        guaranteed_execution_fees = d.pop("guaranteedExecutionFees", UNSET)

        position_side = cls(
            units=units,
            average_price=average_price,
            trade_i_ds=trade_i_ds,
            pl=pl,
            unrealized_pl=unrealized_pl,
            resettable_pl=resettable_pl,
            financing=financing,
            guaranteed_execution_fees=guaranteed_execution_fees,
        )

        position_side.additional_properties = d
        return position_side

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
