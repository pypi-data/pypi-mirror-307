from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transaction import Transaction
from .transaction_heartbeat import TransactionHeartbeat
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="StreamTransactionsResponse200")


@dataclasses.dataclass
class StreamTransactionsResponse200:
    """The response body for the Transaction Stream uses chunked transfer encoding.  Each chunk contains Transaction and/or
    TransactionHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and
    multiple objects found in the same chunk are separated by newlines.
    TransactionHeartbeats are sent every 5 seconds.

        Attributes:
            transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties that are
                common between all Transaction.
            heartbeat (Union[Unset, TransactionHeartbeat]): A TransactionHeartbeat object is injected into the Transaction
                stream to ensure that the HTTP connection remains active."""

    transaction: Optional["Transaction"]
    heartbeat: Optional["TransactionHeartbeat"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .transaction import Transaction
        from .transaction_heartbeat import TransactionHeartbeat

        d = src_dict.copy()
        _transaction = d.pop("transaction", None)
        transaction: Optional[Transaction]
        if isinstance(_transaction, Unset):
            transaction = None
        else:
            transaction = Transaction.from_dict(_transaction)
        _heartbeat = d.pop("heartbeat", None)
        heartbeat: Optional[TransactionHeartbeat]
        if isinstance(_heartbeat, Unset):
            heartbeat = None
        else:
            heartbeat = TransactionHeartbeat.from_dict(_heartbeat)
        stream_transactions_response_200 = cls(
            transaction=transaction, heartbeat=heartbeat
        )
        stream_transactions_response_200.additional_properties = d
        return stream_transactions_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
