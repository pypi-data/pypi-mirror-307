from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .take_profit_order_reject_transaction_reason import (
    TakeProfitOrderRejectTransactionReason,
)
from .take_profit_order_reject_transaction_reject_reason import (
    TakeProfitOrderRejectTransactionRejectReason,
)
from .take_profit_order_reject_transaction_time_in_force import (
    TakeProfitOrderRejectTransactionTimeInForce,
)
from .take_profit_order_reject_transaction_trigger_condition import (
    TakeProfitOrderRejectTransactionTriggerCondition,
)
from .take_profit_order_reject_transaction_type import (
    TakeProfitOrderRejectTransactionType,
)
from typing import TypeVar, Union

T = TypeVar("T", bound="TakeProfitOrderRejectTransaction")


@dataclasses.dataclass
class TakeProfitOrderRejectTransaction:
    """A TakeProfitOrderRejectTransaction represents the rejection of the creation of a TakeProfit Order.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TakeProfitOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "TAKE_PROFIT_ORDER_REJECT" in a TakeProfitOrderRejectTransaction.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        price (Union[Unset, str]): The price threshold specified for the TakeProfit Order. The associated Trade will be
            closed by a market price that is equal to or better than this threshold.
        time_in_force (Union[Unset, TakeProfitOrderRejectTransactionTimeInForce]): The time-in-force requested for the
            TakeProfit Order. Restricted to "GTC", "GFD" and "GTD" for TakeProfit Orders.
        gtd_time (Union[Unset, str]): The date/time when the TakeProfit Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, TakeProfitOrderRejectTransactionTriggerCondition]): Specification of which price
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
        reason (Union[Unset, TakeProfitOrderRejectTransactionReason]): The reason that the Take Profit Order was
            initiated
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        order_fill_transaction_id (Union[Unset, str]): The ID of the OrderFill Transaction that caused this Order to be
            created (only provided if this Order was created automatically when another Order was filled).
        intended_replaces_order_id (Union[Unset, str]): The ID of the Order that this Order was intended to replace
            (only provided if this Order was intended to replace an existing Order).
        reject_reason (Union[Unset, TakeProfitOrderRejectTransactionRejectReason]): The reason that the Reject
            Transaction was created"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, TakeProfitOrderRejectTransactionType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TakeProfitOrderRejectTransactionTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[
        Unset, TakeProfitOrderRejectTransactionTriggerCondition
    ] = UNSET
    reason: Union[Unset, TakeProfitOrderRejectTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    order_fill_transaction_id: Union[Unset, str] = UNSET
    intended_replaces_order_id: Union[Unset, str] = UNSET
    reject_reason: Union[Unset, TakeProfitOrderRejectTransactionRejectReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TakeProfitOrderRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
