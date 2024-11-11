from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .instrument import Instrument
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="GetAccountInstrumentsResponse200")


@dataclasses.dataclass
class GetAccountInstrumentsResponse200:
    """Attributes:
    instruments (Union[Unset, List['Instrument']]): The requested list of instruments.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account."""

    instruments: Optional[List["Instrument"]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .instrument import Instrument

        d = src_dict.copy()
        instruments = []
        _instruments = d.pop("instruments", None)
        for instruments_item_data in _instruments or []:
            instruments_item = Instrument.from_dict(instruments_item_data)
            instruments.append(instruments_item)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_account_instruments_response_200 = cls(
            instruments=instruments, last_transaction_id=last_transaction_id
        )
        get_account_instruments_response_200.additional_properties = d
        return get_account_instruments_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
