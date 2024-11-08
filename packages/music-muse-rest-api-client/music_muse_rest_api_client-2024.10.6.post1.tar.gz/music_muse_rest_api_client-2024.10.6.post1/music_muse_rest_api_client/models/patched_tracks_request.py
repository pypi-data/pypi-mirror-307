import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTracksRequest")


@_attrs_define
class PatchedTracksRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[None, Unset, str]):
        album (Union[Unset, int]):
        label (Union[Unset, int]):
        cover_image (Union[Unset, int]):
        track (Union[Unset, int]):
        artists (Union[Unset, List[int]]):
        genres (Union[Unset, List[int]]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    album: Union[Unset, int] = UNSET
    label: Union[Unset, int] = UNSET
    cover_image: Union[Unset, int] = UNSET
    track: Union[Unset, int] = UNSET
    artists: Union[Unset, List[int]] = UNSET
    genres: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        album = self.album

        label = self.label

        cover_image = self.cover_image

        track = self.track

        artists: Union[Unset, List[int]] = UNSET
        if not isinstance(self.artists, Unset):
            artists = self.artists

        genres: Union[Unset, List[int]] = UNSET
        if not isinstance(self.genres, Unset):
            genres = self.genres

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if album is not UNSET:
            field_dict["album"] = album
        if label is not UNSET:
            field_dict["label"] = label
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if track is not UNSET:
            field_dict["track"] = track
        if artists is not UNSET:
            field_dict["artists"] = artists
        if genres is not UNSET:
            field_dict["genres"] = genres

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        description: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        album = self.album if isinstance(self.album, Unset) else (None, str(self.album).encode(), "text/plain")

        label = self.label if isinstance(self.label, Unset) else (None, str(self.label).encode(), "text/plain")

        cover_image = (
            self.cover_image
            if isinstance(self.cover_image, Unset)
            else (None, str(self.cover_image).encode(), "text/plain")
        )

        track = self.track if isinstance(self.track, Unset) else (None, str(self.track).encode(), "text/plain")

        artists: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.artists, Unset):
            _temp_artists = self.artists
            artists = (None, json.dumps(_temp_artists).encode(), "application/json")

        genres: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.genres, Unset):
            _temp_genres = self.genres
            genres = (None, json.dumps(_temp_genres).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if album is not UNSET:
            field_dict["album"] = album
        if label is not UNSET:
            field_dict["label"] = label
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if track is not UNSET:
            field_dict["track"] = track
        if artists is not UNSET:
            field_dict["artists"] = artists
        if genres is not UNSET:
            field_dict["genres"] = genres

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        album = d.pop("album", UNSET)

        label = d.pop("label", UNSET)

        cover_image = d.pop("cover_image", UNSET)

        track = d.pop("track", UNSET)

        artists = cast(List[int], d.pop("artists", UNSET))

        genres = cast(List[int], d.pop("genres", UNSET))

        patched_tracks_request = cls(
            name=name,
            description=description,
            album=album,
            label=label,
            cover_image=cover_image,
            track=track,
            artists=artists,
            genres=genres,
        )

        patched_tracks_request.additional_properties = d
        return patched_tracks_request

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
