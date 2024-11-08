from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="VideoRequest")


@_attrs_define
class VideoRequest:
    """
    Attributes:
        name (str):
        video (File):
        description (Union[Unset, str]):  Default: ''.
    """

    name: str
    video: File
    description: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        video = self.video.to_tuple()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "video": video,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        video = self.video.to_tuple()

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
                "video": video,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        video = File(payload=BytesIO(d.pop("video")))

        description = d.pop("description", UNSET)

        video_request = cls(
            name=name,
            video=video,
            description=description,
        )

        video_request.additional_properties = d
        return video_request

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
