from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .list_transactions_response_200_type_item import (
    ListTransactionsResponse200TypeItem,
)
from typing import List, Optional, TypeVar

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListTransactionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
