from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="MarketOrderDelayedTradeClose")


@_attrs_define
class MarketOrderDelayedTradeClose:
    """Details for the Market Order extensions specific to a Market Order placed with the intent of fully closing a
    specific open trade that should have already been closed but wasn't due to halted market conditions

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade being closed
            client_trade_id (Union[Unset, str]): The Client ID of the Trade being closed
            source_transaction_id (Union[Unset, str]): The Transaction ID of the DelayedTradeClosure transaction to which
                this Delayed Trade Close belongs to
    """

    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    source_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id

        client_trade_id = self.client_trade_id

        source_transaction_id = self.source_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if client_trade_id is not UNSET:
            field_dict["clientTradeID"] = client_trade_id
        if source_transaction_id is not UNSET:
            field_dict["sourceTransactionID"] = source_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", UNSET)

        client_trade_id = d.pop("clientTradeID", UNSET)

        source_transaction_id = d.pop("sourceTransactionID", UNSET)

        market_order_delayed_trade_close = cls(
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            source_transaction_id=source_transaction_id,
        )

        market_order_delayed_trade_close.additional_properties = d
        return market_order_delayed_trade_close

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
