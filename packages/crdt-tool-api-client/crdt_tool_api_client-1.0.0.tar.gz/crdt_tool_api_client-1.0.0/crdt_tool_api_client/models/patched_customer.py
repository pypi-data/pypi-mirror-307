import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCustomer")


@_attrs_define
class PatchedCustomer:
    """Serializer for the Customer model.

    Attributes:
        id (Union[Unset, str]): Unique identifier for the customer.
        first_name (Union[Unset, str]): First name of the customer.
        middle_name (Union[Unset, str]): Middle name of the customer.
        last_name (Union[Unset, str]): Last name of the customer.
        primary_email (Union[Unset, str]): Primary email of the customer.
        alternative_email (Union[Unset, str]): Alternative email of the customer.
        primary_phone_number (Union[Unset, str]): Primary phone number of the customer.
        alternative_phone_number (Union[Unset, str]): Secondary phone number of the customer.
        client_identifier (Union[Unset, str]): An identifier that the client can use to reference the customer in their
            own domain.
        metadata (Union[Unset, Any]): Metadata about the customer.
        created_at (Union[Unset, datetime.datetime]): Date and time when the customer record was created.
        updated_at (Union[Unset, datetime.datetime]): Date and time when the customer record was last updated.
        deleted_at (Union[None, Unset, datetime.datetime]): Timestamp of when the customer was soft deleted.
        primary_address (Union[Unset, int]): Primary address of the customer.
        alternative_address (Union[None, Unset, int]): Alternative address of the customer.
        created_by (Union[Unset, int]): User who created the customer record.
        updated_by (Union[None, Unset, int]): User who updated the customer record.
        deleted_by (Union[None, Unset, int]): User who deleted the customer record.
    """

    id: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    middle_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    primary_email: Union[Unset, str] = UNSET
    alternative_email: Union[Unset, str] = UNSET
    primary_phone_number: Union[Unset, str] = UNSET
    alternative_phone_number: Union[Unset, str] = UNSET
    client_identifier: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    primary_address: Union[Unset, int] = UNSET
    alternative_address: Union[None, Unset, int] = UNSET
    created_by: Union[Unset, int] = UNSET
    updated_by: Union[None, Unset, int] = UNSET
    deleted_by: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        first_name = self.first_name

        middle_name = self.middle_name

        last_name = self.last_name

        primary_email = self.primary_email

        alternative_email = self.alternative_email

        primary_phone_number = self.primary_phone_number

        alternative_phone_number = self.alternative_phone_number

        client_identifier = self.client_identifier

        metadata = self.metadata

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        primary_address = self.primary_address

        alternative_address: Union[None, Unset, int]
        if isinstance(self.alternative_address, Unset):
            alternative_address = UNSET
        else:
            alternative_address = self.alternative_address

        created_by = self.created_by

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
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if primary_email is not UNSET:
            field_dict["primary_email"] = primary_email
        if alternative_email is not UNSET:
            field_dict["alternative_email"] = alternative_email
        if primary_phone_number is not UNSET:
            field_dict["primary_phone_number"] = primary_phone_number
        if alternative_phone_number is not UNSET:
            field_dict["alternative_phone_number"] = alternative_phone_number
        if client_identifier is not UNSET:
            field_dict["client_identifier"] = client_identifier
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if primary_address is not UNSET:
            field_dict["primary_address"] = primary_address
        if alternative_address is not UNSET:
            field_dict["alternative_address"] = alternative_address
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        first_name = (
            self.first_name
            if isinstance(self.first_name, Unset)
            else (None, str(self.first_name).encode(), "text/plain")
        )

        middle_name = (
            self.middle_name
            if isinstance(self.middle_name, Unset)
            else (None, str(self.middle_name).encode(), "text/plain")
        )

        last_name = (
            self.last_name if isinstance(self.last_name, Unset) else (None, str(self.last_name).encode(), "text/plain")
        )

        primary_email = (
            self.primary_email
            if isinstance(self.primary_email, Unset)
            else (None, str(self.primary_email).encode(), "text/plain")
        )

        alternative_email = (
            self.alternative_email
            if isinstance(self.alternative_email, Unset)
            else (None, str(self.alternative_email).encode(), "text/plain")
        )

        primary_phone_number = (
            self.primary_phone_number
            if isinstance(self.primary_phone_number, Unset)
            else (None, str(self.primary_phone_number).encode(), "text/plain")
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

        created_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat().encode()

        updated_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat().encode()

        deleted_at: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat().encode()
        else:
            deleted_at = (None, str(self.deleted_at).encode(), "text/plain")

        primary_address = (
            self.primary_address
            if isinstance(self.primary_address, Unset)
            else (None, str(self.primary_address).encode(), "text/plain")
        )

        alternative_address: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.alternative_address, Unset):
            alternative_address = UNSET
        elif isinstance(self.alternative_address, int):
            alternative_address = (None, str(self.alternative_address).encode(), "text/plain")
        else:
            alternative_address = (None, str(self.alternative_address).encode(), "text/plain")

        created_by = (
            self.created_by
            if isinstance(self.created_by, Unset)
            else (None, str(self.created_by).encode(), "text/plain")
        )

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

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if middle_name is not UNSET:
            field_dict["middle_name"] = middle_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if primary_email is not UNSET:
            field_dict["primary_email"] = primary_email
        if alternative_email is not UNSET:
            field_dict["alternative_email"] = alternative_email
        if primary_phone_number is not UNSET:
            field_dict["primary_phone_number"] = primary_phone_number
        if alternative_phone_number is not UNSET:
            field_dict["alternative_phone_number"] = alternative_phone_number
        if client_identifier is not UNSET:
            field_dict["client_identifier"] = client_identifier
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if primary_address is not UNSET:
            field_dict["primary_address"] = primary_address
        if alternative_address is not UNSET:
            field_dict["alternative_address"] = alternative_address
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        first_name = d.pop("first_name", UNSET)

        middle_name = d.pop("middle_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        primary_email = d.pop("primary_email", UNSET)

        alternative_email = d.pop("alternative_email", UNSET)

        primary_phone_number = d.pop("primary_phone_number", UNSET)

        alternative_phone_number = d.pop("alternative_phone_number", UNSET)

        client_identifier = d.pop("client_identifier", UNSET)

        metadata = d.pop("metadata", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

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

        primary_address = d.pop("primary_address", UNSET)

        def _parse_alternative_address(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        alternative_address = _parse_alternative_address(d.pop("alternative_address", UNSET))

        created_by = d.pop("created_by", UNSET)

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

        patched_customer = cls(
            id=id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            primary_email=primary_email,
            alternative_email=alternative_email,
            primary_phone_number=primary_phone_number,
            alternative_phone_number=alternative_phone_number,
            client_identifier=client_identifier,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            primary_address=primary_address,
            alternative_address=alternative_address,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
        )

        patched_customer.additional_properties = d
        return patched_customer

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
