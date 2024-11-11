from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.market_order_request_position_fill import (
    check_market_order_request_position_fill,
)
from ..models.market_order_request_position_fill import MarketOrderRequestPositionFill
from ..models.market_order_request_time_in_force import (
    check_market_order_request_time_in_force,
)
from ..models.market_order_request_time_in_force import MarketOrderRequestTimeInForce
from ..models.market_order_request_type import check_market_order_request_type
from ..models.market_order_request_type import MarketOrderRequestType
from typing import Union

if TYPE_CHECKING:
    from ..models.stop_loss_details import StopLossDetails
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.take_profit_details import TakeProfitDetails
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="MarketOrderRequest")


@_attrs_define
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
            your account is associated with MT4.
    """

    type: Union[Unset, MarketOrderRequestType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, MarketOrderRequestTimeInForce] = UNSET
    price_bound: Union[Unset, str] = UNSET
    position_fill: Union[Unset, MarketOrderRequestPositionFill] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        instrument = self.instrument

        units = self.units

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        price_bound = self.price_bound

        position_fill: Union[Unset, str] = UNSET
        if not isinstance(self.position_fill, Unset):
            position_fill = self.position_fill

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        take_profit_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_on_fill, Unset):
            take_profit_on_fill = self.take_profit_on_fill.to_dict()

        stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_on_fill, Unset):
            stop_loss_on_fill = self.stop_loss_on_fill.to_dict()

        trailing_stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = self.trailing_stop_loss_on_fill.to_dict()

        trade_client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_client_extensions, Unset):
            trade_client_extensions = self.trade_client_extensions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if units is not UNSET:
            field_dict["units"] = units
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if price_bound is not UNSET:
            field_dict["priceBound"] = price_bound
        if position_fill is not UNSET:
            field_dict["positionFill"] = position_fill
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if take_profit_on_fill is not UNSET:
            field_dict["takeProfitOnFill"] = take_profit_on_fill
        if stop_loss_on_fill is not UNSET:
            field_dict["stopLossOnFill"] = stop_loss_on_fill
        if trailing_stop_loss_on_fill is not UNSET:
            field_dict["trailingStopLossOnFill"] = trailing_stop_loss_on_fill
        if trade_client_extensions is not UNSET:
            field_dict["tradeClientExtensions"] = trade_client_extensions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stop_loss_details import StopLossDetails
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.take_profit_details import TakeProfitDetails
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, MarketOrderRequestType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_market_order_request_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, MarketOrderRequestTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_market_order_request_time_in_force(_time_in_force)

        price_bound = d.pop("priceBound", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, MarketOrderRequestPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_market_order_request_position_fill(_position_fill)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        _take_profit_on_fill = d.pop("takeProfitOnFill", UNSET)
        take_profit_on_fill: Union[Unset, TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = UNSET
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)

        _stop_loss_on_fill = d.pop("stopLossOnFill", UNSET)
        stop_loss_on_fill: Union[Unset, StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = UNSET
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)

        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", UNSET)
        trailing_stop_loss_on_fill: Union[Unset, TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = UNSET
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )

        _trade_client_extensions = d.pop("tradeClientExtensions", UNSET)
        trade_client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = UNSET
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

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
