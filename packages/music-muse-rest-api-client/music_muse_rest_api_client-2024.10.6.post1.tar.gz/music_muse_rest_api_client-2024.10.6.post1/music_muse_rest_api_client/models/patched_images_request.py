from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="PatchedImagesRequest")


@_attrs_define
class PatchedImagesRequest:
    """
    Attributes:
        description (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):
        image (Union[Unset, File]):
    """

    description: Union[Unset, str] = ""
    name: Union[Unset, str] = UNSET
    image: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        name = self.name

        image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, File]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = File(payload=BytesIO(_image))

        patched_images_request = cls(
            description=description,
            name=name,
            image=image,
        )

        patched_images_request.additional_properties = d
        return patched_images_request

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
