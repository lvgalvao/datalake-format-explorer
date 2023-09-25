"""Módulo de manipulação de solicitações HTTP."""

# http_handler.py

from enum import Enum
from typing import Dict

import httpx
from pydantic import BaseModel, Field


class HTTPMETHODS(Enum):
    """
    Esta classe é uma enumeração de métodos HTTP.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    def upper(self) -> str:
        """
        Retorna o nome do método HTTP em letras maiúsculas.
        """
        return self.value


class HTTPRequest(BaseModel):
    """
    É uma classe que representa uma solicitação HTTP genérica.

    Args:
        url (str): A URL da solicitação.
        method (str): O método HTTP a ser usado (padrão é "GET").
        headers (dict): Um dicionário de cabeçalhos HTTP personalizados.
        params (dict): Um dicionário de parâmetros de consulta.
        data (dict): Um dicionário de dados a serem enviados na solicitação.
    """

    url: str
    method: HTTPMETHODS = "GET"
    headers: Dict = None
    params: Dict = None
    data: Dict = None


async def make_http_request(HTTP_request: HTTPRequest) -> dict:
    """
    Faz uma solicitação HTTP genérica.

    Args:
        http_request (HTTPRequest): Um objeto HTTPRequest contendo os detalhes da solicitação.

    Returns:
        dict: A resposta JSON da solicitação HTTP.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(
            HTTP_request.method,
            HTTP_request.url,
            headers=HTTP_request.headers,
            params=HTTP_request.params,
            data=HTTP_request.data,
        )
        response.raise_for_status()
        return response.json()
