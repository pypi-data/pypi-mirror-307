import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.country_enum import CountryEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Artists")


@_attrs_define
class Artists:
    """
    Attributes:
        id (int):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        slug (str):
        bio (str):
        birth_date (datetime.date):
        label (int):
        genres (List[int]):
        description (Union[None, Unset, str]):
        country (Union[Unset, CountryEnum]): * `AU` - Австралия
            * `AT` - Австрия
            * `AZ` - Азербайджан
            * `AX` - Аландские острова
            * `AL` - Албания
            * `DZ` - Алжир
            * `AS` - Американское Самоа
            * `AI` - Ангилья
            * `AO` - Ангола
            * `AD` - Андорра
            * `AQ` - Антарктида
            * `AG` - Антигуа и Барбуда
            * `AR` - Аргентина
            * `AM` - Армения
            * `AW` - Аруба
            * `AF` - Афганистан
            * `BS` - Багамские острова
            * `BD` - Бангладеш
            * `BB` - Барбадос
            * `BH` - Бахрейн
            * `BY` - Беларусь
            * `BZ` - Белиз
            * `BE` - Бельгия
            * `BJ` - Бенин
            * `BM` - Бермудские острова
            * `BG` - Болгария
            * `BO` - Боливия
            * `BQ` - Бонайре, Синт-Эстатиус и Саба
            * `BA` - Босния и Герцеговина
            * `BW` - Ботсвана
            * `BR` - Бразилия
            * `IO` - Британская территория в Индийском океане
            * `BN` - Бруней
            * `BF` - Буркина-Фасо
            * `BI` - Бурунди
            * `BT` - Бутан
            * `VU` - Вануату
            * `GB` - Великобритания
            * `HU` - Венгрия
            * `VE` - Венесуэла
            * `VG` - Виргинские Острова (Британские)
            * `VI` - Виргинские Острова (США)
            * `UM` - Внешние малые острова США
            * `VN` - Вьетнам
            * `GA` - Габон
            * `HT` - Гаити
            * `GY` - Гайана
            * `GM` - Гамбия
            * `GH` - Гана
            * `GP` - Гваделупа
            * `GT` - Гватемала
            * `GN` - Гвинея
            * `GW` - Гвинея-Бисау
            * `DE` - Германия
            * `GG` - Гернси
            * `GI` - Гибралтар
            * `HN` - Гондурас
            * `HK` - Гонконг
            * `GD` - Гренада
            * `GL` - Гренландия
            * `GR` - Греция
            * `GE` - Грузия
            * `GU` - Гуам
            * `DK` - Дания
            * `JE` - Джерси
            * `DJ` - Джибути
            * `DM` - Доминика
            * `DO` - Доминиканская Республика
            * `EG` - Египет
            * `ZM` - Замбия
            * `EH` - Западная Сахара
            * `ZW` - Зимбабве
            * `IL` - Израиль
            * `IN` - Индия
            * `ID` - Индонезия
            * `JO` - Иордания
            * `IQ` - Ирак
            * `IR` - Иран
            * `IE` - Ирландия
            * `IS` - Исландия
            * `ES` - Испания
            * `IT` - Италия
            * `YE` - Йемен
            * `CV` - Кабо-Верде
            * `KZ` - Казахстан
            * `KY` - Каймановы острова
            * `KH` - Камбоджа
            * `CM` - Камерун
            * `CA` - Канада
            * `QA` - Катар
            * `KE` - Кения
            * `CY` - Кипр
            * `KG` - Киргизия
            * `KI` - Кирибати
            * `CN` - Китай
            * `CC` - Кокосовые (Килинг) острова
            * `CO` - Колумбия
            * `KM` - Коморские острова
            * `CG` - Конго
            * `CD` - Конго (Демократическая Республика)
            * `CR` - Коста-Рика
            * `CI` - Кот-д'Ивуар
            * `CU` - Куба
            * `KW` - Кувейт
            * `CW` - Кюрасао
            * `LA` - Лаос
            * `LV` - Латвия
            * `LS` - Лесото
            * `LR` - Либерии
            * `LB` - Ливан
            * `LY` - Ливия
            * `LT` - Литва
            * `LI` - Лихтенштейн
            * `LU` - Люксембург
            * `MU` - Маврикий
            * `MR` - Мавритания
            * `MG` - Мадагаскар
            * `YT` - Майотта
            * `MO` - Макао
            * `MW` - Малави
            * `MY` - Малайзия
            * `ML` - Мали
            * `MV` - Мальдивы
            * `MT` - Мальта
            * `MA` - Марокко
            * `MQ` - Мартиника
            * `MH` - Маршалловы острова
            * `MX` - Мексика
            * `FM` - Микронезия (Федеративные Штаты)
            * `MZ` - Мозамбик
            * `MD` - Молдова
            * `MC` - Монако
            * `MN` - Монголия
            * `MS` - Монтсеррат
            * `MM` - Мьянмы
            * `NA` - Намибия
            * `NR` - Науру
            * `NP` - Непал
            * `NE` - Нигер
            * `NG` - Нигерия
            * `NL` - Нидерланды
            * `NI` - Никарагуа
            * `NU` - Ниуэ
            * `NZ` - Новая Зеландия
            * `NC` - Новой Каледонии
            * `NO` - Норвегия
            * `AE` - Объединенные Арабские Эмираты
            * `OM` - Оман
            * `BV` - Остров Буве
            * `IM` - Остров Мэн
            * `NF` - Остров Норфолк
            * `CX` - Остров Рождества
            * `HM` - Остров Херд и Острова Макдоналд
            * `CK` - Острова Кука
            * `TC` - Острова Теркс и Кайкос
            * `PK` - Пакистан
            * `PW` - Палау
            * `PS` - Палестина, Государство
            * `PA` - Панама
            * `PG` - Папуа-Новая Гвинея
            * `PY` - Парагвай
            * `PE` - Перу
            * `PN` - Питкэрн
            * `PL` - Польша
            * `PT` - Португалия
            * `PR` - Пуэрто-Рико
            * `RE` - Реюньон
            * `RU` - Россия
            * `RW` - Руанда
            * `RO` - Румыния
            * `SV` - Сальвадор
            * `WS` - Самоа
            * `SM` - Сан - Марино
            * `ST` - Сан-Томе и Принсипи
            * `SA` - Саудовская Аравия
            * `SX` - Святого Мартина (Остров, нидерландская часть)
            * `MF` - Святого Мартина (Остров, французская часть)
            * `SH` - Святой Елены, Вознесения и Тристан-да-Кунья (Острова)
            * `VA` - Святой Престол
            * `KP` - Северная Корея
            * `MK` - Северная Македония
            * `MP` - Северные Марианские острова
            * `SC` - Сейшельские острова
            * `BL` - Сен-Бартельми
            * `PM` - Сен-Пьер и Микелон
            * `SN` - Сенегал
            * `VC` - Сент-Винсент и Гренадины
            * `KN` - Сент-Китс и Невис
            * `LC` - Сент-Люсия
            * `RS` - Сербия
            * `SG` - Сингапур
            * `SY` - Сирия
            * `SK` - Словакия
            * `SI` - Словения
            * `US` - Соединенные Штаты Америки
            * `SB` - Соломоновы Острова
            * `SO` - Сомали
            * `SD` - Судан
            * `SR` - Суринам
            * `SL` - Сьерра-Леоне
            * `TJ` - Таджикистан
            * `TH` - Таиланд
            * `TW` - Тайвань
            * `TZ` - Танзания
            * `TL` - Тимор-Лесте
            * `TG` - Того
            * `TK` - Токелау
            * `TO` - Тонга
            * `TT` - Тринидад и Тобаго
            * `TV` - Тувалу
            * `TN` - Тунис
            * `TM` - Туркменистан
            * `TR` - Турция
            * `UG` - Уганда
            * `UZ` - Узбекистан
            * `UA` - Украина
            * `WF` - Уоллис и Футуна
            * `UY` - Уругвай
            * `FO` - Фарерские острова
            * `FJ` - Фиджи
            * `PH` - Филиппины
            * `FI` - Финляндия
            * `FK` - Фолклендские (Мальвинские) острова
            * `FR` - Франция
            * `GF` - Французская Гвиана
            * `PF` - Французская Полинезия
            * `TF` - Французские южные территории
            * `HR` - Хорватия
            * `CF` - Центральноафриканская Республика
            * `TD` - Чад
            * `ME` - Черногория
            * `CZ` - Чехия
            * `CL` - Чили
            * `CH` - Швейцария
            * `SE` - Швеция
            * `SJ` - Шпицберген и Ян-Майен
            * `LK` - Шри-Ланка
            * `EC` - Эквадор
            * `GQ` - Экваториальная Гвинея
            * `ER` - Эритрея
            * `SZ` - Эсватини
            * `EE` - Эстония
            * `ET` - Эфиопия
            * `ZA` - Южная Африка
            * `GS` - Южная Георгия и Южные Сандвичевы острова
            * `KR` - Южная Корея
            * `SS` - Южный Судан
            * `JM` - Ямайка
            * `JP` - Япония
        avatar (Union[None, Unset, int]):
    """

    id: int
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    slug: str
    bio: str
    birth_date: datetime.date
    label: int
    genres: List[int]
    description: Union[None, Unset, str] = UNSET
    country: Union[Unset, CountryEnum] = UNSET
    avatar: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

        slug = self.slug

        bio = self.bio

        birth_date = self.birth_date.isoformat()

        label = self.label

        genres = self.genres

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        country: Union[Unset, str] = UNSET
        if not isinstance(self.country, Unset):
            country = self.country.value

        avatar: Union[None, Unset, int]
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "updated": updated,
                "name": name,
                "slug": slug,
                "bio": bio,
                "birth_date": birth_date,
                "label": label,
                "genres": genres,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if country is not UNSET:
            field_dict["country"] = country
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name")

        slug = d.pop("slug")

        bio = d.pop("bio")

        birth_date = isoparse(d.pop("birth_date")).date()

        label = d.pop("label")

        genres = cast(List[int], d.pop("genres"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _country = d.pop("country", UNSET)
        country: Union[Unset, CountryEnum]
        if isinstance(_country, Unset):
            country = UNSET
        else:
            country = CountryEnum(_country)

        def _parse_avatar(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        artists = cls(
            id=id,
            created=created,
            updated=updated,
            name=name,
            slug=slug,
            bio=bio,
            birth_date=birth_date,
            label=label,
            genres=genres,
            description=description,
            country=country,
            avatar=avatar,
        )

        artists.additional_properties = d
        return artists

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
