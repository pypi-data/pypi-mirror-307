from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelsRequest")


@_attrs_define
class LabelsRequest:
    """
    Attributes:
        name (str):
        description (Union[None, Unset, str]):
        cover_image (Union[None, Unset, int]):
    """

    name: str
    description: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        cover_image: Union[None, Unset, int]
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        description: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        cover_image: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        elif isinstance(self.cover_image, int):
            cover_image = (None, str(self.cover_image).encode(), "text/plain")
        else:
            cover_image = (None, str(self.cover_image).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_cover_image(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cover_image = _parse_cover_image(d.pop("cover_image", UNSET))

        labels_request = cls(
            name=name,
            description=description,
            cover_image=cover_image,
        )

        labels_request.additional_properties = d
        return labels_request

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
