import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Video")


@_attrs_define
class Video:
    """
    Attributes:
        id (int):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        slug (str):
        duration (Union[None, str]):
        video (str):
        description (Union[Unset, str]):  Default: ''.
    """

    id: int
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    slug: str
    duration: Union[None, str]
    video: str
    description: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

        slug = self.slug

        duration: Union[None, str]
        duration = self.duration

        video = self.video

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "updated": updated,
                "name": name,
                "slug": slug,
                "duration": duration,
                "video": video,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_duration(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        duration = _parse_duration(d.pop("duration"))

        video = d.pop("video")

        description = d.pop("description", UNSET)

        video = cls(
            id=id,
            created=created,
            updated=updated,
            name=name,
            slug=slug,
            duration=duration,
            video=video,
            description=description,
        )

        video.additional_properties = d
        return video

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
