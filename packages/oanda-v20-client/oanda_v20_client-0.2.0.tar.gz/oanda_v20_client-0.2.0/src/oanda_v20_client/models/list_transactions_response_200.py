from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_transactions_response_200_type_item import (
    check_list_transactions_response_200_type_item,
)
from ..models.list_transactions_response_200_type_item import (
    ListTransactionsResponse200TypeItem,
)
from typing import cast
from typing import Union


T = TypeVar("T", bound="ListTransactionsResponse200")


@_attrs_define
class ListTransactionsResponse200:
    """
    Attributes:
        from_ (Union[Unset, str]): The starting time provided in the request.
        to (Union[Unset, str]): The ending time provided in the request.
        page_size (Union[Unset, int]): The pageSize provided in the request
        type (Union[Unset, List[ListTransactionsResponse200TypeItem]]): The Transaction-type filter provided in the
            request
        count (Union[Unset, int]): The number of Transactions that are contained in the pages returned
        pages (Union[Unset, List[str]]): The list of URLs that represent idrange queries providing the data for each
            page in the query results
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    page_size: Union[Unset, int] = UNSET
    type: Union[Unset, List[ListTransactionsResponse200TypeItem]] = UNSET
    count: Union[Unset, int] = UNSET
    pages: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_

        to = self.to

        page_size = self.page_size

        type: Union[Unset, List[str]] = UNSET
        if not isinstance(self.type, Unset):
            type = []
            for type_item_data in self.type:
                type_item: str = type_item_data
                type.append(type_item)

        count = self.count

        pages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pages, Unset):
            pages = self.pages

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if type is not UNSET:
            field_dict["type"] = type
        if count is not UNSET:
            field_dict["count"] = count
        if pages is not UNSET:
            field_dict["pages"] = pages
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("from", UNSET)

        to = d.pop("to", UNSET)

        page_size = d.pop("pageSize", UNSET)

        type = []
        _type = d.pop("type", UNSET)
        for type_item_data in _type or []:
            type_item = check_list_transactions_response_200_type_item(type_item_data)

            type.append(type_item)

        count = d.pop("count", UNSET)

        pages = cast(List[str], d.pop("pages", UNSET))

        last_transaction_id = d.pop("lastTransactionID", UNSET)

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
