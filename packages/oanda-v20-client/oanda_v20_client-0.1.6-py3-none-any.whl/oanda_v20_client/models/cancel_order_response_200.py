from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.order_cancel_transaction import OrderCancelTransaction


T = TypeVar("T", bound="CancelOrderResponse200")


@_attrs_define
class CancelOrderResponse200:
    """
    Attributes:
        order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
            cancellation of an Order in the client's Account.
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_cancel_transaction, Unset):
            order_cancel_transaction = self.order_cancel_transaction.to_dict()

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_cancel_transaction is not UNSET:
            field_dict["orderCancelTransaction"] = order_cancel_transaction
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order_cancel_transaction import OrderCancelTransaction

        d = src_dict.copy()
        _order_cancel_transaction = d.pop("orderCancelTransaction", UNSET)
        order_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_order_cancel_transaction, Unset):
            order_cancel_transaction = UNSET
        else:
            order_cancel_transaction = OrderCancelTransaction.from_dict(
                _order_cancel_transaction
            )

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        cancel_order_response_200 = cls(
            order_cancel_transaction=order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )

        cancel_order_response_200.additional_properties = d
        return cancel_order_response_200

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
