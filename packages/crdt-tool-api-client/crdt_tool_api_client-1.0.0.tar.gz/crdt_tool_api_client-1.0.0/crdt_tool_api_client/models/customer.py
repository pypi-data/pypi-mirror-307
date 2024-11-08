import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Customer")


@_attrs_define
class Customer:
    """Serializer for the Customer model.

    Attributes:
        id (str): Unique identifier for the customer.
        first_name (str): First name of the customer.
        last_name (str): Last name of the customer.
        primary_email (str): Primary email of the customer.
        primary_phone_number (str): Primary phone number of the customer.
        created_at (datetime.datetime): Date and time when the customer record was created.
        updated_at (datetime.datetime): Date and time when the customer record was last updated.
        primary_address (int): Primary address of the customer.
        created_by (int): User who created the customer record.
        middle_name (Union[Unset, str]): Middle name of the customer.
        alternative_email (Union[Unset, str]): Alternative email of the customer.
        alternative_phone_number (Union[Unset, str]): Secondary phone number of the customer.
        client_identifier (Union[Unset, str]): An identifier that the client can use to reference the customer in their
            own domain.
        metadata (Union[Unset, Any]): Metadata about the customer.
        deleted_at (Union[None, Unset, datetime.datetime]): Timestamp of when the customer was soft deleted.
        alternative_address (Union[None, Unset, int]): Alternative address of the customer.
        updated_by (Union[None, Unset, int]): User who updated the customer record.
        deleted_by (Union[None, Unset, int]): User who deleted the customer record.
    """

    id: str
    first_name: str
    last_name: str
    primary_email: str
    primary_phone_number: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    primary_address: int
    created_by: int
    middle_name: Union[Unset, str] = UNSET
    alternative_email: Union[Unset, str] = UNSET
    alternative_phone_number: Union[Unset, str] = UNSET
    client_identifier: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    alternative_address: Union[None, Unset, int] = UNSET
    updated_by: Union[None, Unset, int] = UNSET
    deleted_by: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        first_name = self.first_name

        last_name = self.last_name

        primary_email = self.primary_email

        primary_phone_number = self.primary_phone_number

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        primary_address = self.primary_address

        created_by = self.created_by

        middle_name = self.middle_name

        alternative_email = self.alternative_email

        alternative_phone_number = self.alternative_phone_number

        client_identifier = self.client_identifier

        metadata = self.metadata

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        alternative_address: Union[None, Unset, int]
        if isinstance(self.alternative_address, Unset):
            alternative_address = UNSET
        else:
            alternative_address = self.alternative_address

        updated_by: Union[None, Unset, int]
        if isinstance(self.updated_by, Unset):
            updated_by = UNSET
        else:
            updated_by = self.updated_by

        deleted_by: Union[None, Unset, int]
        if isinstance(self.deleted_by, Unset):
            deleted_by = UNSET
        else:
            deleted_by = self.deleted_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "primary_email": primary_email,
                "primary_phone_number": primary_phone_number,
                "created_at": created_at,
                "updated_at": updated_at,
                "primary_address": primary_address,
                "created_by": created_by,
            }
        )
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if alternative_email is not UNSET:
            field_dict["alternative_email"] = alternative_email
        if alternative_phone_number is not UNSET:
            field_dict["alternative_phone_number"] = alternative_phone_number
        if client_identifier is not UNSET:
            field_dict["client_identifier"] = client_identifier
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if alternative_address is not UNSET:
            field_dict["alternative_address"] = alternative_address
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        first_name = (None, str(self.first_name).encode(), "text/plain")

        last_name = (None, str(self.last_name).encode(), "text/plain")

        primary_email = (None, str(self.primary_email).encode(), "text/plain")

        primary_phone_number = (None, str(self.primary_phone_number).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

        primary_address = (None, str(self.primary_address).encode(), "text/plain")

        created_by = (None, str(self.created_by).encode(), "text/plain")

        middle_name = (
            self.middle_name
            if isinstance(self.middle_name, Unset)
            else (None, str(self.middle_name).encode(), "text/plain")
        )

        alternative_email = (
            self.alternative_email
            if isinstance(self.alternative_email, Unset)
            else (None, str(self.alternative_email).encode(), "text/plain")
        )

        alternative_phone_number = (
            self.alternative_phone_number
            if isinstance(self.alternative_phone_number, Unset)
            else (None, str(self.alternative_phone_number).encode(), "text/plain")
        )

        client_identifier = (
            self.client_identifier
            if isinstance(self.client_identifier, Unset)
            else (None, str(self.client_identifier).encode(), "text/plain")
        )

        metadata = (
            self.metadata if isinstance(self.metadata, Unset) else (None, str(self.metadata).encode(), "text/plain")
        )

        deleted_at: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat().encode()
        else:
            deleted_at = (None, str(self.deleted_at).encode(), "text/plain")

        alternative_address: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.alternative_address, Unset):
            alternative_address = UNSET
        elif isinstance(self.alternative_address, int):
            alternative_address = (None, str(self.alternative_address).encode(), "text/plain")
        else:
            alternative_address = (None, str(self.alternative_address).encode(), "text/plain")

        updated_by: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.updated_by, Unset):
            updated_by = UNSET
        elif isinstance(self.updated_by, int):
            updated_by = (None, str(self.updated_by).encode(), "text/plain")
        else:
            updated_by = (None, str(self.updated_by).encode(), "text/plain")

        deleted_by: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.deleted_by, Unset):
            deleted_by = UNSET
        elif isinstance(self.deleted_by, int):
            deleted_by = (None, str(self.deleted_by).encode(), "text/plain")
        else:
            deleted_by = (None, str(self.deleted_by).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "primary_email": primary_email,
                "primary_phone_number": primary_phone_number,
                "created_at": created_at,
                "updated_at": updated_at,
                "primary_address": primary_address,
                "created_by": created_by,
            }
        )
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if alternative_email is not UNSET:
            field_dict["alternative_email"] = alternative_email
        if alternative_phone_number is not UNSET:
            field_dict["alternative_phone_number"] = alternative_phone_number
        if client_identifier is not UNSET:
            field_dict["client_identifier"] = client_identifier
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if alternative_address is not UNSET:
            field_dict["alternative_address"] = alternative_address
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        primary_email = d.pop("primary_email")

        primary_phone_number = d.pop("primary_phone_number")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        primary_address = d.pop("primary_address")

        created_by = d.pop("created_by")

        middle_name = d.pop("middle_name", UNSET)

        alternative_email = d.pop("alternative_email", UNSET)

        alternative_phone_number = d.pop("alternative_phone_number", UNSET)

        client_identifier = d.pop("client_identifier", UNSET)

        metadata = d.pop("metadata", UNSET)

        def _parse_deleted_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_alternative_address(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        alternative_address = _parse_alternative_address(d.pop("alternative_address", UNSET))

        def _parse_updated_by(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        updated_by = _parse_updated_by(d.pop("updated_by", UNSET))

        def _parse_deleted_by(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        deleted_by = _parse_deleted_by(d.pop("deleted_by", UNSET))

        customer = cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            primary_email=primary_email,
            primary_phone_number=primary_phone_number,
            created_at=created_at,
            updated_at=updated_at,
            primary_address=primary_address,
            created_by=created_by,
            middle_name=middle_name,
            alternative_email=alternative_email,
            alternative_phone_number=alternative_phone_number,
            client_identifier=client_identifier,
            metadata=metadata,
            deleted_at=deleted_at,
            alternative_address=alternative_address,
            updated_by=updated_by,
            deleted_by=deleted_by,
        )

        customer.additional_properties = d
        return customer

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
