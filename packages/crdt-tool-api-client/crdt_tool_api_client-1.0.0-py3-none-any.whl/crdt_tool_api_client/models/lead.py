import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Lead")


@_attrs_define
class Lead:
    """Serializer for the Lead model.

    Attributes:
        id (int):
        name (str): The name of the lead.
        surname (str): The surname of the lead.
        email (str): The email address of the lead.
        email_confirmed (bool): Indicates whether the email address has been confirmed.
        phone (str): The phone number of the lead.
        date_created (datetime.datetime): The date and time when the lead was created.
        date_updated (datetime.datetime): The date and time when the lead was last updated.
        created_by (datetime.datetime): The date and time when the organisation was created.
        updated_by (datetime.datetime): The date and time when the organisation was last updated.
        tenant (int):
        source (int): The source from which the lead was acquired.
        phone_confirmed (Union[Unset, bool]): Indicates whether the phone number has been confirmed.
        import_record (Union[None, Unset, int]): The import record associated with the lead, if any.
        qualification_rule (Union[None, Unset, int]): The qualification rule applied to the lead, if any.
        stage (Union[None, Unset, int]): The current stage of the lead in the sales pipeline, if any.
    """

    id: int
    name: str
    surname: str
    email: str
    email_confirmed: bool
    phone: str
    date_created: datetime.datetime
    date_updated: datetime.datetime
    created_by: datetime.datetime
    updated_by: datetime.datetime
    tenant: int
    source: int
    phone_confirmed: Union[Unset, bool] = UNSET
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

        date_created = self.date_created.isoformat()

        date_updated = self.date_updated.isoformat()

        created_by = self.created_by.isoformat()

        updated_by = self.updated_by.isoformat()

        tenant = self.tenant

        source = self.source

        phone_confirmed = self.phone_confirmed

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
        field_dict.update(
            {
                "id": id,
                "name": name,
                "surname": surname,
                "email": email,
                "email_confirmed": email_confirmed,
                "phone": phone,
                "date_created": date_created,
                "date_updated": date_updated,
                "created_by": created_by,
                "updated_by": updated_by,
                "tenant": tenant,
                "source": source,
            }
        )
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
        if import_record is not UNSET:
            field_dict["import_record"] = import_record
        if qualification_rule is not UNSET:
            field_dict["qualification_rule"] = qualification_rule
        if stage is not UNSET:
            field_dict["stage"] = stage

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        name = (None, str(self.name).encode(), "text/plain")

        surname = (None, str(self.surname).encode(), "text/plain")

        email = (None, str(self.email).encode(), "text/plain")

        email_confirmed = (None, str(self.email_confirmed).encode(), "text/plain")

        phone = (None, str(self.phone).encode(), "text/plain")

        date_created = self.date_created.isoformat().encode()

        date_updated = self.date_updated.isoformat().encode()

        created_by = self.created_by.isoformat().encode()

        updated_by = self.updated_by.isoformat().encode()

        tenant = (None, str(self.tenant).encode(), "text/plain")

        source = (None, str(self.source).encode(), "text/plain")

        phone_confirmed = (
            self.phone_confirmed
            if isinstance(self.phone_confirmed, Unset)
            else (None, str(self.phone_confirmed).encode(), "text/plain")
        )

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

        field_dict.update(
            {
                "id": id,
                "name": name,
                "surname": surname,
                "email": email,
                "email_confirmed": email_confirmed,
                "phone": phone,
                "date_created": date_created,
                "date_updated": date_updated,
                "created_by": created_by,
                "updated_by": updated_by,
                "tenant": tenant,
                "source": source,
            }
        )
        if phone_confirmed is not UNSET:
            field_dict["phone_confirmed"] = phone_confirmed
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
        id = d.pop("id")

        name = d.pop("name")

        surname = d.pop("surname")

        email = d.pop("email")

        email_confirmed = d.pop("email_confirmed")

        phone = d.pop("phone")

        date_created = isoparse(d.pop("date_created"))

        date_updated = isoparse(d.pop("date_updated"))

        created_by = isoparse(d.pop("created_by"))

        updated_by = isoparse(d.pop("updated_by"))

        tenant = d.pop("tenant")

        source = d.pop("source")

        phone_confirmed = d.pop("phone_confirmed", UNSET)

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

        lead = cls(
            id=id,
            name=name,
            surname=surname,
            email=email,
            email_confirmed=email_confirmed,
            phone=phone,
            date_created=date_created,
            date_updated=date_updated,
            created_by=created_by,
            updated_by=updated_by,
            tenant=tenant,
            source=source,
            phone_confirmed=phone_confirmed,
            import_record=import_record,
            qualification_rule=qualification_rule,
            stage=stage,
        )

        lead.additional_properties = d
        return lead

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
