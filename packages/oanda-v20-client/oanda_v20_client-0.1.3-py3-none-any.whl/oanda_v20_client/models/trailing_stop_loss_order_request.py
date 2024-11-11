from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trailing_stop_loss_order_request_time_in_force import (
    check_trailing_stop_loss_order_request_time_in_force,
)
from ..models.trailing_stop_loss_order_request_time_in_force import (
    TrailingStopLossOrderRequestTimeInForce,
)
from ..models.trailing_stop_loss_order_request_trigger_condition import (
    check_trailing_stop_loss_order_request_trigger_condition,
)
from ..models.trailing_stop_loss_order_request_trigger_condition import (
    TrailingStopLossOrderRequestTriggerCondition,
)
from ..models.trailing_stop_loss_order_request_type import (
    check_trailing_stop_loss_order_request_type,
)
from ..models.trailing_stop_loss_order_request_type import (
    TrailingStopLossOrderRequestType,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="TrailingStopLossOrderRequest")


@_attrs_define
class TrailingStopLossOrderRequest:
    """A TrailingStopLossOrderRequest specifies the parameters that may be set when creating a Trailing Stop Loss Order.

    Attributes:
        type (Union[Unset, TrailingStopLossOrderRequestType]): The type of the Order to Create. Must be set to
            "TRAILING_STOP_LOSS" when creating a Trailng Stop Loss Order.
        trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
        client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
            breached.
        distance (Union[Unset, str]): The price distance (in price units) specified for the TrailingStopLoss Order.
        time_in_force (Union[Unset, TrailingStopLossOrderRequestTimeInForce]): The time-in-force requested for the
            TrailingStopLoss Order. Restricted to "GTC", "GFD" and "GTD" for TrailingStopLoss Orders.
        gtd_time (Union[Unset, str]): The date/time when the StopLoss Order will be cancelled if its timeInForce is
            "GTD".
        trigger_condition (Union[Unset, TrailingStopLossOrderRequestTriggerCondition]): Specification of which price
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
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4.
    """

    type: Union[Unset, TrailingStopLossOrderRequestType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TrailingStopLossOrderRequestTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[Unset, TrailingStopLossOrderRequestTriggerCondition] = (
        UNSET
    )
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        trade_id = self.trade_id

        client_trade_id = self.client_trade_id

        distance = self.distance

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        gtd_time = self.gtd_time

        trigger_condition: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_condition, Unset):
            trigger_condition = self.trigger_condition

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if client_trade_id is not UNSET:
            field_dict["clientTradeID"] = client_trade_id
        if distance is not UNSET:
            field_dict["distance"] = distance
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if gtd_time is not UNSET:
            field_dict["gtdTime"] = gtd_time
        if trigger_condition is not UNSET:
            field_dict["triggerCondition"] = trigger_condition
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, TrailingStopLossOrderRequestType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_trailing_stop_loss_order_request_type(_type)

        trade_id = d.pop("tradeID", UNSET)

        client_trade_id = d.pop("clientTradeID", UNSET)

        distance = d.pop("distance", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, TrailingStopLossOrderRequestTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_trailing_stop_loss_order_request_time_in_force(
                _time_in_force
            )

        gtd_time = d.pop("gtdTime", UNSET)

        _trigger_condition = d.pop("triggerCondition", UNSET)
        trigger_condition: Union[Unset, TrailingStopLossOrderRequestTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = UNSET
        else:
            trigger_condition = (
                check_trailing_stop_loss_order_request_trigger_condition(
                    _trigger_condition
                )
            )

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        trailing_stop_loss_order_request = cls(
            type=type,
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            client_extensions=client_extensions,
        )

        trailing_stop_loss_order_request.additional_properties = d
        return trailing_stop_loss_order_request

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
