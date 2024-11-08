from io import BytesIO
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="PatchedAudioRequest")


@_attrs_define
class PatchedAudioRequest:
    """
    Attributes:
        description (Union[Unset, str]):  Default: ''.
        name (Union[Unset, str]):
        transcription (Union[None, Unset, str]):
        audio (Union[Unset, File]):
    """

    description: Union[Unset, str] = ""
    name: Union[Unset, str] = UNSET
    transcription: Union[None, Unset, str] = UNSET
    audio: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        name = self.name

        transcription: Union[None, Unset, str]
        if isinstance(self.transcription, Unset):
            transcription = UNSET
        else:
            transcription = self.transcription

        audio: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.audio, Unset):
            audio = self.audio.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if transcription is not UNSET:
            field_dict["transcription"] = transcription
        if audio is not UNSET:
            field_dict["audio"] = audio

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        transcription: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.transcription, Unset):
            transcription = UNSET
        elif isinstance(self.transcription, str):
            transcription = (None, str(self.transcription).encode(), "text/plain")
        else:
            transcription = (None, str(self.transcription).encode(), "text/plain")

        audio: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.audio, Unset):
            audio = self.audio.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if transcription is not UNSET:
            field_dict["transcription"] = transcription
        if audio is not UNSET:
            field_dict["audio"] = audio

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        def _parse_transcription(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        transcription = _parse_transcription(d.pop("transcription", UNSET))

        _audio = d.pop("audio", UNSET)
        audio: Union[Unset, File]
        if isinstance(_audio, Unset):
            audio = UNSET
        else:
            audio = File(payload=BytesIO(_audio))

        patched_audio_request = cls(
            description=description,
            name=name,
            transcription=transcription,
            audio=audio,
        )

        patched_audio_request.additional_properties = d
        return patched_audio_request

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
