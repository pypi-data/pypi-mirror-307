from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.order_cancel_transaction import OrderCancelTransaction
    from ..models.order_fill_transaction import OrderFillTransaction
    from ..models.market_order_transaction import MarketOrderTransaction


T = TypeVar("T", bound="ClosePositionResponse200")


@_attrs_define
class ClosePositionResponse200:
    """
    Attributes:
        long_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
            creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
            current market price.
            Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
            closeout a Position or to particiate in in a Margin closeout.
        long_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the filling
            of an Order in the client's Account.
        long_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
            cancellation of an Order in the client's Account.
        short_order_create_transaction (Union[Unset, MarketOrderTransaction]): A MarketOrderTransaction represents the
            creation of a Market Order in the user's account. A Market Order is an Order that is filled immediately at the
            current market price.
            Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to
            closeout a Position or to particiate in in a Margin closeout.
        short_order_fill_transaction (Union[Unset, OrderFillTransaction]): An OrderFillTransaction represents the
            filling of an Order in the client's Account.
        short_order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
            cancellation of an Order in the client's Account.
        related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
            satisfying the request.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    long_order_create_transaction: Union[Unset, "MarketOrderTransaction"] = UNSET
    long_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    long_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    short_order_create_transaction: Union[Unset, "MarketOrderTransaction"] = UNSET
    short_order_fill_transaction: Union[Unset, "OrderFillTransaction"] = UNSET
    short_order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        long_order_create_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long_order_create_transaction, Unset):
            long_order_create_transaction = self.long_order_create_transaction.to_dict()

        long_order_fill_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long_order_fill_transaction, Unset):
            long_order_fill_transaction = self.long_order_fill_transaction.to_dict()

        long_order_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.long_order_cancel_transaction, Unset):
            long_order_cancel_transaction = self.long_order_cancel_transaction.to_dict()

        short_order_create_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short_order_create_transaction, Unset):
            short_order_create_transaction = (
                self.short_order_create_transaction.to_dict()
            )

        short_order_fill_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short_order_fill_transaction, Unset):
            short_order_fill_transaction = self.short_order_fill_transaction.to_dict()

        short_order_cancel_transaction: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.short_order_cancel_transaction, Unset):
            short_order_cancel_transaction = (
                self.short_order_cancel_transaction.to_dict()
            )

        related_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.related_transaction_i_ds, Unset):
            related_transaction_i_ds = self.related_transaction_i_ds

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if long_order_create_transaction is not UNSET:
            field_dict["longOrderCreateTransaction"] = long_order_create_transaction
        if long_order_fill_transaction is not UNSET:
            field_dict["longOrderFillTransaction"] = long_order_fill_transaction
        if long_order_cancel_transaction is not UNSET:
            field_dict["longOrderCancelTransaction"] = long_order_cancel_transaction
        if short_order_create_transaction is not UNSET:
            field_dict["shortOrderCreateTransaction"] = short_order_create_transaction
        if short_order_fill_transaction is not UNSET:
            field_dict["shortOrderFillTransaction"] = short_order_fill_transaction
        if short_order_cancel_transaction is not UNSET:
            field_dict["shortOrderCancelTransaction"] = short_order_cancel_transaction
        if related_transaction_i_ds is not UNSET:
            field_dict["relatedTransactionIDs"] = related_transaction_i_ds
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order_cancel_transaction import OrderCancelTransaction
        from ..models.order_fill_transaction import OrderFillTransaction
        from ..models.market_order_transaction import MarketOrderTransaction

        d = src_dict.copy()
        _long_order_create_transaction = d.pop("longOrderCreateTransaction", UNSET)
        long_order_create_transaction: Union[Unset, MarketOrderTransaction]
        if isinstance(_long_order_create_transaction, Unset):
            long_order_create_transaction = UNSET
        else:
            long_order_create_transaction = MarketOrderTransaction.from_dict(
                _long_order_create_transaction
            )

        _long_order_fill_transaction = d.pop("longOrderFillTransaction", UNSET)
        long_order_fill_transaction: Union[Unset, OrderFillTransaction]
        if isinstance(_long_order_fill_transaction, Unset):
            long_order_fill_transaction = UNSET
        else:
            long_order_fill_transaction = OrderFillTransaction.from_dict(
                _long_order_fill_transaction
            )

        _long_order_cancel_transaction = d.pop("longOrderCancelTransaction", UNSET)
        long_order_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_long_order_cancel_transaction, Unset):
            long_order_cancel_transaction = UNSET
        else:
            long_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _long_order_cancel_transaction
            )

        _short_order_create_transaction = d.pop("shortOrderCreateTransaction", UNSET)
        short_order_create_transaction: Union[Unset, MarketOrderTransaction]
        if isinstance(_short_order_create_transaction, Unset):
            short_order_create_transaction = UNSET
        else:
            short_order_create_transaction = MarketOrderTransaction.from_dict(
                _short_order_create_transaction
            )

        _short_order_fill_transaction = d.pop("shortOrderFillTransaction", UNSET)
        short_order_fill_transaction: Union[Unset, OrderFillTransaction]
        if isinstance(_short_order_fill_transaction, Unset):
            short_order_fill_transaction = UNSET
        else:
            short_order_fill_transaction = OrderFillTransaction.from_dict(
                _short_order_fill_transaction
            )

        _short_order_cancel_transaction = d.pop("shortOrderCancelTransaction", UNSET)
        short_order_cancel_transaction: Union[Unset, OrderCancelTransaction]
        if isinstance(_short_order_cancel_transaction, Unset):
            short_order_cancel_transaction = UNSET
        else:
            short_order_cancel_transaction = OrderCancelTransaction.from_dict(
                _short_order_cancel_transaction
            )

        related_transaction_i_ds = cast(
            List[str], d.pop("relatedTransactionIDs", UNSET)
        )

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        close_position_response_200 = cls(
            long_order_create_transaction=long_order_create_transaction,
            long_order_fill_transaction=long_order_fill_transaction,
            long_order_cancel_transaction=long_order_cancel_transaction,
            short_order_create_transaction=short_order_create_transaction,
            short_order_fill_transaction=short_order_fill_transaction,
            short_order_cancel_transaction=short_order_cancel_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )

        close_position_response_200.additional_properties = d
        return close_position_response_200

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
