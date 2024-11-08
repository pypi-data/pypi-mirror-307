from io import BytesIO
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="AudioRequest")


@_attrs_define
class AudioRequest:
    """
    Attributes:
        name (str):
        audio (File):
        description (Union[Unset, str]):  Default: ''.
        transcription (Union[None, Unset, str]):
    """

    name: str
    audio: File
    description: Union[Unset, str] = ""
    transcription: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        audio = self.audio.to_tuple()

        description = self.description

        transcription: Union[None, Unset, str]
        if isinstance(self.transcription, Unset):
            transcription = UNSET
        else:
            transcription = self.transcription

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "audio": audio,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if transcription is not UNSET:
            field_dict["transcription"] = transcription

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        audio = self.audio.to_tuple()

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        transcription: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.transcription, Unset):
            transcription = UNSET
        elif isinstance(self.transcription, str):
            transcription = (None, str(self.transcription).encode(), "text/plain")
        else:
            transcription = (None, str(self.transcription).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
                "audio": audio,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if transcription is not UNSET:
            field_dict["transcription"] = transcription

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        audio = File(payload=BytesIO(d.pop("audio")))

        description = d.pop("description", UNSET)

        def _parse_transcription(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        transcription = _parse_transcription(d.pop("transcription", UNSET))

        audio_request = cls(
            name=name,
            audio=audio,
            description=description,
            transcription=transcription,
        )

        audio_request.additional_properties = d
        return audio_request

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
