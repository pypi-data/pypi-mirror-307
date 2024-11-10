from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="TradeReduce")


@_attrs_define
class TradeReduce:
    """A TradeReduce object represents a Trade for an instrument that was reduced (either partially or fully) in an
    Account. It is found embedded in Transactions that affect the position of an instrument in the account, specifically
    the OrderFill Transaction.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade that was reduced or closed
            units (Union[Unset, str]): The number of units that the Trade was reduced by
            price (Union[Unset, str]): The average price that the units were closed at. This price may be clamped for
                guaranteed Stop Loss Orders.
            realized_pl (Union[Unset, str]): The PL realized when reducing the Trade
            financing (Union[Unset, str]): The financing paid/collected when reducing the Trade
            guaranteed_execution_fee (Union[Unset, str]): This is the fee that is charged for closing the Trade if it has a
                guaranteed Stop Loss Order attached to it.
            half_spread_cost (Union[Unset, str]): The half spread cost for the trade reduce/close. This can be a positive or
                negative value and is represented in the home currency of the Account.
    """

    trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    realized_pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id

        units = self.units

        price = self.price

        realized_pl = self.realized_pl

        financing = self.financing

        guaranteed_execution_fee = self.guaranteed_execution_fee

        half_spread_cost = self.half_spread_cost

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if units is not UNSET:
            field_dict["units"] = units
        if price is not UNSET:
            field_dict["price"] = price
        if realized_pl is not UNSET:
            field_dict["realizedPL"] = realized_pl
        if financing is not UNSET:
            field_dict["financing"] = financing
        if guaranteed_execution_fee is not UNSET:
            field_dict["guaranteedExecutionFee"] = guaranteed_execution_fee
        if half_spread_cost is not UNSET:
            field_dict["halfSpreadCost"] = half_spread_cost

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", UNSET)

        units = d.pop("units", UNSET)

        price = d.pop("price", UNSET)

        realized_pl = d.pop("realizedPL", UNSET)

        financing = d.pop("financing", UNSET)

        guaranteed_execution_fee = d.pop("guaranteedExecutionFee", UNSET)

        half_spread_cost = d.pop("halfSpreadCost", UNSET)

        trade_reduce = cls(
            trade_id=trade_id,
            units=units,
            price=price,
            realized_pl=realized_pl,
            financing=financing,
            guaranteed_execution_fee=guaranteed_execution_fee,
            half_spread_cost=half_spread_cost,
        )

        trade_reduce.additional_properties = d
        return trade_reduce

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
