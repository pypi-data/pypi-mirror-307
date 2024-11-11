from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .stop_loss_order_transaction_reason import StopLossOrderTransactionReason
from .stop_loss_order_transaction_time_in_force import (
    StopLossOrderTransactionTimeInForce,
)
from .stop_loss_order_transaction_trigger_condition import (
    StopLossOrderTransactionTriggerCondition,
)
from .stop_loss_order_transaction_type import StopLossOrderTransactionType
from typing import TypeVar, Union

T = TypeVar("T", bound="StopLossOrderTransaction")


@dataclasses.dataclass
class StopLossOrderTransaction:
    """A StopLossOrderTransaction represents the creation of a StopLoss Order in the user's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, StopLossOrderTransactionType]): The Type of the Transaction. Always set to "STOP_LOSS_ORDER"
            in a StopLossOrderTransaction.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        price (Union[Unset, str]): The price threshold specified for the Stop Loss Order. If the guaranteed flag is
            false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If
            the flag is true the associated Trade will be closed at this price.
        distance (Union[Unset, str]): Specifies the distance (in price units) from the Account's current price to use as
            the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask
            is used.
        time_in_force (Union[Unset, StopLossOrderTransactionTimeInForce]): The time-in-force requested for the StopLoss
            Order. Restricted to "GTC", "GFD" and "GTD" for StopLoss Orders.
        gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, StopLossOrderTransactionTriggerCondition]): Specification of which price
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
        guaranteed (Union[Unset, bool]): Flag indicating that the Stop Loss Order is guaranteed. The default value
            depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be true, for
            DISABLED or ENABLED the default is false.
        guaranteed_execution_premium (Union[Unset, str]): The fee that will be charged if the Stop Loss Order is
            guaranteed and the Order is filled at the guaranteed price. The value is determined at Order creation time. It
            is in price units and is charged for each unit of the Trade.
        reason (Union[Unset, StopLossOrderTransactionReason]): The reason that the Stop Loss Order was initiated
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
        order_fill_transaction_id (Union[Unset, str]): The ID of the OrderFill Transaction that caused this Order to be
            created (only provided if this Order was created automatically when another Order was filled).
        replaces_order_id (Union[Unset, str]): The ID of the Order that this Order replaces (only provided if this Order
            replaces an existing Order).
        cancelling_transaction_id (Union[Unset, str]): The ID of the Transaction that cancels the replaced Order (only
            provided if this Order replaces an existing Order)."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, StopLossOrderTransactionType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, StopLossOrderTransactionTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[Unset, StopLossOrderTransactionTriggerCondition] = UNSET
    guaranteed: Union[Unset, bool] = UNSET
    guaranteed_execution_premium: Union[Unset, str] = UNSET
    reason: Union[Unset, StopLossOrderTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    order_fill_transaction_id: Union[Unset, str] = UNSET
    replaces_order_id: Union[Unset, str] = UNSET
    cancelling_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StopLossOrderTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
