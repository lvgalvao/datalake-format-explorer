"""Essa módulo é responsável por executar a pipeline de ETL."""

import sys

from .ETL.manager_aws import create_bucket, upload_to_s3
from .ETL.manager_polars import save_data_to_formats
from .ETL.manager_spotify import get_all_artist_details


def etl_pipeline(artist_name: str):
    """
    Executa a pipeline de ETL.
    """
    # Step 1: Extract and transform data
    artist_details = get_all_artist_details(artist_name)

    # Step 2: Save data to different formats
    save_data_to_formats(artist_details, artist_name)

    # Step 3: Create a bucket (if not already created)
    bucket_name = f"music-{artist_name.replace(' ', '-').lower()}"
    create_bucket(bucket_name)

    # Step 4: Upload files to S3
    for ext in ["csv", "json", "parquet"]:
        artist_name = artist_name.replace(" ", "-").lower()
        file_name = f"{artist_name}-data.{ext}"
        upload_to_s3(f"data/{file_name}", bucket_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python -m app.pipeline 'Nome do Artista'")
        sys.exit(1)

    artist_name = sys.argv[1]  # Obtenha o nome do artista da linha de comando
    etl_pipeline(artist_name)
