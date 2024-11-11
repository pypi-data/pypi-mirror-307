from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .market_if_touched_order_position_fill import MarketIfTouchedOrderPositionFill
from .market_if_touched_order_state import MarketIfTouchedOrderState
from .market_if_touched_order_time_in_force import MarketIfTouchedOrderTimeInForce
from .market_if_touched_order_trigger_condition import (
    MarketIfTouchedOrderTriggerCondition,
)
from .market_if_touched_order_type import MarketIfTouchedOrderType
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import List, TypeVar, Union

T = TypeVar("T", bound="MarketIfTouchedOrder")


@dataclasses.dataclass
class MarketIfTouchedOrder:
    """A MarketIfTouchedOrder is an order that is created with a price threshold, and will only be filled by a market price
    that is touches or crosses the threshold.

        Attributes:
            id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
            create_time (Union[Unset, str]): The time when the Order was created.
            state (Union[Unset, MarketIfTouchedOrderState]): The current state of the Order.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            type (Union[Unset, MarketIfTouchedOrderType]): The type of the Order. Always set to "MARKET_IF_TOUCHED" for
                Market If Touched Orders.
            instrument (Union[Unset, str]): The MarketIfTouched Order's Instrument.
            units (Union[Unset, str]): The quantity requested to be filled by the MarketIfTouched Order. A posititive number
                of units results in a long Order, and a negative number of units results in a short Order.
            price (Union[Unset, str]): The price threshold specified for the MarketIfTouched Order. The MarketIfTouched
                Order will only be filled by a market price that crosses this price from the direction of the market price at
                the time when the Order was created (the initialMarketPrice). Depending on the value of the Order's price and
                initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order.
            price_bound (Union[Unset, str]): The worst market price that may be used to fill this MarketIfTouched Order.
            time_in_force (Union[Unset, MarketIfTouchedOrderTimeInForce]): The time-in-force requested for the
                MarketIfTouched Order. Restricted to "GTC", "GFD" and "GTD" for MarketIfTouched Orders.
            gtd_time (Union[Unset, str]): The date/time when the MarketIfTouched Order will be cancelled if its timeInForce
                is "GTD".
            position_fill (Union[Unset, MarketIfTouchedOrderPositionFill]): Specification of how Positions in the Account
                are modified when the Order is filled.
            trigger_condition (Union[Unset, MarketIfTouchedOrderTriggerCondition]): Specification of which price component
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
            initial_market_price (Union[Unset, str]): The Market price at the time when the MarketIfTouched Order was
                created.
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
    state: Union[Unset, MarketIfTouchedOrderState] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    type: Union[Unset, MarketIfTouchedOrderType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    price_bound: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, MarketIfTouchedOrderTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    position_fill: Union[Unset, MarketIfTouchedOrderPositionFill] = UNSET
    trigger_condition: Union[Unset, MarketIfTouchedOrderTriggerCondition] = UNSET
    initial_market_price: Union[Unset, str] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
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
    def from_dict(cls, data: Dict[str, Any]) -> "MarketIfTouchedOrder":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
