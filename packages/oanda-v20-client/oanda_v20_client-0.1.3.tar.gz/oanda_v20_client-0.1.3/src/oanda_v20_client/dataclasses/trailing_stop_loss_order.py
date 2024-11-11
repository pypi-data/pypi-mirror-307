from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .trailing_stop_loss_order_state import TrailingStopLossOrderState
from .trailing_stop_loss_order_time_in_force import TrailingStopLossOrderTimeInForce
from .trailing_stop_loss_order_trigger_condition import (
    TrailingStopLossOrderTriggerCondition,
)
from .trailing_stop_loss_order_type import TrailingStopLossOrderType
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="TrailingStopLossOrder")


@dataclasses.dataclass
class TrailingStopLossOrder:
    """A TrailingStopLossOrder is an order that is linked to an open Trade and created with a price distance. The price
    distance is used to calculate a trailing stop value for the order that is in the losing direction from the market
    price at the time of the order's creation. The trailing stop value will follow the market price as it moves in the
    winning direction, and the order will filled (closing the Trade) by the first price that is equal to or worse than
    the trailing stop value. A TrailingStopLossOrder cannot be used to open a new Position.

        Attributes:
            id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
            create_time (Union[Unset, str]): The time when the Order was created.
            state (Union[Unset, TrailingStopLossOrderState]): The current state of the Order.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            type (Union[Unset, TrailingStopLossOrderType]): The type of the Order. Always set to "TRAILING_STOP_LOSS" for
                Trailing Stop Loss Orders.
            trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
            client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
                breached.
            distance (Union[Unset, str]): The price distance (in price units) specified for the TrailingStopLoss Order.
            time_in_force (Union[Unset, TrailingStopLossOrderTimeInForce]): The time-in-force requested for the
                TrailingStopLoss Order. Restricted to "GTC", "GFD" and "GTD" for TrailingStopLoss Orders.
            gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
                "GTD".
            trigger_condition (Union[Unset, TrailingStopLossOrderTriggerCondition]): Specification of which price component
                should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered
                based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price
                depending on the desired behaviour. Orders are always filled using their default price component.
                This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
                condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
                transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
                is set to the default value when indicating the distance from an Order's trigger price, and will always provide
                the default trigger condition when creating or modifying an Order.
                A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
                value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
                a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
            trailing_stop_value (Union[Unset, str]): The trigger price for the Trailing Stop Loss Order. The trailing stop
                value will trail (follow) the market price by the TSL order's configured "distance" as the market price moves in
                the winning direction. If the market price moves to a level that is equal to or worse than the trailing stop
                value, the order will be filled and the Trade will be closed.
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

    id: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    state: Union[Unset, TrailingStopLossOrderState] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    type: Union[Unset, TrailingStopLossOrderType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TrailingStopLossOrderTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[Unset, TrailingStopLossOrderTriggerCondition] = UNSET
    trailing_stop_value: Union[Unset, str] = UNSET
    filling_transaction_id: Union[Unset, str] = UNSET
    filled_time: Union[Unset, str] = UNSET
    trade_opened_id: Union[Unset, str] = UNSET
    trade_reduced_id: Union[Unset, str] = UNSET
    trade_closed_i_ds: Union[Unset, List[str]] = UNSET
    cancelling_transaction_id: Union[Unset, str] = UNSET
    cancelled_time: Union[Unset, str] = UNSET
    replaces_order_id: Union[Unset, str] = UNSET
    replaced_by_order_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrailingStopLossOrder":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
