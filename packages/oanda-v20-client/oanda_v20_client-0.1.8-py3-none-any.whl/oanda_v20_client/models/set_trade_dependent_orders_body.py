from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.stop_loss_details import StopLossDetails
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.take_profit_details import TakeProfitDetails


T = TypeVar("T", bound="SetTradeDependentOrdersBody")


@_attrs_define
class SetTradeDependentOrdersBody:
    """
    Attributes:
        take_profit (Union[Unset, TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit Order to
            be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Take
            Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
        stop_loss (Union[Unset, StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to be
            created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop Loss,
            or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
        trailing_stop_loss (Union[Unset, TrailingStopLossDetails]): TrailingStopLossDetails specifies the details of a
            Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is filled that opens
            a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order is modified
            directly through the Trade.
    """

    take_profit: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss: Union[Unset, "TrailingStopLossDetails"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        take_profit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit, Unset):
            take_profit = self.take_profit.to_dict()

        stop_loss: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss, Unset):
            stop_loss = self.stop_loss.to_dict()

        trailing_stop_loss: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss, Unset):
            trailing_stop_loss = self.trailing_stop_loss.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if take_profit is not UNSET:
            field_dict["takeProfit"] = take_profit
        if stop_loss is not UNSET:
            field_dict["stopLoss"] = stop_loss
        if trailing_stop_loss is not UNSET:
            field_dict["trailingStopLoss"] = trailing_stop_loss

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stop_loss_details import StopLossDetails
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.take_profit_details import TakeProfitDetails

        d = src_dict.copy()
        _take_profit = d.pop("takeProfit", UNSET)
        take_profit: Union[Unset, TakeProfitDetails]
        if isinstance(_take_profit, Unset):
            take_profit = UNSET
        else:
            take_profit = TakeProfitDetails.from_dict(_take_profit)

        _stop_loss = d.pop("stopLoss", UNSET)
        stop_loss: Union[Unset, StopLossDetails]
        if isinstance(_stop_loss, Unset):
            stop_loss = UNSET
        else:
            stop_loss = StopLossDetails.from_dict(_stop_loss)

        _trailing_stop_loss = d.pop("trailingStopLoss", UNSET)
        trailing_stop_loss: Union[Unset, TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss, Unset):
            trailing_stop_loss = UNSET
        else:
            trailing_stop_loss = TrailingStopLossDetails.from_dict(_trailing_stop_loss)

        set_trade_dependent_orders_body = cls(
            take_profit=take_profit,
            stop_loss=stop_loss,
            trailing_stop_loss=trailing_stop_loss,
        )

        set_trade_dependent_orders_body.additional_properties = d
        return set_trade_dependent_orders_body

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
