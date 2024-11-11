from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.daily_financing_transaction_account_financing_mode import (
    check_daily_financing_transaction_account_financing_mode,
)
from ..models.daily_financing_transaction_account_financing_mode import (
    DailyFinancingTransactionAccountFinancingMode,
)
from ..models.daily_financing_transaction_type import (
    check_daily_financing_transaction_type,
)
from ..models.daily_financing_transaction_type import DailyFinancingTransactionType
from typing import Union

if TYPE_CHECKING:
    from ..models.position_financing import PositionFinancing


T = TypeVar("T", bound="DailyFinancingTransaction")


@_attrs_define
class DailyFinancingTransaction:
    """A DailyFinancingTransaction represents the daily payment/collection of financing for an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, DailyFinancingTransactionType]): The Type of the Transaction. Always set to "DAILY_FINANCING"
            for a DailyFinancingTransaction.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Account.
        account_balance (Union[Unset, str]): The Account's balance after daily financing.
        account_financing_mode (Union[Unset, DailyFinancingTransactionAccountFinancingMode]): The account financing mode
            at the time of the daily financing.
        position_financings (Union[Unset, List['PositionFinancing']]): The financing paid/collected for each Position in
            the Account.
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, DailyFinancingTransactionType] = UNSET
    financing: Union[Unset, str] = UNSET
    account_balance: Union[Unset, str] = UNSET
    account_financing_mode: Union[
        Unset, DailyFinancingTransactionAccountFinancingMode
    ] = UNSET
    position_financings: Union[Unset, List["PositionFinancing"]] = UNSET
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

        financing = self.financing

        account_balance = self.account_balance

        account_financing_mode: Union[Unset, str] = UNSET
        if not isinstance(self.account_financing_mode, Unset):
            account_financing_mode = self.account_financing_mode

        position_financings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.position_financings, Unset):
            position_financings = []
            for position_financings_item_data in self.position_financings:
                position_financings_item = position_financings_item_data.to_dict()
                position_financings.append(position_financings_item)

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
        if financing is not UNSET:
            field_dict["financing"] = financing
        if account_balance is not UNSET:
            field_dict["accountBalance"] = account_balance
        if account_financing_mode is not UNSET:
            field_dict["accountFinancingMode"] = account_financing_mode
        if position_financings is not UNSET:
            field_dict["positionFinancings"] = position_financings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position_financing import PositionFinancing

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, DailyFinancingTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_daily_financing_transaction_type(_type)

        financing = d.pop("financing", UNSET)

        account_balance = d.pop("accountBalance", UNSET)

        _account_financing_mode = d.pop("accountFinancingMode", UNSET)
        account_financing_mode: Union[
            Unset, DailyFinancingTransactionAccountFinancingMode
        ]
        if isinstance(_account_financing_mode, Unset):
            account_financing_mode = UNSET
        else:
            account_financing_mode = (
                check_daily_financing_transaction_account_financing_mode(
                    _account_financing_mode
                )
            )

        position_financings = []
        _position_financings = d.pop("positionFinancings", UNSET)
        for position_financings_item_data in _position_financings or []:
            position_financings_item = PositionFinancing.from_dict(
                position_financings_item_data
            )

            position_financings.append(position_financings_item)

        daily_financing_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            financing=financing,
            account_balance=account_balance,
            account_financing_mode=account_financing_mode,
            position_financings=position_financings,
        )

        daily_financing_transaction.additional_properties = d
        return daily_financing_transaction

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
