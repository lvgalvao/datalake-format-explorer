"""Módulo para gerenciar o Spotify."""

# manager_spotify.py

import base64
import os

import httpx
from dotenv import load_dotenv

from ..models.spotify_models import (
    AlbumDetails,
    ArtistDetails,
    CompleteArtistDetails,
    TrackDetails,
)

# Carregar variáveis de ambiente do arquivo .env que está na raiz
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)
load_dotenv(dotenv_path=env_path)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


def get_spotify_access_token() -> str:
    """
    Obtém o access token do Spotify.

    Returns:
        str: Access token.
    """
    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("utf-8")
    ).decode("utf-8")
    headers = {"Authorization": f"Basic {auth_header}"}
    data = {"grant_type": "client_credentials"}
    response = httpx.post(AUTH_URL, headers=headers, data=data)
    token_response_data = response.json()
    print(f"[INFO] Access token: {token_response_data['access_token']}")
    return token_response_data["access_token"]


def search_artist(name: str, token: str) -> str:
    """
    Procura por um artista no Spotify e retorna o ID do primeiro resultado.

    Args:
        name (str): Nome do artista.
        token (str): Access token.

    Returns:
        str: ID do artista.
    """
    BASE_URL = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": name, "type": "artist", "limit": 1}
    response = httpx.get(BASE_URL, headers=headers, params=params)
    data = response.json()
    return data["artists"]["items"][0]["id"]


def get_artist_albums(artist_id: str, token: str) -> list:
    """
    Obtém os álbuns de um artista.

    Args:
        artist_id (str): ID do artista.
        token (str): Access token.

    Returns:
        list: Lista de objetos AlbumDetails.
    """
    BASE_URL = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(BASE_URL, headers=headers)
    albums_data = response.json()["items"]
    return [
        AlbumDetails(
            id=album["id"],
            name=album["name"],
            release_date=album.get("release_date", None),
            total_tracks=album["total_tracks"],
        )
        for album in albums_data
    ]


def get_album_tracks(album_id: str, token: str) -> list[TrackDetails]:
    """
    Obtém as músicas de um álbum.

    Args:
        album_id (str): ID do álbum.
        token (str): Access token.

    Returns:
        list: Lista de objetos TrackDetails.
    """
    BASE_URL = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(BASE_URL, headers=headers)
    tracks_data = response.json()["items"]
    return [
        TrackDetails(
            id=track["id"],
            name=track["name"],
            duration_ms=track["duration_ms"],
            release_date=track.get("release_date", "N/A"),
            popularity=track.get("popularity", 0),
            track_ids=[],
        )
        for track in tracks_data
    ]


def get_all_artist_details(artist_name: str) -> list[CompleteArtistDetails]:
    """
    Obtém todos os detalhes de um artista.

    Args:
        artist_name (str): Nome do artista.

    Returns:
        list: Lista de objetos CompleteArtistDetails.
    """
    token = get_spotify_access_token()
    artist_id = search_artist(artist_name, token)
    albums = get_artist_albums(artist_id, token)
    all_tracks = []

    for album in albums:
        tracks = get_album_tracks(album.id, token)
        for track in tracks:
            all_tracks.append(
                CompleteArtistDetails(
                    artist=artist_name,
                    artist_id=artist_id,
                    album=album.name,
                    track=track.name,
                    minutes=track.duration_ms / 60000,  # Convert ms to minutes
                    release_date=track.release_date,
                    popularity=track.popularity,
                )
            )
    return all_tracks


if __name__ == "__main__":
    raul_details = get_all_artist_details("Raul Seixas")
    print(raul_details)
