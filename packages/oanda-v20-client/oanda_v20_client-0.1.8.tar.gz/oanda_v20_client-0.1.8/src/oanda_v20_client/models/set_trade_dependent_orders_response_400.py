from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.trailing_stop_loss_order_reject_transaction import (
        TrailingStopLossOrderRejectTransaction,
    )
    from ..models.stop_loss_order_reject_transaction import (
        StopLossOrderRejectTransaction,
    )
    from ..models.take_profit_order_reject_transaction import (
        TakeProfitOrderRejectTransaction,
    )
    from ..models.order_cancel_reject_transaction import OrderCancelRejectTransaction


T = TypeVar("T", bound="SetTradeDependentOrdersResponse400")


@_attrs_define
class SetTradeDependentOrdersResponse400:
    """
    Attributes:
        take_profit_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
            OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
        take_profit_order_reject_transaction (Union[Unset, TakeProfitOrderRejectTransaction]): A
            TakeProfitOrderRejectTransaction represents the rejection of the creation of a TakeProfit Order.
        stop_loss_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
            OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
        stop_loss_order_reject_transaction (Union[Unset, StopLossOrderRejectTransaction]): A
            StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.
        trailing_stop_loss_order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An
            OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.
        trailing_stop_loss_order_reject_transaction (Union[Unset, TrailingStopLossOrderRejectTransaction]): A
            TrailingStopLossOrderRejectTransaction represents the rejection of the creation of a TrailingStopLoss Order.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request.
        error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
            errors.
        error_message (Union[Unset, str]): The human-readable description of the error that has occurred.
    """

    take_profit_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    take_profit_order_reject_transaction: Union[
        Unset, "TakeProfitOrderRejectTransaction"
    ] = UNSET
    stop_loss_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    stop_loss_order_reject_transaction: Union[
        Unset, "StopLossOrderRejectTransaction"
    ] = UNSET
    trailing_stop_loss_order_cancel_reject_transaction: Union[
        Unset, "OrderCancelRejectTransaction"
    ] = UNSET
    trailing_stop_loss_order_reject_transaction: Union[
        Unset, "TrailingStopLossOrderRejectTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        take_profit_order_cancel_reject_transaction: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.take_profit_order_cancel_reject_transaction, Unset):
            take_profit_order_cancel_reject_transaction = (
                self.take_profit_order_cancel_reject_transaction.to_dict()
            )

        take_profit_order_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_order_reject_transaction, Unset):
            take_profit_order_reject_transaction = (
                self.take_profit_order_reject_transaction.to_dict()
            )

        stop_loss_order_cancel_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_cancel_reject_transaction, Unset):
            stop_loss_order_cancel_reject_transaction = (
                self.stop_loss_order_cancel_reject_transaction.to_dict()
            )

        stop_loss_order_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order_reject_transaction, Unset):
            stop_loss_order_reject_transaction = (
                self.stop_loss_order_reject_transaction.to_dict()
            )

        trailing_stop_loss_order_cancel_reject_transaction: Union[
            Unset, Dict[str, Any]
        ] = UNSET
        if not isinstance(
            self.trailing_stop_loss_order_cancel_reject_transaction, Unset
        ):
            trailing_stop_loss_order_cancel_reject_transaction = (
                self.trailing_stop_loss_order_cancel_reject_transaction.to_dict()
            )

        trailing_stop_loss_order_reject_transaction: Union[Unset, Dict[str, Any]] = (
            UNSET
        )
        if not isinstance(self.trailing_stop_loss_order_reject_transaction, Unset):
            trailing_stop_loss_order_reject_transaction = (
                self.trailing_stop_loss_order_reject_transaction.to_dict()
            )

        last_transaction_id = self.last_transaction_id

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        error_code = self.error_code

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if take_profit_order_cancel_reject_transaction is not UNSET:
            field_dict["takeProfitOrderCancelRejectTransaction"] = (
                take_profit_order_cancel_reject_transaction
            )
        if take_profit_order_reject_transaction is not UNSET:
            field_dict["takeProfitOrderRejectTransaction"] = (
                take_profit_order_reject_transaction
            )
        if stop_loss_order_cancel_reject_transaction is not UNSET:
            field_dict["stopLossOrderCancelRejectTransaction"] = (
                stop_loss_order_cancel_reject_transaction
            )
        if stop_loss_order_reject_transaction is not UNSET:
            field_dict["stopLossOrderRejectTransaction"] = (
                stop_loss_order_reject_transaction
            )
        if trailing_stop_loss_order_cancel_reject_transaction is not UNSET:
            field_dict["trailingStopLossOrderCancelRejectTransaction"] = (
                trailing_stop_loss_order_cancel_reject_transaction
            )
        if trailing_stop_loss_order_reject_transaction is not UNSET:
            field_dict["trailingStopLossOrderRejectTransaction"] = (
                trailing_stop_loss_order_reject_transaction
            )
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trailing_stop_loss_order_reject_transaction import (
            TrailingStopLossOrderRejectTransaction,
        )
        from ..models.stop_loss_order_reject_transaction import (
            StopLossOrderRejectTransaction,
        )
        from ..models.take_profit_order_reject_transaction import (
            TakeProfitOrderRejectTransaction,
        )
        from ..models.order_cancel_reject_transaction import (
            OrderCancelRejectTransaction,
        )

        d = src_dict.copy()
        _take_profit_order_cancel_reject_transaction = d.pop(
            "takeProfitOrderCancelRejectTransaction", UNSET
        )
        take_profit_order_cancel_reject_transaction: Union[
            Unset, OrderCancelRejectTransaction
        ]
        if isinstance(_take_profit_order_cancel_reject_transaction, Unset):
            take_profit_order_cancel_reject_transaction = UNSET
        else:
            take_profit_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _take_profit_order_cancel_reject_transaction
                )
            )

        _take_profit_order_reject_transaction = d.pop(
            "takeProfitOrderRejectTransaction", UNSET
        )
        take_profit_order_reject_transaction: Union[
            Unset, TakeProfitOrderRejectTransaction
        ]
        if isinstance(_take_profit_order_reject_transaction, Unset):
            take_profit_order_reject_transaction = UNSET
        else:
            take_profit_order_reject_transaction = (
                TakeProfitOrderRejectTransaction.from_dict(
                    _take_profit_order_reject_transaction
                )
            )

        _stop_loss_order_cancel_reject_transaction = d.pop(
            "stopLossOrderCancelRejectTransaction", UNSET
        )
        stop_loss_order_cancel_reject_transaction: Union[
            Unset, OrderCancelRejectTransaction
        ]
        if isinstance(_stop_loss_order_cancel_reject_transaction, Unset):
            stop_loss_order_cancel_reject_transaction = UNSET
        else:
            stop_loss_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _stop_loss_order_cancel_reject_transaction
                )
            )

        _stop_loss_order_reject_transaction = d.pop(
            "stopLossOrderRejectTransaction", UNSET
        )
        stop_loss_order_reject_transaction: Union[Unset, StopLossOrderRejectTransaction]
        if isinstance(_stop_loss_order_reject_transaction, Unset):
            stop_loss_order_reject_transaction = UNSET
        else:
            stop_loss_order_reject_transaction = (
                StopLossOrderRejectTransaction.from_dict(
                    _stop_loss_order_reject_transaction
                )
            )

        _trailing_stop_loss_order_cancel_reject_transaction = d.pop(
            "trailingStopLossOrderCancelRejectTransaction", UNSET
        )
        trailing_stop_loss_order_cancel_reject_transaction: Union[
            Unset, OrderCancelRejectTransaction
        ]
        if isinstance(_trailing_stop_loss_order_cancel_reject_transaction, Unset):
            trailing_stop_loss_order_cancel_reject_transaction = UNSET
        else:
            trailing_stop_loss_order_cancel_reject_transaction = (
                OrderCancelRejectTransaction.from_dict(
                    _trailing_stop_loss_order_cancel_reject_transaction
                )
            )

        _trailing_stop_loss_order_reject_transaction = d.pop(
            "trailingStopLossOrderRejectTransaction", UNSET
        )
        trailing_stop_loss_order_reject_transaction: Union[
            Unset, TrailingStopLossOrderRejectTransaction
        ]
        if isinstance(_trailing_stop_loss_order_reject_transaction, Unset):
            trailing_stop_loss_order_reject_transaction = UNSET
        else:
            trailing_stop_loss_order_reject_transaction = (
                TrailingStopLossOrderRejectTransaction.from_dict(
                    _trailing_stop_loss_order_reject_transaction
                )
            )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        error_code = d.pop("errorCode", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        set_trade_dependent_orders_response_400 = cls(
            take_profit_order_cancel_reject_transaction=take_profit_order_cancel_reject_transaction,
            take_profit_order_reject_transaction=take_profit_order_reject_transaction,
            stop_loss_order_cancel_reject_transaction=stop_loss_order_cancel_reject_transaction,
            stop_loss_order_reject_transaction=stop_loss_order_reject_transaction,
            trailing_stop_loss_order_cancel_reject_transaction=trailing_stop_loss_order_cancel_reject_transaction,
            trailing_stop_loss_order_reject_transaction=trailing_stop_loss_order_reject_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
            error_code=error_code,
            error_message=error_message,
        )

        set_trade_dependent_orders_response_400.additional_properties = d
        return set_trade_dependent_orders_response_400

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
