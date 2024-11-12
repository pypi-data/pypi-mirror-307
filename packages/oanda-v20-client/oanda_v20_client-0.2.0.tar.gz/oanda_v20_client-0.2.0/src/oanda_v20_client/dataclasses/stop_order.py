from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .stop_loss_details import StopLossDetails
from .stop_order_position_fill import StopOrderPositionFill
from .stop_order_position_fill import check_stop_order_position_fill
from .stop_order_state import StopOrderState
from .stop_order_state import check_stop_order_state
from .stop_order_time_in_force import StopOrderTimeInForce
from .stop_order_time_in_force import check_stop_order_time_in_force
from .stop_order_trigger_condition import StopOrderTriggerCondition
from .stop_order_trigger_condition import check_stop_order_trigger_condition
from .stop_order_type import StopOrderType
from .stop_order_type import check_stop_order_type
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="StopOrder")


@dataclasses.dataclass
class StopOrder:
    """A StopOrder is an order that is created with a price threshold, and will only be filled by a price that is equal to
    or worse than the threshold.

        Attributes:
            id (Optional[str]): The Order's identifier, unique within the Order's Account.
            create_time (Optional[str]): The time when the Order was created.
            state (Optional[StopOrderState]): The current state of the Order.
            client_extensions (Optional[ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            type (Optional[StopOrderType]): The type of the Order. Always set to "STOP" for Stop Orders.
            instrument (Optional[str]): The Stop Order's Instrument.
            units (Optional[str]): The quantity requested to be filled by the Stop Order. A posititive number of units
                results in a long Order, and a negative number of units results in a short Order.
            price (Optional[str]): The price threshold specified for the Stop Order. The Stop Order will only be filled
                by a market price that is equal to or worse than this price.
            price_bound (Optional[str]): The worst market price that may be used to fill this Stop Order. If the market
                gaps and crosses through both the price and the priceBound, the Stop Order will be cancelled instead of being
                filled.
            time_in_force (Optional[StopOrderTimeInForce]): The time-in-force requested for the Stop Order.
            gtd_time (Optional[str]): The date/time when the Stop Order will be cancelled if its timeInForce is "GTD".
            position_fill (Optional[StopOrderPositionFill]): Specification of how Positions in the Account are modified
                when the Order is filled.
            trigger_condition (Optional[StopOrderTriggerCondition]): Specification of which price component should be
                used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on
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
            take_profit_on_fill (Optional[TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit
                Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring
                a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
            stop_loss_on_fill (Optional[StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to
                be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop
                Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
            trailing_stop_loss_on_fill (Optional[TrailingStopLossDetails]): TrailingStopLossDetails specifies the
                details of a Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is
                filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order
                is modified directly through the Trade.
            trade_client_extensions (Optional[ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            filling_transaction_id (Optional[str]): ID of the Transaction that filled this Order (only provided when the
                Order's state is FILLED)
            filled_time (Optional[str]): Date/time when the Order was filled (only provided when the Order's state is
                FILLED)
            trade_opened_id (Optional[str]): Trade ID of Trade opened when the Order was filled (only provided when the
                Order's state is FILLED and a Trade was opened as a result of the fill)
            trade_reduced_id (Optional[str]): Trade ID of Trade reduced when the Order was filled (only provided when
                the Order's state is FILLED and a Trade was reduced as a result of the fill)
            trade_closed_i_ds (Optional[List[str]]): Trade IDs of Trades closed when the Order was filled (only provided
                when the Order's state is FILLED and one or more Trades were closed as a result of the fill)
            cancelling_transaction_id (Optional[str]): ID of the Transaction that cancelled the Order (only provided
                when the Order's state is CANCELLED)
            cancelled_time (Optional[str]): Date/time when the Order was cancelled (only provided when the state of the
                Order is CANCELLED)
            replaces_order_id (Optional[str]): The ID of the Order that was replaced by this Order (only provided if
                this Order was created as part of a cancel/replace).
            replaced_by_order_id (Optional[str]): The ID of the Order that replaced this Order (only provided if this
                Order was cancelled as part of a cancel/replace)."""

    id: Optional[str]
    create_time: Optional[str]
    state: Optional[StopOrderState]
    client_extensions: Optional["ClientExtensions"]
    type: Optional[StopOrderType]
    instrument: Optional[str]
    units: Optional[str]
    price: Optional[str]
    price_bound: Optional[str]
    time_in_force: Optional[StopOrderTimeInForce]
    gtd_time: Optional[str]
    position_fill: Optional[StopOrderPositionFill]
    trigger_condition: Optional[StopOrderTriggerCondition]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]
    filling_transaction_id: Optional[str]
    filled_time: Optional[str]
    trade_opened_id: Optional[str]
    trade_reduced_id: Optional[str]
    trade_closed_i_ds: Optional[List[str]]
    cancelling_transaction_id: Optional[str]
    cancelled_time: Optional[str]
    replaces_order_id: Optional[str]
    replaced_by_order_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions
        from .stop_loss_details import StopLossDetails
        from .take_profit_details import TakeProfitDetails
        from .trailing_stop_loss_details import TrailingStopLossDetails

        d = src_dict.copy()
        id = d.pop("id", None)
        create_time = d.pop("createTime", None)
        _state = d.pop("state", None)
        state: Optional[StopOrderState]
        if _state is None:
            state = None
        else:
            state = check_stop_order_state(_state)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if _client_extensions is None:
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _type = d.pop("type", None)
        type: Optional[StopOrderType]
        if _type is None:
            type = None
        else:
            type = check_stop_order_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        price = d.pop("price", None)
        price_bound = d.pop("priceBound", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[StopOrderTimeInForce]
        if _time_in_force is None:
            time_in_force = None
        else:
            time_in_force = check_stop_order_time_in_force(_time_in_force)
        gtd_time = d.pop("gtdTime", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[StopOrderPositionFill]
        if _position_fill is None:
            position_fill = None
        else:
            position_fill = check_stop_order_position_fill(_position_fill)
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[StopOrderTriggerCondition]
        if _trigger_condition is None:
            trigger_condition = None
        else:
            trigger_condition = check_stop_order_trigger_condition(_trigger_condition)
        _take_profit_on_fill = d.pop("takeProfitOnFill", None)
        take_profit_on_fill: Optional[TakeProfitDetails]
        if _take_profit_on_fill is None:
            take_profit_on_fill = None
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)
        _stop_loss_on_fill = d.pop("stopLossOnFill", None)
        stop_loss_on_fill: Optional[StopLossDetails]
        if _stop_loss_on_fill is None:
            stop_loss_on_fill = None
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)
        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", None)
        trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails]
        if _trailing_stop_loss_on_fill is None:
            trailing_stop_loss_on_fill = None
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )
        _trade_client_extensions = d.pop("tradeClientExtensions", None)
        trade_client_extensions: Optional[ClientExtensions]
        if _trade_client_extensions is None:
            trade_client_extensions = None
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )
        filling_transaction_id = d.pop("fillingTransactionID", None)
        filled_time = d.pop("filledTime", None)
        trade_opened_id = d.pop("tradeOpenedID", None)
        trade_reduced_id = d.pop("tradeReducedID", None)
        trade_closed_i_ds = cast(List[str], d.pop("tradeClosedIDs", None))
        cancelling_transaction_id = d.pop("cancellingTransactionID", None)
        cancelled_time = d.pop("cancelledTime", None)
        replaces_order_id = d.pop("replacesOrderID", None)
        replaced_by_order_id = d.pop("replacedByOrderID", None)
        stop_order = cls(
            id=id,
            create_time=create_time,
            state=state,
            client_extensions=client_extensions,
            type=type,
            instrument=instrument,
            units=units,
            price=price,
            price_bound=price_bound,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            position_fill=position_fill,
            trigger_condition=trigger_condition,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
            filling_transaction_id=filling_transaction_id,
            filled_time=filled_time,
            trade_opened_id=trade_opened_id,
            trade_reduced_id=trade_reduced_id,
            trade_closed_i_ds=trade_closed_i_ds,
            cancelling_transaction_id=cancelling_transaction_id,
            cancelled_time=cancelled_time,
            replaces_order_id=replaces_order_id,
            replaced_by_order_id=replaced_by_order_id,
        )
        return stop_order

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
