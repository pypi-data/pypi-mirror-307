import datetime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_period_enum import BillingPeriodEnum
from ..models.pricing_model_enum import PricingModelEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedPlan")


@_attrs_define
class PatchedPlan:
    """Serializer for the Plan model.

    Attributes:
        id (Union[Unset, str]): Unique identifier for the plan.
        plan_name (Union[Unset, str]): Name of the plan.
        plan_code (Union[Unset, str]): Unique identifier for the plan.
        plan_description (Union[Unset, str]): Description of what the plan includes.
        billing_period (Union[Unset, BillingPeriodEnum]): * `daily` - Daily
            * `weekly` - Weekly
            * `monthly` - Monthly
            * `yearly` - Yearly
        subscription_term_length (Union[Unset, int]): Default length of time customers are committed to a subscription.
        billing_cycles (Union[Unset, int]): Number of billing cycles before the subscription ends. 0 for indefinite.
        pricing_model (Union[Unset, PricingModelEnum]): * `fixed` - Fixed
            * `ramp` - Ramp
        dunning_campaign (Union[Unset, str]): Dunning campaign associated with the plan.
        metadata (Union[Unset, Any]): Metadata about the plan.
        created_at (Union[Unset, datetime.datetime]): Date and time when the plan record was created.
        updated_at (Union[Unset, datetime.datetime]): Date and time when the plan record was last updated.
        deleted_at (Union[None, Unset, datetime.datetime]): Timestamp of when the plan was soft deleted.
        created_by (Union[Unset, int]): User who created the plan record.
        updated_by (Union[None, Unset, int]): User who updated the plan record.
        deleted_by (Union[None, Unset, int]): User who deleted the plan record.
    """

    id: Union[Unset, str] = UNSET
    plan_name: Union[Unset, str] = UNSET
    plan_code: Union[Unset, str] = UNSET
    plan_description: Union[Unset, str] = UNSET
    billing_period: Union[Unset, BillingPeriodEnum] = UNSET
    subscription_term_length: Union[Unset, int] = UNSET
    billing_cycles: Union[Unset, int] = UNSET
    pricing_model: Union[Unset, PricingModelEnum] = UNSET
    dunning_campaign: Union[Unset, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, int] = UNSET
    updated_by: Union[None, Unset, int] = UNSET
    deleted_by: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        plan_name = self.plan_name

        plan_code = self.plan_code

        plan_description = self.plan_description

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.value

        subscription_term_length = self.subscription_term_length

        billing_cycles = self.billing_cycles

        pricing_model: Union[Unset, str] = UNSET
        if not isinstance(self.pricing_model, Unset):
            pricing_model = self.pricing_model.value

        dunning_campaign = self.dunning_campaign

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
        if plan_name is not UNSET:
            field_dict["plan_name"] = plan_name
        if plan_code is not UNSET:
            field_dict["plan_code"] = plan_code
        if plan_description is not UNSET:
            field_dict["plan_description"] = plan_description
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period
        if subscription_term_length is not UNSET:
            field_dict["subscription_term_length"] = subscription_term_length
        if billing_cycles is not UNSET:
            field_dict["billing_cycles"] = billing_cycles
        if pricing_model is not UNSET:
            field_dict["pricing_model"] = pricing_model
        if dunning_campaign is not UNSET:
            field_dict["dunning_campaign"] = dunning_campaign
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if deleted_by is not UNSET:
            field_dict["deleted_by"] = deleted_by

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        plan_name = (
            self.plan_name if isinstance(self.plan_name, Unset) else (None, str(self.plan_name).encode(), "text/plain")
        )

        plan_code = (
            self.plan_code if isinstance(self.plan_code, Unset) else (None, str(self.plan_code).encode(), "text/plain")
        )

        plan_description = (
            self.plan_description
            if isinstance(self.plan_description, Unset)
            else (None, str(self.plan_description).encode(), "text/plain")
        )

        billing_period: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = (None, str(self.billing_period.value).encode(), "text/plain")

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

        pricing_model: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.pricing_model, Unset):
            pricing_model = (None, str(self.pricing_model.value).encode(), "text/plain")

        dunning_campaign = (
            self.dunning_campaign
            if isinstance(self.dunning_campaign, Unset)
            else (None, str(self.dunning_campaign).encode(), "text/plain")
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
        if plan_name is not UNSET:
            field_dict["plan_name"] = plan_name
        if plan_code is not UNSET:
            field_dict["plan_code"] = plan_code
        if plan_description is not UNSET:
            field_dict["plan_description"] = plan_description
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period
        if subscription_term_length is not UNSET:
            field_dict["subscription_term_length"] = subscription_term_length
        if billing_cycles is not UNSET:
            field_dict["billing_cycles"] = billing_cycles
        if pricing_model is not UNSET:
            field_dict["pricing_model"] = pricing_model
        if dunning_campaign is not UNSET:
            field_dict["dunning_campaign"] = dunning_campaign
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
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

        plan_name = d.pop("plan_name", UNSET)

        plan_code = d.pop("plan_code", UNSET)

        plan_description = d.pop("plan_description", UNSET)

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, BillingPeriodEnum]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = BillingPeriodEnum(_billing_period)

        subscription_term_length = d.pop("subscription_term_length", UNSET)

        billing_cycles = d.pop("billing_cycles", UNSET)

        _pricing_model = d.pop("pricing_model", UNSET)
        pricing_model: Union[Unset, PricingModelEnum]
        if isinstance(_pricing_model, Unset):
            pricing_model = UNSET
        else:
            pricing_model = PricingModelEnum(_pricing_model)

        dunning_campaign = d.pop("dunning_campaign", UNSET)

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

        patched_plan = cls(
            id=id,
            plan_name=plan_name,
            plan_code=plan_code,
            plan_description=plan_description,
            billing_period=billing_period,
            subscription_term_length=subscription_term_length,
            billing_cycles=billing_cycles,
            pricing_model=pricing_model,
            dunning_campaign=dunning_campaign,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            created_by=created_by,
            updated_by=updated_by,
            deleted_by=deleted_by,
        )

        patched_plan.additional_properties = d
        return patched_plan

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
