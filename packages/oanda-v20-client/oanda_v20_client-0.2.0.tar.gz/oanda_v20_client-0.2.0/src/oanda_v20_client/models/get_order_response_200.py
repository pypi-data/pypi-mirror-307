from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.order import Order


T = TypeVar("T", bound="GetOrderResponse200")


@_attrs_define
class GetOrderResponse200:
    """
    Attributes:
        order (Union[Unset, Order]): The base Order definition specifies the properties that are common to all Orders.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    order: Union[Unset, "Order"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.to_dict()

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order import Order

        d = src_dict.copy()
        _order = d.pop("order", UNSET)
        order: Union[Unset, Order]
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = Order.from_dict(_order)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_order_response_200 = cls(
            order=order,
            last_transaction_id=last_transaction_id,
        )

        get_order_response_200.additional_properties = d
        return get_order_response_200

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
