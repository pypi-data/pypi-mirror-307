import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Albums")


@_attrs_define
class Albums:
    """
    Attributes:
        id (int):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        slug (str):
        release_date (datetime.date):
        cover_image (int):
        labels (List[int]):
        artists (List[int]):
        genres (List[int]):
        description (Union[None, Unset, str]):
    """

    id: int
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    slug: str
    release_date: datetime.date
    cover_image: int
    labels: List[int]
    artists: List[int]
    genres: List[int]
    description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

        slug = self.slug

        release_date = self.release_date.isoformat()

        cover_image = self.cover_image

        labels = self.labels

        artists = self.artists

        genres = self.genres

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
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
                "release_date": release_date,
                "cover_image": cover_image,
                "labels": labels,
                "artists": artists,
                "genres": genres,
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

        release_date = isoparse(d.pop("release_date")).date()

        cover_image = d.pop("cover_image")

        labels = cast(List[int], d.pop("labels"))

        artists = cast(List[int], d.pop("artists"))

        genres = cast(List[int], d.pop("genres"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        albums = cls(
            id=id,
            created=created,
            updated=updated,
            name=name,
            slug=slug,
            release_date=release_date,
            cover_image=cover_image,
            labels=labels,
            artists=artists,
            genres=genres,
            description=description,
        )

        albums.additional_properties = d
        return albums

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
