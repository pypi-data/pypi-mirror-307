from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.transaction import Transaction


T = TypeVar("T", bound="CreateOrderResponse404")


@_attrs_define
class CreateOrderResponse404:
    """
    Attributes:
        order_reject_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties
            that are common between all Transaction.
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request. Only present if the Account exists.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account. Only
            present if the Account exists.
        error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
            errors.
        error_message (Union[Unset, str]): The human-readable description of the error that has occurred.
    """

    order_reject_transaction: Union[Unset, "Transaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order_reject_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.order_reject_transaction, Unset):
            order_reject_transaction = self.order_reject_transaction.to_dict()

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        last_transaction_id = self.last_transaction_id

        error_code = self.error_code

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order_reject_transaction is not UNSET:
            field_dict["orderRejectTransaction"] = order_reject_transaction
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transaction import Transaction

        d = src_dict.copy()
        _order_reject_transaction = d.pop("orderRejectTransaction", UNSET)
        order_reject_transaction: Union[Unset, Transaction]
        if isinstance(_order_reject_transaction, Unset):
            order_reject_transaction = UNSET
        else:
            order_reject_transaction = Transaction.from_dict(_order_reject_transaction)

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        error_code = d.pop("errorCode", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        create_order_response_404 = cls(
            order_reject_transaction=order_reject_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )

        create_order_response_404.additional_properties = d
        return create_order_response_404

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
