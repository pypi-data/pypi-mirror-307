from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .take_profit_order_transaction_reason import TakeProfitOrderTransactionReason
from .take_profit_order_transaction_reason import (
    check_take_profit_order_transaction_reason,
)
from .take_profit_order_transaction_time_in_force import (
    TakeProfitOrderTransactionTimeInForce,
)
from .take_profit_order_transaction_time_in_force import (
    check_take_profit_order_transaction_time_in_force,
)
from .take_profit_order_transaction_trigger_condition import (
    TakeProfitOrderTransactionTriggerCondition,
)
from .take_profit_order_transaction_trigger_condition import (
    check_take_profit_order_transaction_trigger_condition,
)
from .take_profit_order_transaction_type import TakeProfitOrderTransactionType
from .take_profit_order_transaction_type import check_take_profit_order_transaction_type
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="TakeProfitOrderTransaction")


@dataclasses.dataclass
class TakeProfitOrderTransaction:
    """A TakeProfitOrderTransaction represents the creation of a TakeProfit Order in the user's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TakeProfitOrderTransactionType]): The Type of the Transaction. Always set to
            "TAKE_PROFIT_ORDER" in a TakeProfitOrderTransaction.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        price (Union[Unset, str]): The price threshold specified for the TakeProfit Order. The associated Trade will be
            closed by a market price that is equal to or better than this threshold.
        time_in_force (Union[Unset, TakeProfitOrderTransactionTimeInForce]): The time-in-force requested for the
            TakeProfit Order. Restricted to "GTC", "GFD" and "GTD" for TakeProfit Orders.
        gtd_time (Union[Unset, str]): The date/time when the TakeProfit Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, TakeProfitOrderTransactionTriggerCondition]): Specification of which price
            component should be used when determining if an Order should be triggered and filled. This allows Orders to be
            triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy)
            price depending on the desired behaviour. Orders are always filled using their default price component.
            This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
            condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
            transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
            is set to the default value when indicating the distance from an Order's trigger price, and will always provide
            the default trigger condition when creating or modifying an Order.
            A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
            value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
            a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
        reason (Union[Unset, TakeProfitOrderTransactionReason]): The reason that the Take Profit Order was initiated
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        order_fill_transaction_id (Union[Unset, str]): The ID of the OrderFill Transaction that caused this Order to be
            created (only provided if this Order was created automatically when another Order was filled).
        replaces_order_id (Union[Unset, str]): The ID of the Order that this Order replaces (only provided if this Order
            replaces an existing Order).
        cancelling_transaction_id (Union[Unset, str]): The ID of the Transaction that cancels the replaced Order (only
            provided if this Order replaces an existing Order)."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[TakeProfitOrderTransactionType]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    price: Optional[str]
    time_in_force: Optional[TakeProfitOrderTransactionTimeInForce]
    gtd_time: Optional[str]
    trigger_condition: Optional[TakeProfitOrderTransactionTriggerCondition]
    reason: Optional[TakeProfitOrderTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    order_fill_transaction_id: Optional[str]
    replaces_order_id: Optional[str]
    cancelling_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[TakeProfitOrderTransactionType]
        if _type is None:
            type = None
        else:
            type = check_take_profit_order_transaction_type(_type)
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        price = d.pop("price", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[TakeProfitOrderTransactionTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_take_profit_order_transaction_time_in_force(
                _time_in_force
            )
        gtd_time = d.pop("gtdTime", None)
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[TakeProfitOrderTransactionTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = None
        else:
            trigger_condition = check_take_profit_order_transaction_trigger_condition(
                _trigger_condition
            )
        _reason = d.pop("reason", None)
        reason: Optional[TakeProfitOrderTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_take_profit_order_transaction_reason(_reason)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        order_fill_transaction_id = d.pop("orderFillTransactionID", None)
        replaces_order_id = d.pop("replacesOrderID", None)
        cancelling_transaction_id = d.pop("cancellingTransactionID", None)
        take_profit_order_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            price=price,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            reason=reason,
            client_extensions=client_extensions,
            order_fill_transaction_id=order_fill_transaction_id,
            replaces_order_id=replaces_order_id,
            cancelling_transaction_id=cancelling_transaction_id,
        )
        take_profit_order_transaction.additional_properties = d
        return take_profit_order_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
