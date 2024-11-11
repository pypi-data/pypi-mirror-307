from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="PricingHeartbeat")


@_attrs_define
class PricingHeartbeat:
    """A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.

    Attributes:
        type (Union[Unset, str]): The string "HEARTBEAT"
        time (Union[Unset, str]): The date/time when the Heartbeat was created.
    """

    type: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        time = d.pop("time", UNSET)

        pricing_heartbeat = cls(
            type=type,
            time=time,
        )

        pricing_heartbeat.additional_properties = d
        return pricing_heartbeat

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
