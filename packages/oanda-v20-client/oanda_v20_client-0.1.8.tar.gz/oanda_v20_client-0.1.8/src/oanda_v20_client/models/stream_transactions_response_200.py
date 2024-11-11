from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.transaction import Transaction
    from ..models.transaction_heartbeat import TransactionHeartbeat


T = TypeVar("T", bound="StreamTransactionsResponse200")


@_attrs_define
class StreamTransactionsResponse200:
    """The response body for the Transaction Stream uses chunked transfer encoding.  Each chunk contains Transaction and/or
    TransactionHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and
    multiple objects found in the same chunk are separated by newlines.
    TransactionHeartbeats are sent every 5 seconds.

        Attributes:
            transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties that are
                common between all Transaction.
            heartbeat (Union[Unset, TransactionHeartbeat]): A TransactionHeartbeat object is injected into the Transaction
                stream to ensure that the HTTP connection remains active.
    """

    transaction: Union[Unset, "Transaction"] = UNSET
    heartbeat: Union[Unset, "TransactionHeartbeat"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transaction, Unset):
            transaction = self.transaction.to_dict()

        heartbeat: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.heartbeat, Unset):
            heartbeat = self.heartbeat.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transaction is not UNSET:
            field_dict["transaction"] = transaction
        if heartbeat is not UNSET:
            field_dict["heartbeat"] = heartbeat

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.transaction import Transaction
        from ..models.transaction_heartbeat import TransactionHeartbeat

        d = src_dict.copy()
        _transaction = d.pop("transaction", UNSET)
        transaction: Union[Unset, Transaction]
        if isinstance(_transaction, Unset):
            transaction = UNSET
        else:
            transaction = Transaction.from_dict(_transaction)

        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, TransactionHeartbeat]
        if isinstance(_heartbeat, Unset):
            heartbeat = UNSET
        else:
            heartbeat = TransactionHeartbeat.from_dict(_heartbeat)

        stream_transactions_response_200 = cls(
            transaction=transaction,
            heartbeat=heartbeat,
        )

        stream_transactions_response_200.additional_properties = d
        return stream_transactions_response_200

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
