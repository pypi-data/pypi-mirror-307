from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .market_order_request_position_fill import MarketOrderRequestPositionFill
from .market_order_request_position_fill import check_market_order_request_position_fill
from .market_order_request_time_in_force import MarketOrderRequestTimeInForce
from .market_order_request_time_in_force import check_market_order_request_time_in_force
from .market_order_request_type import MarketOrderRequestType
from .market_order_request_type import check_market_order_request_type
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="MarketOrderRequest")


@dataclasses.dataclass
class MarketOrderRequest:
    """A MarketOrderRequest specifies the parameters that may be set when creating a Market Order.

    Attributes:
        type (Union[Unset, MarketOrderRequestType]): The type of the Order to Create. Must be set to "MARKET" when
            creating a Market Order.
        instrument (Union[Unset, str]): The Market Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Market Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        time_in_force (Union[Unset, MarketOrderRequestTimeInForce]): The time-in-force requested for the Market Order.
            Restricted to FOK or IOC for a MarketOrder.
        price_bound (Union[Unset, str]): The worst price that the client is willing to have the Market Order filled at.
        position_fill (Union[Unset, MarketOrderRequestPositionFill]): Specification of how Positions in the Account are
            modified when the Order is filled.
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
            your account is associated with MT4."""

    type: Optional[MarketOrderRequestType]
    instrument: Optional[str]
    units: Optional[str]
    time_in_force: Optional[MarketOrderRequestTimeInForce]
    price_bound: Optional[str]
    position_fill: Optional[MarketOrderRequestPositionFill]
    client_extensions: Optional["ClientExtensions"]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .stop_loss_details import StopLossDetails
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .take_profit_details import TakeProfitDetails
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        _type = d.pop("type", None)
        type: Optional[MarketOrderRequestType]
        if _type is None:
            type = None
        else:
            type = check_market_order_request_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[MarketOrderRequestTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_market_order_request_time_in_force(_time_in_force)
        price_bound = d.pop("priceBound", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[MarketOrderRequestPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = None
        else:
            position_fill = check_market_order_request_position_fill(_position_fill)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _take_profit_on_fill = d.pop("takeProfitOnFill", None)
        take_profit_on_fill: Optional[TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = None
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)
        _stop_loss_on_fill = d.pop("stopLossOnFill", None)
        stop_loss_on_fill: Optional[StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = None
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)
        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", None)
        trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = None
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )
        _trade_client_extensions = d.pop("tradeClientExtensions", None)
        trade_client_extensions: Optional[ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = None
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )
        market_order_request = cls(
            type=type,
            instrument=instrument,
            units=units,
            time_in_force=time_in_force,
            price_bound=price_bound,
            position_fill=position_fill,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
        )
        market_order_request.additional_properties = d
        return market_order_request

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
