import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TracksRequest")


@_attrs_define
class TracksRequest:
    """
    Attributes:
        name (str):
        album (int):
        label (int):
        cover_image (int):
        track (int):
        artists (List[int]):
        genres (List[int]):
        description (Union[None, Unset, str]):
    """

    name: str
    album: int
    label: int
    cover_image: int
    track: int
    artists: List[int]
    genres: List[int]
    description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        album = self.album

        label = self.label

        cover_image = self.cover_image

        track = self.track

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
                "album": album,
                "label": label,
                "cover_image": cover_image,
                "track": track,
                "artists": artists,
                "genres": genres,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        album = (None, str(self.album).encode(), "text/plain")

        label = (None, str(self.label).encode(), "text/plain")

        cover_image = (None, str(self.cover_image).encode(), "text/plain")

        track = (None, str(self.track).encode(), "text/plain")

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
                "album": album,
                "label": label,
                "cover_image": cover_image,
                "track": track,
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

        album = d.pop("album")

        label = d.pop("label")

        cover_image = d.pop("cover_image")

        track = d.pop("track")

        artists = cast(List[int], d.pop("artists"))

        genres = cast(List[int], d.pop("genres"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        tracks_request = cls(
            name=name,
            album=album,
            label=label,
            cover_image=cover_image,
            track=track,
            artists=artists,
            genres=genres,
            description=description,
        )

        tracks_request.additional_properties = d
        return tracks_request

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
