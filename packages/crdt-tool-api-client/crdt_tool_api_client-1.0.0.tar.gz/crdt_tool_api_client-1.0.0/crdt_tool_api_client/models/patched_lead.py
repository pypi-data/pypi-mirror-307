import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedLead")


@_attrs_define
class PatchedLead:
    """Serializer for the Lead model.

    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]): The name of the lead.
        surname (Union[Unset, str]): The surname of the lead.
        email (Union[Unset, str]): The email address of the lead.
        email_confirmed (Union[Unset, bool]): Indicates whether the email address has been confirmed.
        phone (Union[Unset, str]): The phone number of the lead.
        phone_confirmed (Union[Unset, bool]): Indicates whether the phone number has been confirmed.
        date_created (Union[Unset, datetime.datetime]): The date and time when the lead was created.
        date_updated (Union[Unset, datetime.datetime]): The date and time when the lead was last updated.
        created_by (Union[Unset, datetime.datetime]): The date and time when the organisation was created.
        updated_by (Union[Unset, datetime.datetime]): The date and time when the organisation was last updated.
        tenant (Union[Unset, int]):
        source (Union[Unset, int]): The source from which the lead was acquired.
        import_record (Union[None, Unset, int]): The import record associated with the lead, if any.
        qualification_rule (Union[None, Unset, int]): The qualification rule applied to the lead, if any.
        stage (Union[None, Unset, int]): The current stage of the lead in the sales pipeline, if any.
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    surname: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    email_confirmed: Union[Unset, bool] = UNSET
    phone: Union[Unset, str] = UNSET
    phone_confirmed: Union[Unset, bool] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    date_updated: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, datetime.datetime] = UNSET
    updated_by: Union[Unset, datetime.datetime] = UNSET
    tenant: Union[Unset, int] = UNSET
    source: Union[Unset, int] = UNSET
    import_record: Union[None, Unset, int] = UNSET
    qualification_rule: Union[None, Unset, int] = UNSET
    stage: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        surname = self.surname

        email = self.email

        email_confirmed = self.email_confirmed

        phone = self.phone

        phone_confirmed = self.phone_confirmed

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        date_updated: Union[Unset, str] = UNSET
        if not isinstance(self.date_updated, Unset):
            date_updated = self.date_updated.isoformat()

        created_by: Union[Unset, str] = UNSET
        if not isinstance(self.created_by, Unset):
            created_by = self.created_by.isoformat()

        updated_by: Union[Unset, str] = UNSET
        if not isinstance(self.updated_by, Unset):
            updated_by = self.updated_by.isoformat()

        tenant = self.tenant

        source = self.source

        import_record: Union[None, Unset, int]
        if isinstance(self.import_record, Unset):
            import_record = UNSET
        else:
            import_record = self.import_record

        qualification_rule: Union[None, Unset, int]
        if isinstance(self.qualification_rule, Unset):
            qualification_rule = UNSET
        else:
            qualification_rule = self.qualification_rule

        stage: Union[None, Unset, int]
        if isinstance(self.stage, Unset):
            stage = UNSET
        else:
            stage = self.stage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if surname is not UNSET:
            field_dict["surname"] = surname
        if email is not UNSET:
            field_dict["email"] = email
        if email_confirmed is not UNSET:
            field_dict["email_confirmed"] = email_confirmed
        if phone is not UNSET:
            field_dict["phone"] = phone
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if date_updated is not UNSET:
            field_dict["date_updated"] = date_updated
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if source is not UNSET:
            field_dict["source"] = source
        if import_record is not UNSET:
            field_dict["import_record"] = import_record
        if qualification_rule is not UNSET:
            field_dict["qualification_rule"] = qualification_rule
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        surname = self.surname if isinstance(self.surname, Unset) else (None, str(self.surname).encode(), "text/plain")

        email = self.email if isinstance(self.email, Unset) else (None, str(self.email).encode(), "text/plain")

        email_confirmed = (
            self.email_confirmed
            if isinstance(self.email_confirmed, Unset)
            else (None, str(self.email_confirmed).encode(), "text/plain")
        )

        phone = self.phone if isinstance(self.phone, Unset) else (None, str(self.phone).encode(), "text/plain")

        phone_confirmed = (
            self.phone_confirmed
            if isinstance(self.phone_confirmed, Unset)
            else (None, str(self.phone_confirmed).encode(), "text/plain")
        )

        date_created: Union[Unset, bytes] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat().encode()

        date_updated: Union[Unset, bytes] = UNSET
        if not isinstance(self.date_updated, Unset):
            date_updated = self.date_updated.isoformat().encode()

        created_by: Union[Unset, bytes] = UNSET
        if not isinstance(self.created_by, Unset):
            created_by = self.created_by.isoformat().encode()

        updated_by: Union[Unset, bytes] = UNSET
        if not isinstance(self.updated_by, Unset):
            updated_by = self.updated_by.isoformat().encode()

        tenant = self.tenant if isinstance(self.tenant, Unset) else (None, str(self.tenant).encode(), "text/plain")

        source = self.source if isinstance(self.source, Unset) else (None, str(self.source).encode(), "text/plain")

        import_record: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.import_record, Unset):
            import_record = UNSET
        elif isinstance(self.import_record, int):
            import_record = (None, str(self.import_record).encode(), "text/plain")
        else:
            import_record = (None, str(self.import_record).encode(), "text/plain")

        qualification_rule: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.qualification_rule, Unset):
            qualification_rule = UNSET
        elif isinstance(self.qualification_rule, int):
            qualification_rule = (None, str(self.qualification_rule).encode(), "text/plain")
        else:
            qualification_rule = (None, str(self.qualification_rule).encode(), "text/plain")

        stage: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.stage, Unset):
            stage = UNSET
        elif isinstance(self.stage, int):
            stage = (None, str(self.stage).encode(), "text/plain")
        else:
            stage = (None, str(self.stage).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if surname is not UNSET:
            field_dict["surname"] = surname
        if email is not UNSET:
            field_dict["email"] = email
        if email_confirmed is not UNSET:
            field_dict["email_confirmed"] = email_confirmed
        if phone is not UNSET:
            field_dict["phone"] = phone
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if date_updated is not UNSET:
            field_dict["date_updated"] = date_updated
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if source is not UNSET:
            field_dict["source"] = source
        if import_record is not UNSET:
            field_dict["import_record"] = import_record
        if qualification_rule is not UNSET:
            field_dict["qualification_rule"] = qualification_rule
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        surname = d.pop("surname", UNSET)

        email = d.pop("email", UNSET)

        email_confirmed = d.pop("email_confirmed", UNSET)

        phone = d.pop("phone", UNSET)

        phone_confirmed = d.pop("phone_confirmed", UNSET)

        _date_created = d.pop("date_created", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _date_updated = d.pop("date_updated", UNSET)
        date_updated: Union[Unset, datetime.datetime]
        if isinstance(_date_updated, Unset):
            date_updated = UNSET
        else:
            date_updated = isoparse(_date_updated)

        _created_by = d.pop("created_by", UNSET)
        created_by: Union[Unset, datetime.datetime]
        if isinstance(_created_by, Unset):
            created_by = UNSET
        else:
            created_by = isoparse(_created_by)

        _updated_by = d.pop("updated_by", UNSET)
        updated_by: Union[Unset, datetime.datetime]
        if isinstance(_updated_by, Unset):
            updated_by = UNSET
        else:
            updated_by = isoparse(_updated_by)

        tenant = d.pop("tenant", UNSET)

        source = d.pop("source", UNSET)

        def _parse_import_record(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        import_record = _parse_import_record(d.pop("import_record", UNSET))

        def _parse_qualification_rule(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        qualification_rule = _parse_qualification_rule(d.pop("qualification_rule", UNSET))

        def _parse_stage(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stage = _parse_stage(d.pop("stage", UNSET))

        patched_lead = cls(
            id=id,
            name=name,
            surname=surname,
            email=email,
            email_confirmed=email_confirmed,
            phone=phone,
            phone_confirmed=phone_confirmed,
            date_created=date_created,
            date_updated=date_updated,
            created_by=created_by,
            updated_by=updated_by,
            tenant=tenant,
            source=source,
            import_record=import_record,
            qualification_rule=qualification_rule,
            stage=stage,
        )

        patched_lead.additional_properties = d
        return patched_lead

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
