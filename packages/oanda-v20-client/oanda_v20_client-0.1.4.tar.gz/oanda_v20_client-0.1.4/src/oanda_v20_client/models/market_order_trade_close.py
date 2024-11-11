from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="MarketOrderTradeClose")


@_attrs_define
class MarketOrderTradeClose:
    """A MarketOrderTradeClose specifies the extensions to a Market Order that has been created specifically to close a
    Trade.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade requested to be closed
            client_trade_id (Union[Unset, str]): The client ID of the Trade requested to be closed
            units (Union[Unset, str]): Indication of how much of the Trade to close. Either "ALL", or a DecimalNumber
                reflection a partial close of the Trade.
    """

    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id

        client_trade_id = self.client_trade_id

        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if client_trade_id is not UNSET:
            field_dict["clientTradeID"] = client_trade_id
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", UNSET)

        client_trade_id = d.pop("clientTradeID", UNSET)

        units = d.pop("units", UNSET)

        market_order_trade_close = cls(
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            units=units,
        )

        market_order_trade_close.additional_properties = d
        return market_order_trade_close

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
