# Welcome to MkDocs

## Descrição

O projeto consiste em coletar dados de uma API do Spotify, transformar os dados em diferentes formatos e armazenar em um bucket na AWS.

## Fluxo

```mermaid
flowchart LR
    A[Manager Spotify: Coleta de Dados] -->|Extrai dados| B(Manager Pandas: Converte Formatos)
    B -->|Converte p/ CSV| C[Load: Salva no Bucket]
    B -->|Converte p/ Parquet| C[Manager AWS: Salva no Bucket]
    B -->|Converte p/ JSON| C[Manager AWS: Salva no Bucket]
    B -->|Converte p/ XLS| C[Manager AWS: Salva no Bucket]
    C -->|Salva como CSV| D1[Bucket AWS]
    C -->|Salva como Parquet| D1[Bucket AWS]
    C -->|Salva como JSON| D1[Bucket AWS]
    C -->|Salva como XLS| D1[Bucket AWS]
```

## Módulos

### ::: app.ETL.manager_spotify

### ::: app.ETL.manager_pandas

### ::: app.ETL.manager_aws
