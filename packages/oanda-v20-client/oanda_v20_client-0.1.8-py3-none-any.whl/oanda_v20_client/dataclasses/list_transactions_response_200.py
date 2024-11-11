from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .list_transactions_response_200_type_item import (
    ListTransactionsResponse200TypeItem,
)
from .list_transactions_response_200_type_item import (
    check_list_transactions_response_200_type_item,
)
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="ListTransactionsResponse200")


@dataclasses.dataclass
class ListTransactionsResponse200:
    """Attributes:
    from_ (Union[Unset, str]): The starting time provided in the request.
    to (Union[Unset, str]): The ending time provided in the request.
    page_size (Union[Unset, int]): The pageSize provided in the request
    type (Union[Unset, List[ListTransactionsResponse200TypeItem]]): The Transaction-type filter provided in the
        request
    count (Union[Unset, int]): The number of Transactions that are contained in the pages returned
    pages (Union[Unset, List[str]]): The list of URLs that represent idrange queries providing the data for each
        page in the query results
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    from_: Optional[str]
    to: Optional[str]
    page_size: Optional[int]
    type: Optional[List[ListTransactionsResponse200TypeItem]]
    count: Optional[int]
    pages: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("from", None)
        to = d.pop("to", None)
        page_size = d.pop("pageSize", None)
        type = []
        _type = d.pop("type", None)
        for type_item_data in _type or []:
            type_item = check_list_transactions_response_200_type_item(type_item_data)
            type.append(type_item)
        count = d.pop("count", None)
        pages = cast(List[str], d.pop("pages", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        list_transactions_response_200 = cls(
            from_=from_,
            to=to,
            page_size=page_size,
            type=type,
            count=count,
            pages=pages,
            last_transaction_id=last_transaction_id,
        )
        list_transactions_response_200.additional_properties = d
        return list_transactions_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
