"""Contains all the data models used in inputs/outputs"""

from .albums import Albums
from .albums_request import AlbumsRequest
from .artists import Artists
from .artists_request import ArtistsRequest
from .audio import Audio
from .audio_request import AudioRequest
from .auth_token import AuthToken
from .auth_token_request import AuthTokenRequest
from .country_enum import CountryEnum
from .genres import Genres
from .genres_request import GenresRequest
from .images import Images
from .images_request import ImagesRequest
from .labels import Labels
from .labels_request import LabelsRequest
from .paginated_albums_list import PaginatedAlbumsList
from .paginated_artists_list import PaginatedArtistsList
from .paginated_audio_list import PaginatedAudioList
from .paginated_genres_list import PaginatedGenresList
from .paginated_images_list import PaginatedImagesList
from .paginated_labels_list import PaginatedLabelsList
from .paginated_tracks_list import PaginatedTracksList
from .paginated_video_list import PaginatedVideoList
from .patched_albums_request import PatchedAlbumsRequest
from .patched_artists_request import PatchedArtistsRequest
from .patched_audio_request import PatchedAudioRequest
from .patched_genres_request import PatchedGenresRequest
from .patched_images_request import PatchedImagesRequest
from .patched_labels_request import PatchedLabelsRequest
from .patched_tracks_request import PatchedTracksRequest
from .patched_video_request import PatchedVideoRequest
from .tracks import Tracks
from .tracks_request import TracksRequest
from .video import Video
from .video_request import VideoRequest

__all__ = (
    "Albums",
    "AlbumsRequest",
    "Artists",
    "ArtistsRequest",
    "Audio",
    "AudioRequest",
    "AuthToken",
    "AuthTokenRequest",
    "CountryEnum",
    "Genres",
    "GenresRequest",
    "Images",
    "ImagesRequest",
    "Labels",
    "LabelsRequest",
    "PaginatedAlbumsList",
    "PaginatedArtistsList",
    "PaginatedAudioList",
    "PaginatedGenresList",
    "PaginatedImagesList",
    "PaginatedLabelsList",
    "PaginatedTracksList",
    "PaginatedVideoList",
    "PatchedAlbumsRequest",
    "PatchedArtistsRequest",
    "PatchedAudioRequest",
    "PatchedGenresRequest",
    "PatchedImagesRequest",
    "PatchedLabelsRequest",
    "PatchedTracksRequest",
    "PatchedVideoRequest",
    "Tracks",
    "TracksRequest",
    "Video",
    "VideoRequest",
)
