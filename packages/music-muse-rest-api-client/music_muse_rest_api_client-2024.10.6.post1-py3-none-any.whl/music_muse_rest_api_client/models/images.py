import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Images")


@_attrs_define
class Images:
    """
    Attributes:
        id (int):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        slug (str):
        image_width (Union[None, int]):
        image_height (Union[None, int]):
        description (Union[Unset, str]):  Default: ''.
        image (Union[Unset, str]):
    """

    id: int
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    slug: str
    image_width: Union[None, int]
    image_height: Union[None, int]
    description: Union[Unset, str] = ""
    image: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

        slug = self.slug

        image_width: Union[None, int]
        image_width = self.image_width

        image_height: Union[None, int]
        image_height = self.image_height

        description = self.description

        image = self.image

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "updated": updated,
                "name": name,
                "slug": slug,
                "image_width": image_width,
                "image_height": image_height,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_image_width(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        image_width = _parse_image_width(d.pop("image_width"))

        def _parse_image_height(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        image_height = _parse_image_height(d.pop("image_height"))

        description = d.pop("description", UNSET)

        image = d.pop("image", UNSET)

        images = cls(
            id=id,
            created=created,
            updated=updated,
            name=name,
            slug=slug,
            image_width=image_width,
            image_height=image_height,
            description=description,
            image=image,
        )

        images.additional_properties = d
        return images

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
