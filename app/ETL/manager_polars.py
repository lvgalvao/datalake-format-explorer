"""Essa módulo é o responsável pelas transformações usando Pandas."""

from typing import List

import polars as pl

from ..models.spotify_models import CompleteArtistDetails


def save_data_to_formats(data: List[CompleteArtistDetails], artist_name: str):
    """
    Salva os dados em diferentes formatos.

    Args:
        data (List[CompleteArtistDetails]): Lista de objetos CompleteArtistDetails.
        artist_name (str): Nome do artista.
    """
    # Converte os dados (que esperamos ser uma lista de objetos CompleteArtistDetails) em um DataFrame do Polars
    df = pl.DataFrame([item.model_dump() for item in data])

    # Substitui espaços em branco por hífens e converte para minúsculas
    artist_name = artist_name.replace(" ", "-").lower()

    # Salva em CSV
    df.write_csv(f"data/{artist_name}-data.csv")

    # Salva em JSON
    df.write_json(f"data/{artist_name}-data.json")

    # Salva em Parquet
    df.write_parquet(f"data/{artist_name}-data.parquet")

    print(f"[INFO] Data for {artist_name} saved in multiple formats!")


if __name__ == "__main__":
    # Como exemplo, suponhamos que você importe a função get_all_artist_details do outro arquivo
    from .manager_spotify import get_all_artist_details

    artist_details = get_all_artist_details("Raul Seixas")
    save_data_to_formats(artist_details, "Raul Seixas")
