"""Módulo para gerenciar o S3 da AWS."""

import os

import boto3

# Configurar o cliente do S3 para usar o endpoint do LocalStack e não o da AWS real
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


def create_bucket(bucket_name: str):
    """
    Cria um bucket no S3.

    Args:
        bucket_name (str): Nome do bucket.
    """
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"[INFO] Bucket {bucket_name} created successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to create bucket. Reason: {e}")


def upload_to_s3(file_name: str, bucket_name: str):
    """
    Faz upload de um arquivo para o S3.

    Args:
        file_name (str): Nome do arquivo.
        bucket_name (str): Nome do bucket.
    """
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"[INFO] {file_name} uploaded successfully to {bucket_name}!")
    except Exception as e:
        print(f"[ERROR] Failed to upload {file_name}. Reason: {e}")


if __name__ == "__main__":
    bucket_name = "my-music-data"
    artist_name = "Raul Seixas"
    data_dir = "data"  # Diretório onde os arquivos estão

    # Create a bucket
    create_bucket(bucket_name)

    # Upload files
    for ext in ["csv", "json", "parquet"]:
        file_name = f"{artist_name}-data.{ext}"
        file_path = os.path.join(data_dir, file_name)
        upload_to_s3(file_path, bucket_name)
