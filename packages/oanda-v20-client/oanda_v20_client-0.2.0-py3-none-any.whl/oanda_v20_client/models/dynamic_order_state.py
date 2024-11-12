from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="DynamicOrderState")


@_attrs_define
class DynamicOrderState:
    """The dynamic state of an Order. This is only relevant to TrailingStopLoss Orders, as no other Order type has dynamic
    state.

        Attributes:
            id (Union[Unset, str]): The Order's ID.
            trailing_stop_value (Union[Unset, str]): The Order's calculated trailing stop value.
            trigger_distance (Union[Unset, str]): The distance between the Trailing Stop Loss Order's trailingStopValue and
                the current Market Price. This represents the distance (in price units) of the Order from a triggering price. If
                the distance could not be determined, this value will not be set.
            is_trigger_distance_exact (Union[Unset, bool]): True if an exact trigger distance could be calculated. If false,
                it means the provided trigger distance is a best estimate. If the distance could not be determined, this value
                will not be set.
    """

    id: Union[Unset, str] = UNSET
    trailing_stop_value: Union[Unset, str] = UNSET
    trigger_distance: Union[Unset, str] = UNSET
    is_trigger_distance_exact: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        trailing_stop_value = self.trailing_stop_value

        trigger_distance = self.trigger_distance

        is_trigger_distance_exact = self.is_trigger_distance_exact

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if trailing_stop_value is not UNSET:
            field_dict["trailingStopValue"] = trailing_stop_value
        if trigger_distance is not UNSET:
            field_dict["triggerDistance"] = trigger_distance
        if is_trigger_distance_exact is not UNSET:
            field_dict["isTriggerDistanceExact"] = is_trigger_distance_exact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        trailing_stop_value = d.pop("trailingStopValue", UNSET)

        trigger_distance = d.pop("triggerDistance", UNSET)

        is_trigger_distance_exact = d.pop("isTriggerDistanceExact", UNSET)

        dynamic_order_state = cls(
            id=id,
            trailing_stop_value=trailing_stop_value,
            trigger_distance=trigger_distance,
            is_trigger_distance_exact=is_trigger_distance_exact,
        )

        dynamic_order_state.additional_properties = d
        return dynamic_order_state

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
