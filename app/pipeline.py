# pipeline.py

import asyncio
import os
import sys
import time

from loguru import logger

from .ETL.manager_aws import create_bucket, upload_to_s3
from .ETL.manager_polars import save_data_to_formats
from .ETL.manager_spotify import get_all_artist_details

logger.remove()  # Remove qualquer configuração de log anterior (opcional)
logger.add("análise.log", rotation="10 MB", level="INFO")


async def analyze_file_sizes(artist_name: str):
    """
    Analisa e compara o tamanho dos arquivos gerados em diferentes formatos.
    Recomenda o formato com o menor volume total.
    """
    # Diretório onde os arquivos estão
    data_dir = "data"

    # Nomes dos arquivos
    csv_file = f"{artist_name.lower().replace(' ', '-')}-data.csv"
    json_file = f"{artist_name.lower().replace(' ', '-')}-data.json"
    parquet_file = f"{artist_name.lower().replace(' ', '-')}-data.parquet"

    # Caminhos completos dos arquivos
    csv_path = os.path.join(data_dir, csv_file)
    json_path = os.path.join(data_dir, json_file)
    parquet_path = os.path.join(data_dir, parquet_file)

    # Obtém os tamanhos dos arquivos
    csv_size = os.path.getsize(csv_path)
    json_size = os.path.getsize(json_path)
    parquet_size = os.path.getsize(parquet_path)

    # Calcula as somas dos tamanhos
    total_csv_size = csv_size
    total_json_size = json_size
    total_parquet_size = parquet_size

    # Determina o formato com o menor volume total
    smallest_format = "CSV"
    smallest_size = total_csv_size

    if total_json_size < smallest_size:
        smallest_format = "JSON"
        smallest_size = total_json_size

    if total_parquet_size < smallest_size:
        smallest_format = "Parquet"
        smallest_size = total_parquet_size

    # Imprime os resultados
    logger.info(f"Análise de tamanho dos arquivos para {artist_name}:")
    logger.info(f"Tamanho total do arquivo CSV: {total_csv_size} bytes")
    logger.info(f"Tamanho total do arquivo JSON: {total_json_size} bytes")
    logger.info(f"Tamanho total do arquivo Parquet: {total_parquet_size} bytes")
    logger.info(
        f"Recomendação: Use o formato {smallest_format} com o menor volume total."
    )

    # Retorna o formato recomendado
    return smallest_format


async def etl_pipeline(artist_name: str):
    """
    Executa a pipeline de ETL.
    """
    # Step 0: Start timer

    start_time = time.time()

    # Step 1: Extract and transform data
    artist_details = await get_all_artist_details(artist_name)

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

    # Step 5: Analyze file sizes and recommend format
    recommended_format = await analyze_file_sizes(artist_name)
    logger.info(f"Formato recomendado: {recommended_format}")

    # Step 6: Stop timer and print total time

    end_time = time.time()
    total_time = end_time - start_time

    logger.info(f"Tempo total de execução: {total_time} segundos")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python -m app.pipeline 'Nome do Artista'")
        sys.exit(1)

    artist_name = sys.argv[1]  # Obtenha o nome do artista da linha de comando
    asyncio.run(etl_pipeline(artist_name))
