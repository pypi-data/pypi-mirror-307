from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .trailing_stop_loss_order_reject_transaction_reason import (
    TrailingStopLossOrderRejectTransactionReason,
)
from .trailing_stop_loss_order_reject_transaction_reject_reason import (
    TrailingStopLossOrderRejectTransactionRejectReason,
)
from .trailing_stop_loss_order_reject_transaction_time_in_force import (
    TrailingStopLossOrderRejectTransactionTimeInForce,
)
from .trailing_stop_loss_order_reject_transaction_trigger_condition import (
    TrailingStopLossOrderRejectTransactionTriggerCondition,
)
from .trailing_stop_loss_order_reject_transaction_type import (
    TrailingStopLossOrderRejectTransactionType,
)
from typing import Optional, TypeVar

T = TypeVar("T", bound="TrailingStopLossOrderRejectTransaction")


@dataclasses.dataclass
class TrailingStopLossOrderRejectTransaction:
    """A TrailingStopLossOrderRejectTransaction represents the rejection of the creation of a TrailingStopLoss Order.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TrailingStopLossOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "TRAILING_STOP_LOSS_ORDER_REJECT" in a TrailingStopLossOrderRejectTransaction.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        distance (Union[Unset, str]): The price distance (in price units) specified for the TrailingStopLoss Order.
        time_in_force (Union[Unset, TrailingStopLossOrderRejectTransactionTimeInForce]): The time-in-force requested for
            the TrailingStopLoss Order. Restricted to "GTC", "GFD" and "GTD" for TrailingStopLoss Orders.
        gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, TrailingStopLossOrderRejectTransactionTriggerCondition]): Specification of which
            price component should be used when determining if an Order should be triggered and filled. This allows Orders
            to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid
            for buy) price depending on the desired behaviour. Orders are always filled using their default price component.
            This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
            condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
            transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
            is set to the default value when indicating the distance from an Order's trigger price, and will always provide
            the default trigger condition when creating or modifying an Order.
            A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
            value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
            a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
        reason (Union[Unset, TrailingStopLossOrderRejectTransactionReason]): The reason that the Trailing Stop Loss
            Order was initiated
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        order_fill_transaction_id (Union[Unset, str]): The ID of the OrderFill Transaction that caused this Order to be
            created (only provided if this Order was created automatically when another Order was filled).
        intended_replaces_order_id (Union[Unset, str]): The ID of the Order that this Order was intended to replace
            (only provided if this Order was intended to replace an existing Order).
        reject_reason (Union[Unset, TrailingStopLossOrderRejectTransactionRejectReason]): The reason that the Reject
            Transaction was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[TrailingStopLossOrderRejectTransactionType]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    distance: Optional[str]
    time_in_force: Optional[TrailingStopLossOrderRejectTransactionTimeInForce]
    gtd_time: Optional[str]
    trigger_condition: Optional[TrailingStopLossOrderRejectTransactionTriggerCondition]
    reason: Optional[TrailingStopLossOrderRejectTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    order_fill_transaction_id: Optional[str]
    intended_replaces_order_id: Optional[str]
    reject_reason: Optional[TrailingStopLossOrderRejectTransactionRejectReason]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "TrailingStopLossOrderRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
