import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Genres")


@_attrs_define
class Genres:
    """
    Attributes:
        id (int):
        slug (str):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        description (Union[None, Unset, str]):
        cover_image (Union[None, Unset, int]):
    """

    id: int
    slug: str
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    description: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        slug = self.slug

        created = self.created.isoformat()

        updated = self.updated.isoformat()

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
                "id": id,
                "slug": slug,
                "created": created,
                "updated": updated,
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
        id = d.pop("id")

        slug = d.pop("slug")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

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

        genres = cls(
            id=id,
            slug=slug,
            created=created,
            updated=updated,
            name=name,
            description=description,
            cover_image=cover_image,
        )

        genres.additional_properties = d
        return genres

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
