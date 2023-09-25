# manager_spotify.py

import base64
import os
import sys
from typing import List

from dotenv import load_dotenv

from ..models.spotify_models import AlbumDetails, CompleteArtistDetails, TrackDetails
from .handler_http import HTTPMETHODS, HTTPRequest, make_http_request

# Carregar variáveis de ambiente do arquivo .env que está na raiz
env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)
load_dotenv(dotenv_path=env_path)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


async def get_spotify_access_token() -> str:
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

    # Faz a solicitação usando o http_handler
    response = await make_http_request(
        HTTPRequest(url=AUTH_URL, method=HTTPMETHODS.POST, headers=headers, data=data)
    )
    token_response_data = response
    print(f"[INFO] Access token: {token_response_data['access_token']}")
    return token_response_data["access_token"]


async def search_artist(name: str, token: str) -> str:
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

    # Faz a solicitação usando o http_handler
    response = await make_http_request(
        HTTPRequest(
            url=BASE_URL, method=HTTPMETHODS.GET, headers=headers, params=params
        )
    )
    data = response
    return data["artists"]["items"][0]["id"]


async def get_artist_albums(artist_id: str, token: str) -> List[AlbumDetails]:
    """
    Obtém os álbuns de um artista.

    Args:
        artist_id (str): ID do artista.
        token (str): Access token.

    Returns:
        List[AlbumDetails]: Lista de objetos AlbumDetails.
    """
    BASE_URL = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = {"Authorization": f"Bearer {token}"}

    # Faz a solicitação usando o http_handler
    response = await make_http_request(
        HTTPRequest(url=BASE_URL, method=HTTPMETHODS.GET, headers=headers)
    )
    albums_data = response["items"]
    return [
        AlbumDetails(
            id=album["id"],
            name=album["name"],
            release_date=album.get("release_date", None),
            total_tracks=album["total_tracks"],
        )
        for album in albums_data
    ]


async def get_album_tracks(album_id: str, token: str) -> List[TrackDetails]:
    """
    Obtém as músicas de um álbum.

    Args:
        album_id (str): ID do álbum.
        token (str): Access token.

    Returns:
        List[TrackDetails]: Lista de objetos TrackDetails.
    """
    BASE_URL = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}

    # Faz a solicitação usando o http_handler
    response = await make_http_request(
        HTTPRequest(url=BASE_URL, method=HTTPMETHODS.GET, headers=headers)
    )
    tracks_data = response["items"]
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


async def get_all_artist_details(artist_name: str) -> List[CompleteArtistDetails]:
    """
    Obtém todos os detalhes de um artista.

    Args:
        artist_name (str): Nome do artista.

    Returns:
        List[CompleteArtistDetails]: Lista de objetos CompleteArtistDetails.
    """
    token = await get_spotify_access_token()
    artist_id = await search_artist(artist_name, token)
    albums = await get_artist_albums(artist_id, token)
    all_tracks = []

    for album in albums:
        tracks = await get_album_tracks(album.id, token)
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
    if len(sys.argv) != 2:
        print("Uso: python -m app.manager_spotify 'Nome do Artista'")
        sys.exit(1)

    artist_name = sys.argv[1]
    import asyncio

    asyncio.run(get_all_artist_details(artist_name))
