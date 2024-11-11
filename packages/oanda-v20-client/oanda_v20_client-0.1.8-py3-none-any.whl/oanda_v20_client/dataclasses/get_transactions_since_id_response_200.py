from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transaction import Transaction
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="GetTransactionsSinceIdResponse200")


@dataclasses.dataclass
class GetTransactionsSinceIdResponse200:
    """Attributes:
    transactions (Union[Unset, List['Transaction']]): The list of Transactions that satisfy the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    transactions: Optional[List["Transaction"]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .transaction import Transaction

        d = src_dict.copy()
        transactions = []
        _transactions = d.pop("transactions", None)
        for transactions_item_data in _transactions or []:
            transactions_item = Transaction.from_dict(transactions_item_data)
            transactions.append(transactions_item)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_transactions_since_id_response_200 = cls(
            transactions=transactions, last_transaction_id=last_transaction_id
        )
        get_transactions_since_id_response_200.additional_properties = d
        return get_transactions_since_id_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
