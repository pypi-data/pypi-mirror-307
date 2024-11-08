from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define, field as _attrs_field

from ..models.interval_heartbeat_state_schema_type import IntervalHeartbeatStateSchemaType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntervalHeartbeatStateSchema")


@_attrs_define
class IntervalHeartbeatStateSchema:
    """
    Attributes:
        type (IntervalHeartbeatStateSchemaType):
        interval_seconds (int):
        id (Union[None, Unset, int]):
        environment (Union[None, Unset, str]):
        muted (Union[Unset, bool]):  Default: False.
        resolve_incident (Union[Unset, bool]):  Default: True.
        timeout_seconds (Union[Unset, int]):  Default: 0.
    """

    type: IntervalHeartbeatStateSchemaType
    interval_seconds: int
    id: Union[None, Unset, int] = UNSET
    environment: Union[None, Unset, str] = UNSET
    muted: Union[Unset, bool] = False
    resolve_incident: Union[Unset, bool] = True
    timeout_seconds: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        interval_seconds = self.interval_seconds

        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        environment: Union[None, Unset, str]
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        muted = self.muted

        resolve_incident = self.resolve_incident

        timeout_seconds = self.timeout_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "interval_seconds": interval_seconds,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if environment is not UNSET:
            field_dict["environment"] = environment
        if muted is not UNSET:
            field_dict["muted"] = muted
        if resolve_incident is not UNSET:
            field_dict["resolve_incident"] = resolve_incident
        if timeout_seconds is not UNSET:
            field_dict["timeout_seconds"] = timeout_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = IntervalHeartbeatStateSchemaType(d.pop("type"))

        interval_seconds = d.pop("interval_seconds")

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_environment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        environment = _parse_environment(d.pop("environment", UNSET))

        muted = d.pop("muted", UNSET)

        resolve_incident = d.pop("resolve_incident", UNSET)

        timeout_seconds = d.pop("timeout_seconds", UNSET)

        interval_heartbeat_state_schema = cls(
            type=type,
            interval_seconds=interval_seconds,
            id=id,
            environment=environment,
            muted=muted,
            resolve_incident=resolve_incident,
            timeout_seconds=timeout_seconds,
        )

        interval_heartbeat_state_schema.additional_properties = d
        return interval_heartbeat_state_schema

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
