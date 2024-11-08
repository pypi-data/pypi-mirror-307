import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_period_enum import BillingPeriodEnum
from ..models.pricing_model_enum import PricingModelEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Plan")


@_attrs_define
class Plan:
    """Serializer for the Plan model.

    Attributes:
        id (str): Unique identifier for the plan.
        plan_name (str): Name of the plan.
        plan_code (str): Unique identifier for the plan.
        billing_period (BillingPeriodEnum): * `daily` - Daily
            * `weekly` - Weekly
            * `monthly` - Monthly
            * `yearly` - Yearly
        pricing_model (PricingModelEnum): * `fixed` - Fixed
            * `ramp` - Ramp
        created_at (datetime.datetime): Date and time when the plan record was created.
        updated_at (datetime.datetime): Date and time when the plan record was last updated.
        created_by (int): User who created the plan record.
        plan_description (Union[Unset, str]): Description of what the plan includes.
        subscription_term_length (Union[Unset, int]): Default length of time customers are committed to a subscription.
        billing_cycles (Union[Unset, int]): Number of billing cycles before the subscription ends. 0 for indefinite.
        dunning_campaign (Union[Unset, str]): Dunning campaign associated with the plan.
        metadata (Union[Unset, Any]): Metadata about the plan.
        deleted_at (Union[None, Unset, datetime.datetime]): Timestamp of when the plan was soft deleted.
        updated_by (Union[None, Unset, int]): User who updated the plan record.
        deleted_by (Union[None, Unset, int]): User who deleted the plan record.
    """

    id: str
    plan_name: str
    plan_code: str
    billing_period: BillingPeriodEnum
    pricing_model: PricingModelEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: int
    plan_description: Union[Unset, str] = UNSET
    subscription_term_length: Union[Unset, int] = UNSET
    billing_cycles: Union[Unset, int] = UNSET
    dunning_campaign: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_by: Union[None, Unset, int] = UNSET
    deleted_by: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        plan_name = self.plan_name

        plan_code = self.plan_code

        billing_period = self.billing_period.value

        pricing_model = self.pricing_model.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by

        plan_description = self.plan_description

        subscription_term_length = self.subscription_term_length

        billing_cycles = self.billing_cycles

        dunning_campaign = self.dunning_campaign

        metadata = self.metadata

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

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
                "plan_name": plan_name,
                "plan_code": plan_code,
                "billing_period": billing_period,
                "pricing_model": pricing_model,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by": created_by,
            }
        )
        if plan_description is not UNSET:
            field_dict["plan_description"] = plan_description
        if subscription_term_length is not UNSET:
            field_dict["subscription_term_length"] = subscription_term_length
        if billing_cycles is not UNSET:
            field_dict["billing_cycles"] = billing_cycles
        if dunning_campaign is not UNSET:
            field_dict["dunning_campaign"] = dunning_campaign
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        plan_name = (None, str(self.plan_name).encode(), "text/plain")

        plan_code = (None, str(self.plan_code).encode(), "text/plain")

        billing_period = (None, str(self.billing_period.value).encode(), "text/plain")

        pricing_model = (None, str(self.pricing_model.value).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

        created_by = (None, str(self.created_by).encode(), "text/plain")

        plan_description = (
            self.plan_description
            if isinstance(self.plan_description, Unset)
            else (None, str(self.plan_description).encode(), "text/plain")
        )

        subscription_term_length = (
            self.subscription_term_length
            if isinstance(self.subscription_term_length, Unset)
            else (None, str(self.subscription_term_length).encode(), "text/plain")
        )

        billing_cycles = (
            self.billing_cycles
            if isinstance(self.billing_cycles, Unset)
            else (None, str(self.billing_cycles).encode(), "text/plain")
        )

        dunning_campaign = (
            self.dunning_campaign
            if isinstance(self.dunning_campaign, Unset)
            else (None, str(self.dunning_campaign).encode(), "text/plain")
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
                "plan_name": plan_name,
                "plan_code": plan_code,
                "billing_period": billing_period,
                "pricing_model": pricing_model,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by": created_by,
            }
        )
        if plan_description is not UNSET:
            field_dict["plan_description"] = plan_description
        if subscription_term_length is not UNSET:
            field_dict["subscription_term_length"] = subscription_term_length
        if billing_cycles is not UNSET:
            field_dict["billing_cycles"] = billing_cycles
        if dunning_campaign is not UNSET:
            field_dict["dunning_campaign"] = dunning_campaign
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        plan_name = d.pop("plan_name")

        plan_code = d.pop("plan_code")

        billing_period = BillingPeriodEnum(d.pop("billing_period"))

        pricing_model = PricingModelEnum(d.pop("pricing_model"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        plan_description = d.pop("plan_description", UNSET)

        subscription_term_length = d.pop("subscription_term_length", UNSET)

        billing_cycles = d.pop("billing_cycles", UNSET)

        dunning_campaign = d.pop("dunning_campaign", UNSET)

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

        plan = cls(
            id=id,
            plan_name=plan_name,
            plan_code=plan_code,
            billing_period=billing_period,
            pricing_model=pricing_model,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            plan_description=plan_description,
            subscription_term_length=subscription_term_length,
            billing_cycles=billing_cycles,
            dunning_campaign=dunning_campaign,
            metadata=metadata,
            deleted_at=deleted_at,
            updated_by=updated_by,
            deleted_by=deleted_by,
        )

        plan.additional_properties = d
        return plan

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
