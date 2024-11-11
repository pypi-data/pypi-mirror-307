from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.order_client_extensions_modify_transaction import (
        OrderClientExtensionsModifyTransaction,
    )


T = TypeVar("T", bound="SetOrderClientExtensionsResponse200")


@_attrs_define
class SetOrderClientExtensionsResponse200:
    """
    Attributes:
        order_client_extensions_modify_transaction (Union[Unset, OrderClientExtensionsModifyTransaction]): A
            OrderClientExtensionsModifyTransaction represents the modification of an Order's Client Extensions.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request.
    """

    order_client_extensions_modify_transaction: Union[
        Unset, "OrderClientExtensionsModifyTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_client_extensions_modify_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_client_extensions_modify_transaction, Unset):
            order_client_extensions_modify_transaction = (
                self.order_client_extensions_modify_transaction.to_dict()
            )

        last_transaction_id = self.last_transaction_id

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_client_extensions_modify_transaction is not UNSET:
            field_dict["orderClientExtensionsModifyTransaction"] = (
                order_client_extensions_modify_transaction
            )
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order_client_extensions_modify_transaction import (
            OrderClientExtensionsModifyTransaction,
        )

        d = src_dict.copy()
        _order_client_extensions_modify_transaction = d.pop(
            "orderClientExtensionsModifyTransaction", UNSET
        )
        order_client_extensions_modify_transaction: Union[
            Unset, OrderClientExtensionsModifyTransaction
        ]
        if isinstance(_order_client_extensions_modify_transaction, Unset):
            order_client_extensions_modify_transaction = UNSET
        else:
            order_client_extensions_modify_transaction = (
                OrderClientExtensionsModifyTransaction.from_dict(
                    _order_client_extensions_modify_transaction
                )
            )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        set_order_client_extensions_response_200 = cls(
            order_client_extensions_modify_transaction=order_client_extensions_modify_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
        )

        set_order_client_extensions_response_200.additional_properties = d
        return set_order_client_extensions_response_200

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
