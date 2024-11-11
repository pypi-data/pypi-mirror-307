from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trailing_stop_loss_details_time_in_force import (
    check_trailing_stop_loss_details_time_in_force,
)
from ..models.trailing_stop_loss_details_time_in_force import (
    TrailingStopLossDetailsTimeInForce,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="TrailingStopLossDetails")


@_attrs_define
class TrailingStopLossDetails:
    """TrailingStopLossDetails specifies the details of a Trailing Stop Loss Order to be created on behalf of a client.
    This may happen when an Order is filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's
    dependent Trailing Stop Loss Order is modified directly through the Trade.

        Attributes:
            distance (Union[Unset, str]): The distance (in price units) from the Trade's fill price that the Trailing Stop
                Loss Order will be triggered at.
            time_in_force (Union[Unset, TrailingStopLossDetailsTimeInForce]): The time in force for the created Trailing
                Stop Loss Order. This may only be GTC, GTD or GFD.
            gtd_time (Union[Unset, str]): The date when the Trailing Stop Loss Order will be cancelled on if timeInForce is
                GTD.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
    """

    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TrailingStopLossDetailsTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        distance = self.distance

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        gtd_time = self.gtd_time

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if distance is not UNSET:
            field_dict["distance"] = distance
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if gtd_time is not UNSET:
            field_dict["gtdTime"] = gtd_time
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        distance = d.pop("distance", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, TrailingStopLossDetailsTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_trailing_stop_loss_details_time_in_force(
                _time_in_force
            )

        gtd_time = d.pop("gtdTime", UNSET)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        trailing_stop_loss_details = cls(
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            client_extensions=client_extensions,
        )

        trailing_stop_loss_details.additional_properties = d
        return trailing_stop_loss_details

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
