from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.limit_order_request_position_fill import (
    check_limit_order_request_position_fill,
)
from ..models.limit_order_request_position_fill import LimitOrderRequestPositionFill
from ..models.limit_order_request_time_in_force import (
    check_limit_order_request_time_in_force,
)
from ..models.limit_order_request_time_in_force import LimitOrderRequestTimeInForce
from ..models.limit_order_request_trigger_condition import (
    check_limit_order_request_trigger_condition,
)
from ..models.limit_order_request_trigger_condition import (
    LimitOrderRequestTriggerCondition,
)
from ..models.limit_order_request_type import check_limit_order_request_type
from ..models.limit_order_request_type import LimitOrderRequestType
from typing import Union

if TYPE_CHECKING:
    from ..models.stop_loss_details import StopLossDetails
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.take_profit_details import TakeProfitDetails
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="LimitOrderRequest")


@_attrs_define
class LimitOrderRequest:
    """A LimitOrderRequest specifies the parameters that may be set when creating a Limit Order.

    Attributes:
        type (Union[Unset, LimitOrderRequestType]): The type of the Order to Create. Must be set to "LIMIT" when
            creating a Market Order.
        instrument (Union[Unset, str]): The Limit Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Limit Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        price (Union[Unset, str]): The price threshold specified for the Limit Order. The Limit Order will only be
            filled by a market price that is equal to or better than this price.
        time_in_force (Union[Unset, LimitOrderRequestTimeInForce]): The time-in-force requested for the Limit Order.
        gtd_time (Union[Unset, str]): The date/time when the Limit Order will be cancelled if its timeInForce is "GTD".
        position_fill (Union[Unset, LimitOrderRequestPositionFill]): Specification of how Positions in the Account are
            modified when the Order is filled.
        trigger_condition (Union[Unset, LimitOrderRequestTriggerCondition]): Specification of which price component
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

    type: Union[Unset, LimitOrderRequestType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, LimitOrderRequestTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    position_fill: Union[Unset, LimitOrderRequestPositionFill] = UNSET
    trigger_condition: Union[Unset, LimitOrderRequestTriggerCondition] = UNSET
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

        price = self.price

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        gtd_time = self.gtd_time

        position_fill: Union[Unset, str] = UNSET
        if not isinstance(self.position_fill, Unset):
            position_fill = self.position_fill

        trigger_condition: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_condition, Unset):
            trigger_condition = self.trigger_condition

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
        if price is not UNSET:
            field_dict["price"] = price
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if gtd_time is not UNSET:
            field_dict["gtdTime"] = gtd_time
        if position_fill is not UNSET:
            field_dict["positionFill"] = position_fill
        if trigger_condition is not UNSET:
            field_dict["triggerCondition"] = trigger_condition
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
        type: Union[Unset, LimitOrderRequestType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_limit_order_request_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        price = d.pop("price", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, LimitOrderRequestTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_limit_order_request_time_in_force(_time_in_force)

        gtd_time = d.pop("gtdTime", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, LimitOrderRequestPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_limit_order_request_position_fill(_position_fill)

        _trigger_condition = d.pop("triggerCondition", UNSET)
        trigger_condition: Union[Unset, LimitOrderRequestTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = UNSET
        else:
            trigger_condition = check_limit_order_request_trigger_condition(
                _trigger_condition
            )

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
