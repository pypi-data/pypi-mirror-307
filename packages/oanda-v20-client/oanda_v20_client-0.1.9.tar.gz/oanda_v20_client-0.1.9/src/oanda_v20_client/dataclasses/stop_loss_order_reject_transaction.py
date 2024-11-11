from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .stop_loss_order_reject_transaction_reason import (
    StopLossOrderRejectTransactionReason,
)
from .stop_loss_order_reject_transaction_reason import (
    check_stop_loss_order_reject_transaction_reason,
)
from .stop_loss_order_reject_transaction_reject_reason import (
    StopLossOrderRejectTransactionRejectReason,
)
from .stop_loss_order_reject_transaction_reject_reason import (
    check_stop_loss_order_reject_transaction_reject_reason,
)
from .stop_loss_order_reject_transaction_time_in_force import (
    StopLossOrderRejectTransactionTimeInForce,
)
from .stop_loss_order_reject_transaction_time_in_force import (
    check_stop_loss_order_reject_transaction_time_in_force,
)
from .stop_loss_order_reject_transaction_trigger_condition import (
    StopLossOrderRejectTransactionTriggerCondition,
)
from .stop_loss_order_reject_transaction_trigger_condition import (
    check_stop_loss_order_reject_transaction_trigger_condition,
)
from .stop_loss_order_reject_transaction_type import StopLossOrderRejectTransactionType
from .stop_loss_order_reject_transaction_type import (
    check_stop_loss_order_reject_transaction_type,
)
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="StopLossOrderRejectTransaction")


@dataclasses.dataclass
class StopLossOrderRejectTransaction:
    """A StopLossOrderRejectTransaction represents the rejection of the creation of a StopLoss Order.

    Attributes:
        id (Optional[str]): The Transaction's Identifier.
        time (Optional[str]): The date/time when the Transaction was created.
        user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Optional[str]): The ID of the Account the Transaction was created for.
        batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Optional[str]): The Request ID of the request which generated the transaction.
        type (Optional[StopLossOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "STOP_LOSS_ORDER_REJECT" in a StopLossOrderRejectTransaction.
        trade_id (Optional[str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Optional[str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        price (Optional[str]): The price threshold specified for the Stop Loss Order. If the guaranteed flag is
            false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If
            the flag is true the associated Trade will be closed at this price.
        distance (Optional[str]): Specifies the distance (in price units) from the Account's current price to use as
            the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask
            is used.
        time_in_force (Optional[StopLossOrderRejectTransactionTimeInForce]): The time-in-force requested for the
            StopLoss Order. Restricted to "GTC", "GFD" and "GTD" for StopLoss Orders.
        gtd_time (Optional[str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Optional[StopLossOrderRejectTransactionTriggerCondition]): Specification of which price
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
        guaranteed (Optional[bool]): Flag indicating that the Stop Loss Order is guaranteed. The default value
            depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for
            DISABLED or ENABLED the default is false.
        reason (Optional[StopLossOrderRejectTransactionReason]): The reason that the Stop Loss Order was initiated
        client_extensions (Optional[ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        order_fill_transaction_id (Optional[str]): The ID of the OrderFill Transaction that caused this Order to be
            created (only provided if this Order was created automatically when another Order was filled).
        intended_replaces_order_id (Optional[str]): The ID of the Order that this Order was intended to replace
            (only provided if this Order was intended to replace an existing Order).
        reject_reason (Optional[StopLossOrderRejectTransactionRejectReason]): The reason that the Reject Transaction
            was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[StopLossOrderRejectTransactionType]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    price: Optional[str]
    distance: Optional[str]
    time_in_force: Optional[StopLossOrderRejectTransactionTimeInForce]
    gtd_time: Optional[str]
    trigger_condition: Optional[StopLossOrderRejectTransactionTriggerCondition]
    guaranteed: Optional[bool]
    reason: Optional[StopLossOrderRejectTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    order_fill_transaction_id: Optional[str]
    intended_replaces_order_id: Optional[str]
    reject_reason: Optional[StopLossOrderRejectTransactionRejectReason]

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
        type: Optional[StopLossOrderRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_stop_loss_order_reject_transaction_type(_type)
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        price = d.pop("price", None)
        distance = d.pop("distance", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[StopLossOrderRejectTransactionTimeInForce]
        if _time_in_force is None:
            time_in_force = None
        else:
            time_in_force = check_stop_loss_order_reject_transaction_time_in_force(
                _time_in_force
            )
        gtd_time = d.pop("gtdTime", None)
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[StopLossOrderRejectTransactionTriggerCondition]
        if _trigger_condition is None:
            trigger_condition = None
        else:
            trigger_condition = (
                check_stop_loss_order_reject_transaction_trigger_condition(
                    _trigger_condition
                )
            )
        guaranteed = d.pop("guaranteed", None)
        _reason = d.pop("reason", None)
        reason: Optional[StopLossOrderRejectTransactionReason]
        if _reason is None:
            reason = None
        else:
            reason = check_stop_loss_order_reject_transaction_reason(_reason)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if _client_extensions is None:
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        order_fill_transaction_id = d.pop("orderFillTransactionID", None)
        intended_replaces_order_id = d.pop("intendedReplacesOrderID", None)
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[StopLossOrderRejectTransactionRejectReason]
        if _reject_reason is None:
            reject_reason = None
        else:
            reject_reason = check_stop_loss_order_reject_transaction_reject_reason(
                _reject_reason
            )
        stop_loss_order_reject_transaction = cls(
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
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            guaranteed=guaranteed,
            reason=reason,
            client_extensions=client_extensions,
            order_fill_transaction_id=order_fill_transaction_id,
            intended_replaces_order_id=intended_replaces_order_id,
            reject_reason=reject_reason,
        )
        stop_loss_order_reject_transaction.additional_properties = d
        return stop_loss_order_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
