from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.take_profit_order_transaction import TakeProfitOrderTransaction
    from ..models.stop_loss_order_transaction import StopLossOrderTransaction
    from ..models.order_fill_transaction import OrderFillTransaction
    from ..models.order_cancel_transaction import OrderCancelTransaction
    from ..models.trailing_stop_loss_order_transaction import (
        TrailingStopLossOrderTransaction,
    )


T = TypeVar("T", bound="SetTradeDependentOrdersResponse200")


@_attrs_define
class SetTradeDependentOrdersResponse200:
    """
    Attributes:
        take_profit_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
            represents the cancellation of an Order in the client's Account.
        take_profit_order_transaction (Union[Unset, TakeProfitOrderTransaction]): A TakeProfitOrderTransaction
            represents the creation of a TakeProfit Order in the user's Account.
        take_profit_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
            filling of an Order in the client's Account.
        take_profit_order_created_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
            represents the cancellation of an Order in the client's Account.
        stop_loss_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents
            the cancellation of an Order in the client's Account.
        stop_loss_order_transaction (Union[Unset, StopLossOrderTransaction]): A StopLossOrderTransaction represents the
            creation of a StopLoss Order in the user's Account.
        stop_loss_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
            filling of an Order in the client's Account.
        stop_loss_order_created_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
            represents the cancellation of an Order in the client's Account.
        trailing_stop_loss_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction
            represents the cancellation of an Order in the client's Account.
        trailing_stop_loss_order_transaction (Union[Unset, TrailingStopLossOrderTransaction]): A
            TrailingStopLossOrderTransaction represents the creation of a TrailingStopLoss Order in the user's Account.
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    take_profit_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    take_profit_order_transaction: Union[Unset, "TakeProfitOrderTransaction"] = UNSET
    take_profit_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    take_profit_order_created_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    stop_loss_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    stop_loss_order_transaction: Union[Unset, "StopLossOrderTransaction"] = UNSET
    stop_loss_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    stop_loss_order_created_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    trailing_stop_loss_order_cancel_transaction: Union[
        Unset, "OrderCancelTransaction"
    ] = UNSET
    trailing_stop_loss_order_transaction: Union[
        Unset, "TrailingStopLossOrderTransaction"
    ] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        take_profit_order_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_order_cancel_transaction, Unset):
            take_profit_order_cancel_transaction = (
                self.take_profit_order_cancel_transaction.to_dict()
            )

        take_profit_order_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_order_transaction, Unset):
            take_profit_order_transaction = self.take_profit_order_transaction.to_dict()

        take_profit_order_fill_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_order_fill_transaction, Unset):
            take_profit_order_fill_transaction = (
                self.take_profit_order_fill_transaction.to_dict()
            )

        take_profit_order_created_cancel_transaction: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.take_profit_order_created_cancel_transaction, Unset):
            take_profit_order_created_cancel_transaction = (
                self.take_profit_order_created_cancel_transaction.to_dict()
            )

        stop_loss_order_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_cancel_transaction, Unset):
            stop_loss_order_cancel_transaction = (
                self.stop_loss_order_cancel_transaction.to_dict()
            )

        stop_loss_order_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_transaction, Unset):
            stop_loss_order_transaction = self.stop_loss_order_transaction.to_dict()

        stop_loss_order_fill_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_fill_transaction, Unset):
            stop_loss_order_fill_transaction = (
                self.stop_loss_order_fill_transaction.to_dict()
            )

        stop_loss_order_created_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_created_cancel_transaction, Unset):
            stop_loss_order_created_cancel_transaction = (
                self.stop_loss_order_created_cancel_transaction.to_dict()
            )

        trailing_stop_loss_order_cancel_transaction: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.trailing_stop_loss_order_cancel_transaction, Unset):
            trailing_stop_loss_order_cancel_transaction = (
                self.trailing_stop_loss_order_cancel_transaction.to_dict()
            )

        trailing_stop_loss_order_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss_order_transaction, Unset):
            trailing_stop_loss_order_transaction = (
                self.trailing_stop_loss_order_transaction.to_dict()
            )

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if take_profit_order_cancel_transaction is not UNSET:
            field_dict["takeProfitOrderCancelTransaction"] = (
                take_profit_order_cancel_transaction
            )
        if take_profit_order_transaction is not UNSET:
            field_dict["takeProfitOrderTransaction"] = take_profit_order_transaction
        if take_profit_order_fill_transaction is not UNSET:
            field_dict["takeProfitOrderFillTransaction"] = (
                take_profit_order_fill_transaction
            )
        if take_profit_order_created_cancel_transaction is not UNSET:
            field_dict["takeProfitOrderCreatedCancelTransaction"] = (
                take_profit_order_created_cancel_transaction
            )
        if stop_loss_order_cancel_transaction is not UNSET:
            field_dict["stopLossOrderCancelTransaction"] = (
                stop_loss_order_cancel_transaction
            )
        if stop_loss_order_transaction is not UNSET:
            field_dict["stopLossOrderTransaction"] = stop_loss_order_transaction
        if stop_loss_order_fill_transaction is not UNSET:
            field_dict["stopLossOrderFillTransaction"] = (
                stop_loss_order_fill_transaction
            )
        if stop_loss_order_created_cancel_transaction is not UNSET:
            field_dict["stopLossOrderCreatedCancelTransaction"] = (
                stop_loss_order_created_cancel_transaction
            )
        if trailing_stop_loss_order_cancel_transaction is not UNSET:
            field_dict["trailingStopLossOrderCancelTransaction"] = (
                trailing_stop_loss_order_cancel_transaction
            )
        if trailing_stop_loss_order_transaction is not UNSET:
            field_dict["trailingStopLossOrderTransaction"] = (
                trailing_stop_loss_order_transaction
            )
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.take_profit_order_transaction import TakeProfitOrderTransaction
        from ..models.stop_loss_order_transaction import StopLossOrderTransaction
        from ..models.order_fill_transaction import OrderFillTransaction
        from ..models.order_cancel_transaction import OrderCancelTransaction
        from ..models.trailing_stop_loss_order_transaction import (
            TrailingStopLossOrderTransaction,
        )

        d = src_dict.copy()
        _take_profit_order_cancel_transaction = d.pop(
            "takeProfitOrderCancelTransaction", UNSET
        )
        take_profit_order_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_take_profit_order_cancel_transaction, Unset):
            take_profit_order_cancel_transaction = UNSET
        else:
            take_profit_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _take_profit_order_cancel_transaction
            )

        _take_profit_order_transaction = d.pop("takeProfitOrderTransaction", UNSET)
        take_profit_order_transaction: Union[Unset, TakeProfitOrderTransaction]
        if isinstance(_take_profit_order_transaction, Unset):
            take_profit_order_transaction = UNSET
        else:
            take_profit_order_transaction = TakeProfitOrderTransaction.from_dict(
                _take_profit_order_transaction
            )

        _take_profit_order_fill_transaction = d.pop(
            "takeProfitOrderFillTransaction", UNSET
        )
        take_profit_order_fill_transaction: Union[Unset, OrderFillTransaction]
        if isinstance(_take_profit_order_fill_transaction, Unset):
            take_profit_order_fill_transaction = UNSET
        else:
            take_profit_order_fill_transaction = OrderFillTransaction.from_dict(
                _take_profit_order_fill_transaction
            )

        _take_profit_order_created_cancel_transaction = d.pop(
            "takeProfitOrderCreatedCancelTransaction", UNSET
        )
        take_profit_order_created_cancel_transaction: Union[
            Unset, OrderCancelTransaction
        ]
        if isinstance(_take_profit_order_created_cancel_transaction, Unset):
            take_profit_order_created_cancel_transaction = UNSET
        else:
            take_profit_order_created_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _take_profit_order_created_cancel_transaction
                )
            )

        _stop_loss_order_cancel_transaction = d.pop(
            "stopLossOrderCancelTransaction", UNSET
        )
        stop_loss_order_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_stop_loss_order_cancel_transaction, Unset):
            stop_loss_order_cancel_transaction = UNSET
        else:
            stop_loss_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _stop_loss_order_cancel_transaction
            )

        _stop_loss_order_transaction = d.pop("stopLossOrderTransaction", UNSET)
        stop_loss_order_transaction: Union[Unset, StopLossOrderTransaction]
        if isinstance(_stop_loss_order_transaction, Unset):
            stop_loss_order_transaction = UNSET
        else:
            stop_loss_order_transaction = StopLossOrderTransaction.from_dict(
                _stop_loss_order_transaction
            )

        _stop_loss_order_fill_transaction = d.pop("stopLossOrderFillTransaction", UNSET)
        stop_loss_order_fill_transaction: Union[Unset, OrderFillTransaction]
        if isinstance(_stop_loss_order_fill_transaction, Unset):
            stop_loss_order_fill_transaction = UNSET
        else:
            stop_loss_order_fill_transaction = OrderFillTransaction.from_dict(
                _stop_loss_order_fill_transaction
            )

        _stop_loss_order_created_cancel_transaction = d.pop(
            "stopLossOrderCreatedCancelTransaction", UNSET
        )
        stop_loss_order_created_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_stop_loss_order_created_cancel_transaction, Unset):
            stop_loss_order_created_cancel_transaction = UNSET
        else:
            stop_loss_order_created_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _stop_loss_order_created_cancel_transaction
                )
            )

        _trailing_stop_loss_order_cancel_transaction = d.pop(
            "trailingStopLossOrderCancelTransaction", UNSET
        )
        trailing_stop_loss_order_cancel_transaction: Union[
            Unset, OrderCancelTransaction
        ]
        if isinstance(_trailing_stop_loss_order_cancel_transaction, Unset):
            trailing_stop_loss_order_cancel_transaction = UNSET
        else:
            trailing_stop_loss_order_cancel_transaction = (
                OrderCancelTransaction.from_dict(
                    _trailing_stop_loss_order_cancel_transaction
                )
            )

        _trailing_stop_loss_order_transaction = d.pop(
            "trailingStopLossOrderTransaction", UNSET
        )
        trailing_stop_loss_order_transaction: Union[
            Unset, TrailingStopLossOrderTransaction
        ]
        if isinstance(_trailing_stop_loss_order_transaction, Unset):
            trailing_stop_loss_order_transaction = UNSET
        else:
            trailing_stop_loss_order_transaction = (
                TrailingStopLossOrderTransaction.from_dict(
                    _trailing_stop_loss_order_transaction
                )
            )

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        set_trade_dependent_orders_response_200 = cls(
            take_profit_order_cancel_transaction=take_profit_order_cancel_transaction,
            take_profit_order_transaction=take_profit_order_transaction,
            take_profit_order_fill_transaction=take_profit_order_fill_transaction,
            take_profit_order_created_cancel_transaction=take_profit_order_created_cancel_transaction,
            stop_loss_order_cancel_transaction=stop_loss_order_cancel_transaction,
            stop_loss_order_transaction=stop_loss_order_transaction,
            stop_loss_order_fill_transaction=stop_loss_order_fill_transaction,
            stop_loss_order_created_cancel_transaction=stop_loss_order_created_cancel_transaction,
            trailing_stop_loss_order_cancel_transaction=trailing_stop_loss_order_cancel_transaction,
            trailing_stop_loss_order_transaction=trailing_stop_loss_order_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )

        set_trade_dependent_orders_response_200.additional_properties = d
        return set_trade_dependent_orders_response_200

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
