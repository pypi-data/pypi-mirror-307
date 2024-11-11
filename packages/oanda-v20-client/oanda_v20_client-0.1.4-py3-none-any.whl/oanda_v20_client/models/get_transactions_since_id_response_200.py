from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.transaction import Transaction


T = TypeVar("T", bound="GetTransactionsSinceIdResponse200")


@_attrs_define
class GetTransactionsSinceIdResponse200:
    """
    Attributes:
        transactions (Union[Unset, List['Transaction']]): The list of Transactions that satisfy the request.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    transactions: Union[Unset, List["Transaction"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        transactions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transactions is not UNSET:
            field_dict["transactions"] = transactions
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transaction import Transaction

        d = src_dict.copy()
        transactions = []
        _transactions = d.pop("transactions", UNSET)
        for transactions_item_data in _transactions or []:
            transactions_item = Transaction.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_transactions_since_id_response_200 = cls(
            transactions=transactions,
            last_transaction_id=last_transaction_id,
        )

        get_transactions_since_id_response_200.additional_properties = d
        return get_transactions_since_id_response_200

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
