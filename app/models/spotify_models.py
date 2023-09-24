"""Módulo com os Models do Spotify."""

# spotify_models.py

from typing import List, Optional

from pydantic import BaseModel


class TrackDetails(BaseModel):
    """
    Modelo para os detalhes de uma faixa.
    """

    name: str
    duration_ms: int
    release_date: str
    popularity: int
    track_ids: list  # Lista de IDs das faixas


class AlbumDetails(BaseModel):
    """
    Modelo para os detalhes de um álbum.
    """

    id: str
    name: str
    release_date: Optional[str]
    total_tracks: int
    tracks: Optional[List[TrackDetails]] = []


class ArtistDetails(BaseModel):
    """
    Modelo para os detalhes de um artista.
    """

    id: str
    name: str
    albums: List[AlbumDetails]


class CompleteArtistDetails(BaseModel):
    """
    Modelo para os detalhes completos de um artista.
    """

    artist: str
    artist_id: str
    album: str
    track: str
    minutes: float
    release_date: str
    popularity: int
