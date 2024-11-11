from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.market_order_reject_transaction import MarketOrderRejectTransaction


T = TypeVar("T", bound="CloseTradeResponse400")


@_attrs_define
class CloseTradeResponse400:
    """
    Attributes:
        order_reject_transaction (Union[Unset, MarketOrderRejectTransaction]): A MarketOrderRejectTransaction represents
            the rejection of the creation of a Market Order.
        error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
            errors.
        error_message (Union[Unset, str]): The human-readable description of the error that has occurred.
    """

    order_reject_transaction: Union[Unset, "MarketOrderRejectTransaction"] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_reject_transaction, Unset):
            order_reject_transaction = self.order_reject_transaction.to_dict()

        error_code = self.error_code

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_reject_transaction is not UNSET:
            field_dict["orderRejectTransaction"] = order_reject_transaction
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.market_order_reject_transaction import (
            MarketOrderRejectTransaction,
        )

        d = src_dict.copy()
        _order_reject_transaction = d.pop("orderRejectTransaction", UNSET)
        order_reject_transaction: Union[Unset, MarketOrderRejectTransaction]
        if isinstance(_order_reject_transaction, Unset):
            order_reject_transaction = UNSET
        else:
            order_reject_transaction = MarketOrderRejectTransaction.from_dict(
                _order_reject_transaction
            )

        error_code = d.pop("errorCode", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        close_trade_response_400 = cls(
            order_reject_transaction=order_reject_transaction,
            error_code=error_code,
            error_message=error_message,
        )

        close_trade_response_400.additional_properties = d
        return close_trade_response_400

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
