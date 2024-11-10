from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="OrderIdentifier")


@_attrs_define
class OrderIdentifier:
    """An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.

    Attributes:
        order_id (Union[Unset, str]): The OANDA-assigned Order ID
        client_order_id (Union[Unset, str]): The client-provided client Order ID
    """

    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_id = self.order_id

        client_order_id = self.client_order_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_id is not UNSET:
            field_dict["orderID"] = order_id
        if client_order_id is not UNSET:
            field_dict["clientOrderID"] = client_order_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        order_id = d.pop("orderID", UNSET)

        client_order_id = d.pop("clientOrderID", UNSET)

        order_identifier = cls(
            order_id=order_id,
            client_order_id=client_order_id,
        )

        order_identifier.additional_properties = d
        return order_identifier

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
