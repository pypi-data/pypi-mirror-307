from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .stop_loss_details import StopLossDetails
from .stop_order_reject_transaction_position_fill import (
    StopOrderRejectTransactionPositionFill,
)
from .stop_order_reject_transaction_reason import StopOrderRejectTransactionReason
from .stop_order_reject_transaction_reject_reason import (
    StopOrderRejectTransactionRejectReason,
)
from .stop_order_reject_transaction_time_in_force import (
    StopOrderRejectTransactionTimeInForce,
)
from .stop_order_reject_transaction_trigger_condition import (
    StopOrderRejectTransactionTriggerCondition,
)
from .stop_order_reject_transaction_type import StopOrderRejectTransactionType
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="StopOrderRejectTransaction")


@dataclasses.dataclass
class StopOrderRejectTransaction:
    """A StopOrderRejectTransaction represents the rejection of the creation of a Stop Order.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, StopOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "STOP_ORDER_REJECT" in a StopOrderRejectTransaction.
        instrument (Union[Unset, str]): The Stop Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Stop Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        price (Union[Unset, str]): The price threshold specified for the Stop Order. The Stop Order will only be filled
            by a market price that is equal to or worse than this price.
        price_bound (Union[Unset, str]): The worst market price that may be used to fill this Stop Order. If the market
            gaps and crosses through both the price and the priceBound, the Stop Order will be cancelled instead of being
            filled.
        time_in_force (Union[Unset, StopOrderRejectTransactionTimeInForce]): The time-in-force requested for the Stop
            Order.
        gtd_time (Union[Unset, str]): The date/time when the Stop Order will be cancelled if its timeInForce is "GTD".
        position_fill (Union[Unset, StopOrderRejectTransactionPositionFill]): Specification of how Positions in the
            Account are modified when the Order is filled.
        trigger_condition (Union[Unset, StopOrderRejectTransactionTriggerCondition]): Specification of which price
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
        reason (Union[Unset, StopOrderRejectTransactionReason]): The reason that the Stop Order was initiated
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        take_profit_on_fill (Union[Unset, TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit
            Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring
            a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
        stop_loss_on_fill (Union[Unset, StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to
            be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop
            Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
        trailing_stop_loss_on_fill (Union[Unset, TrailingStopLossDetails]): TrailingStopLossDetails specifies the
            details of a Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is
            filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order
            is modified directly through the Trade.
        trade_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        intended_replaces_order_id (Union[Unset, str]): The ID of the Order that this Order was intended to replace
            (only provided if this Order was intended to replace an existing Order).
        reject_reason (Union[Unset, StopOrderRejectTransactionRejectReason]): The reason that the Reject Transaction was
            created"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, StopOrderRejectTransactionType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    price_bound: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, StopOrderRejectTransactionTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    position_fill: Union[Unset, StopOrderRejectTransactionPositionFill] = UNSET
    trigger_condition: Union[Unset, StopOrderRejectTransactionTriggerCondition] = UNSET
    reason: Union[Unset, StopOrderRejectTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    intended_replaces_order_id: Union[Unset, str] = UNSET
    reject_reason: Union[Unset, StopOrderRejectTransactionRejectReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StopOrderRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
