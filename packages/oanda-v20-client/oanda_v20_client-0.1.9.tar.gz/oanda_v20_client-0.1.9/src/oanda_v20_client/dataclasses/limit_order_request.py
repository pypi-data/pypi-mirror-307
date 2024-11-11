from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .limit_order_request_position_fill import LimitOrderRequestPositionFill
from .limit_order_request_position_fill import check_limit_order_request_position_fill
from .limit_order_request_time_in_force import LimitOrderRequestTimeInForce
from .limit_order_request_time_in_force import check_limit_order_request_time_in_force
from .limit_order_request_trigger_condition import LimitOrderRequestTriggerCondition
from .limit_order_request_trigger_condition import (
    check_limit_order_request_trigger_condition,
)
from .limit_order_request_type import LimitOrderRequestType
from .limit_order_request_type import check_limit_order_request_type
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="LimitOrderRequest")


@dataclasses.dataclass
class LimitOrderRequest:
    """A LimitOrderRequest specifies the parameters that may be set when creating a Limit Order.

    Attributes:
        type (Optional[LimitOrderRequestType]): The type of the Order to Create. Must be set to "LIMIT" when
            creating a Market Order.
        instrument (Optional[str]): The Limit Order's Instrument.
        units (Optional[str]): The quantity requested to be filled by the Limit Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        price (Optional[str]): The price threshold specified for the Limit Order. The Limit Order will only be
            filled by a market price that is equal to or better than this price.
        time_in_force (Optional[LimitOrderRequestTimeInForce]): The time-in-force requested for the Limit Order.
        gtd_time (Optional[str]): The date/time when the Limit Order will be cancelled if its timeInForce is "GTD".
        position_fill (Optional[LimitOrderRequestPositionFill]): Specification of how Positions in the Account are
            modified when the Order is filled.
        trigger_condition (Optional[LimitOrderRequestTriggerCondition]): Specification of which price component
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
        client_extensions (Optional[ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
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
            your account is associated with MT4."""

    type: Optional[LimitOrderRequestType]
    instrument: Optional[str]
    units: Optional[str]
    price: Optional[str]
    time_in_force: Optional[LimitOrderRequestTimeInForce]
    gtd_time: Optional[str]
    position_fill: Optional[LimitOrderRequestPositionFill]
    trigger_condition: Optional[LimitOrderRequestTriggerCondition]
    client_extensions: Optional["ClientExtensions"]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .take_profit_details import TakeProfitDetails
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .client_extensions import ClientExtensions
        from .stop_loss_details import StopLossDetails

        d = src_dict.copy()
        _type = d.pop("type", None)
        type: Optional[LimitOrderRequestType]
        if _type is None:
            type = None
        else:
            type = check_limit_order_request_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        price = d.pop("price", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[LimitOrderRequestTimeInForce]
        if _time_in_force is None:
            time_in_force = None
        else:
            time_in_force = check_limit_order_request_time_in_force(_time_in_force)
        gtd_time = d.pop("gtdTime", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[LimitOrderRequestPositionFill]
        if _position_fill is None:
            position_fill = None
        else:
            position_fill = check_limit_order_request_position_fill(_position_fill)
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[LimitOrderRequestTriggerCondition]
        if _trigger_condition is None:
            trigger_condition = None
        else:
            trigger_condition = check_limit_order_request_trigger_condition(
                _trigger_condition
            )
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if _client_extensions is None:
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
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
        limit_order_request = cls(
            type=type,
            instrument=instrument,
            units=units,
            price=price,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            position_fill=position_fill,
            trigger_condition=trigger_condition,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
        )
        limit_order_request.additional_properties = d
        return limit_order_request

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
