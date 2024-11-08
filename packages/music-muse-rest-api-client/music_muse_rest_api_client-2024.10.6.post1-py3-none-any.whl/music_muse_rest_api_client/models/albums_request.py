import datetime
import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AlbumsRequest")


@_attrs_define
class AlbumsRequest:
    """
    Attributes:
        name (str):
        release_date (datetime.date):
        cover_image (int):
        labels (List[int]):
        artists (List[int]):
        genres (List[int]):
        description (Union[None, Unset, str]):
    """

    name: str
    release_date: datetime.date
    cover_image: int
    labels: List[int]
    artists: List[int]
    genres: List[int]
    description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

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
                "name": name,
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

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        release_date = self.release_date.isoformat().encode()

        cover_image = (None, str(self.cover_image).encode(), "text/plain")

        _temp_labels = self.labels
        labels = (None, json.dumps(_temp_labels).encode(), "application/json")

        _temp_artists = self.artists
        artists = (None, json.dumps(_temp_artists).encode(), "application/json")

        _temp_genres = self.genres
        genres = (None, json.dumps(_temp_genres).encode(), "application/json")

        description: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
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
        name = d.pop("name")

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

        albums_request = cls(
            name=name,
            release_date=release_date,
            cover_image=cover_image,
            labels=labels,
            artists=artists,
            genres=genres,
            description=description,
        )

        albums_request.additional_properties = d
        return albums_request

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
