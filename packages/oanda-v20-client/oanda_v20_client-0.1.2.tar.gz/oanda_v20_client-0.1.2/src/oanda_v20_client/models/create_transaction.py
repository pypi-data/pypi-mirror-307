from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_transaction_type import check_create_transaction_type
from ..models.create_transaction_type import CreateTransactionType
from typing import Union


T = TypeVar("T", bound="CreateTransaction")


@_attrs_define
class CreateTransaction:
    """A CreateTransaction represents the creation of an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, CreateTransactionType]): The Type of the Transaction. Always set to "CREATE" in a
            CreateTransaction.
        division_id (Union[Unset, int]): The ID of the Division that the Account is in
        site_id (Union[Unset, int]): The ID of the Site that the Account was created at
        account_user_id (Union[Unset, int]): The ID of the user that the Account was created for
        account_number (Union[Unset, int]): The number of the Account within the site/division/user
        home_currency (Union[Unset, str]): The home currency of the Account
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, CreateTransactionType] = UNSET
    division_id: Union[Unset, int] = UNSET
    site_id: Union[Unset, int] = UNSET
    account_user_id: Union[Unset, int] = UNSET
    account_number: Union[Unset, int] = UNSET
    home_currency: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        time = self.time

        user_id = self.user_id

        account_id = self.account_id

        batch_id = self.batch_id

        request_id = self.request_id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        division_id = self.division_id

        site_id = self.site_id

        account_user_id = self.account_user_id

        account_number = self.account_number

        home_currency = self.home_currency

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if time is not UNSET:
            field_dict["time"] = time
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if account_id is not UNSET:
            field_dict["accountID"] = account_id
        if batch_id is not UNSET:
            field_dict["batchID"] = batch_id
        if request_id is not UNSET:
            field_dict["requestID"] = request_id
        if type is not UNSET:
            field_dict["type"] = type
        if division_id is not UNSET:
            field_dict["divisionID"] = division_id
        if site_id is not UNSET:
            field_dict["siteID"] = site_id
        if account_user_id is not UNSET:
            field_dict["accountUserID"] = account_user_id
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if home_currency is not UNSET:
            field_dict["homeCurrency"] = home_currency

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, CreateTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_create_transaction_type(_type)

        division_id = d.pop("divisionID", UNSET)

        site_id = d.pop("siteID", UNSET)

        account_user_id = d.pop("accountUserID", UNSET)

        account_number = d.pop("accountNumber", UNSET)

        home_currency = d.pop("homeCurrency", UNSET)

        create_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            division_id=division_id,
            site_id=site_id,
            account_user_id=account_user_id,
            account_number=account_number,
            home_currency=home_currency,
        )

        create_transaction.additional_properties = d
        return create_transaction

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
