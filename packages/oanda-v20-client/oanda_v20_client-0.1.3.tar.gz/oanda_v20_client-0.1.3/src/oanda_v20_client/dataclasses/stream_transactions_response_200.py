from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transaction import Transaction
from .transaction_heartbeat import TransactionHeartbeat
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    transaction: Union[Unset, "Transaction"] = UNSET
    heartbeat: Union[Unset, "TransactionHeartbeat"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamTransactionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
