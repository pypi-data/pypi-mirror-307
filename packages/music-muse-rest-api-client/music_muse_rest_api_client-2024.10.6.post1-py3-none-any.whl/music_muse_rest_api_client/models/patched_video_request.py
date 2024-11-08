from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="PatchedVideoRequest")


@_attrs_define
class PatchedVideoRequest:
    """
    Attributes:
        description (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):
        video (Union[Unset, File]):
    """

    description: Union[Unset, str] = ""
    name: Union[Unset, str] = UNSET
    video: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        name = self.name

        video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if video is not UNSET:
            field_dict["video"] = video

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if video is not UNSET:
            field_dict["video"] = video

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        _video = d.pop("video", UNSET)
        video: Union[Unset, File]
        if isinstance(_video, Unset):
            video = UNSET
        else:
            video = File(payload=BytesIO(_video))

        patched_video_request = cls(
            description=description,
            name=name,
            video=video,
        )

        patched_video_request.additional_properties = d
        return patched_video_request

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
