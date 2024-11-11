from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .stop_loss_order_state import StopLossOrderState
from .stop_loss_order_time_in_force import StopLossOrderTimeInForce
from .stop_loss_order_trigger_condition import StopLossOrderTriggerCondition
from .stop_loss_order_type import StopLossOrderType
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="StopLossOrder")


@dataclasses.dataclass
class StopLossOrder:
    """A StopLossOrder is an order that is linked to an open Trade and created with a price threshold. The Order will be
    filled (closing the Trade) by the first price that is equal to or worse than the threshold. A StopLossOrder cannot
    be used to open a new Position.

        Attributes:
            id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
            create_time (Union[Unset, str]): The time when the Order was created.
            state (Union[Unset, StopLossOrderState]): The current state of the Order.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            type (Union[Unset, StopLossOrderType]): The type of the Order. Always set to "STOP_LOSS" for Stop Loss Orders.
            guaranteed_execution_premium (Union[Unset, str]): The premium that will be charged if the Stop Loss Order is
                guaranteed and the Order is filled at the guaranteed price. It is in price units and is charged for each unit of
                the Trade.
            trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
            client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
                breached.
            price (Union[Unset, str]): The price threshold specified for the Stop Loss Order. If the guaranteed flag is
                false, the associated Trade will be closed by a market price that is equal to or worse than this threshold. If
                the flag is true the associated Trade will be closed at this price.
            distance (Union[Unset, str]): Specifies the distance (in price units) from the Account's current price to use as
                the Stop Loss Order price. If the Trade is short the Instrument's bid price is used, and for long Trades the ask
                is used.
            time_in_force (Union[Unset, StopLossOrderTimeInForce]): The time-in-force requested for the StopLoss Order.
                Restricted to "GTC", "GFD" and "GTD" for StopLoss Orders.
            gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
                "GTD".
            trigger_condition (Union[Unset, StopLossOrderTriggerCondition]): Specification of which price component should
                be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on
                the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on
                the desired behaviour. Orders are always filled using their default price component.
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
            filling_transaction_id (Union[Unset, str]): ID of the Transaction that filled this Order (only provided when the
                Order's state is FILLED)
            filled_time (Union[Unset, str]): Date/time when the Order was filled (only provided when the Order's state is
                FILLED)
            trade_opened_id (Union[Unset, str]): Trade ID of Trade opened when the Order was filled (only provided when the
                Order's state is FILLED and a Trade was opened as a result of the fill)
            trade_reduced_id (Union[Unset, str]): Trade ID of Trade reduced when the Order was filled (only provided when
                the Order's state is FILLED and a Trade was reduced as a result of the fill)
            trade_closed_i_ds (Union[Unset, List[str]]): Trade IDs of Trades closed when the Order was filled (only provided
                when the Order's state is FILLED and one or more Trades were closed as a result of the fill)
            cancelling_transaction_id (Union[Unset, str]): ID of the Transaction that cancelled the Order (only provided
                when the Order's state is CANCELLED)
            cancelled_time (Union[Unset, str]): Date/time when the Order was cancelled (only provided when the state of the
                Order is CANCELLED)
            replaces_order_id (Union[Unset, str]): The ID of the Order that was replaced by this Order (only provided if
                this Order was created as part of a cancel/replace).
            replaced_by_order_id (Union[Unset, str]): The ID of the Order that replaced this Order (only provided if this
                Order was cancelled as part of a cancel/replace)."""

    id: Optional[str]
    create_time: Optional[str]
    state: Optional[StopLossOrderState]
    client_extensions: Optional["ClientExtensions"]
    type: Optional[StopLossOrderType]
    guaranteed_execution_premium: Optional[str]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    price: Optional[str]
    distance: Optional[str]
    time_in_force: Optional[StopLossOrderTimeInForce]
    gtd_time: Optional[str]
    trigger_condition: Optional[StopLossOrderTriggerCondition]
    guaranteed: Optional[bool]
    filling_transaction_id: Optional[str]
    filled_time: Optional[str]
    trade_opened_id: Optional[str]
    trade_reduced_id: Optional[str]
    trade_closed_i_ds: Optional[List[str]]
    cancelling_transaction_id: Optional[str]
    cancelled_time: Optional[str]
    replaces_order_id: Optional[str]
    replaced_by_order_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StopLossOrder":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
