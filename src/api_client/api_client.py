from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NamedTuple, Optional

import requests
import time


class RespostaAPI(NamedTuple):
    """Empacota o status HTTP e o corpo (já parseado) de uma resposta de API."""
    status_code: int
    dados: Any


def get_jogos(
    endereco_api: str,
    token: str,
    endpoint: str,
    edicao: Optional[int] = None,
    rodada: Optional[int] = None,
    pagina: Optional[int] = None,
    por_pagina: Optional[int] = None,
    timeout: int = 30,
    diretorio: str = ''
) -> RespostaAPI:
    """
    Realiza uma requisição GET a um endpoint de uma API, autenticando via
    token no header e repassando query params opcionais.

    Args:
        endereco_api: URL base da API.
        token: Token de autenticação, enviado no header da requisição.
        endpoint: Caminho do endpoint (ex.: "/atletas" ou "atletas").
        edicao: Filtro obrigatorio de temporada.
        rodada: Filtro opcional de id da rodada.
        pagina: Filtro opcional de página (paginação).
        por_pagina: Filtro opcional de itens por página.
        timeout: Timeout (em segundos) para a requisição. Padrão: 30s.
        diretorio: Diretório onde o JSON de resposta será salvo.

    Returns:
        Sempre um RespostaAPI(status_code, dados). Em caso de falha
        (timeout, erro de conexão, erro HTTP não tratado como retry),
        `dados` vem como lista vazia e `status_code` reflete o erro
        (ou -1 quando nem chegou a haver resposta HTTP, ex.: timeout).
    """
    url = f"{endereco_api.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        "token": f"{token}",
    }

    # Monta o dicionário de query params, descartando os valores nulos.
    params_candidatos = {
        "edicao": edicao,
        "rodada": rodada,
        "pagina": pagina,
        "por_pagina": por_pagina,
    }
    params = {chave: valor for chave, valor in params_candidatos.items() if valor is not None}

    dados: Any = []
    status_code = -1
    resposta = None

    try:
        resposta = requests.get(url, headers=headers, params=params, timeout=timeout)
        status_code = resposta.status_code

        if status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 1))
            print(f"Limite de requisições atingido. Aguardando {espera} segundos...")
            time.sleep(espera)
            return get_jogos(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                edicao=edicao,
                rodada=rodada,
                pagina=pagina,
                por_pagina=por_pagina,
                timeout=timeout,
                diretorio=diretorio
            )

        if status_code == 503:
            return get_jogos(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                edicao=edicao,
                rodada=rodada,
                pagina=pagina,
                por_pagina=por_pagina,
                timeout=timeout,
                diretorio=diretorio
            )

        resposta.raise_for_status()
        corpo = resposta.json()
        dados = corpo.get("resultados", {}).get("jogos", [])

    except requests.exceptions.Timeout:
        print("A API demorou demais para responder.")

    except requests.exceptions.HTTPError:
        print(f"A API retornou erro: {status_code}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")

    partes = [endpoint.replace('/', '')]
    for chave, valor in params.items():
        partes.append(str(chave))
        partes.append(str(valor))

    file_name = "_".join(partes)
    file_path = Path(diretorio) / f"{file_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return RespostaAPI(status_code=status_code, dados=dados)


def get_escalacao_by_jogo_id(
    endereco_api: str,
    token: str,
    endpoint: str,
    jogo_id: str = '',
    timeout: int = 30,
    diretorio: str = ''
) -> RespostaAPI:
    url = f"{endereco_api.rstrip('/')}/{endpoint.lstrip('/')}/{jogo_id.lstrip('/')}"

    headers = {
        "token": f"{token}",
    }

    dados: Any = []
    status_code = -1
    resposta = None

    try:
        resposta = requests.get(url, headers=headers, timeout=timeout)
        status_code = resposta.status_code

        if status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 1))
            print(f"Limite de requisições atingido. Aguardando {espera} segundos...")
            time.sleep(espera)
            return get_escalacao_by_jogo_id(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                jogo_id=jogo_id,
                timeout=timeout,
                diretorio=diretorio
            )

        if status_code == 503:
            return get_escalacao_by_jogo_id(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                jogo_id=jogo_id,
                timeout=timeout,
                diretorio=diretorio
            )

        resposta.raise_for_status()
        corpo = resposta.json()
        dados = corpo.get("referencias", {}).get("escalacao", [])

    except requests.exceptions.Timeout:
        print("A API demorou demais para responder.")

    except requests.exceptions.HTTPError:
        print(f"A API retornou erro: {status_code}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")

    file_name = endpoint.replace('/', '') + '_' + jogo_id
    file_path = Path(diretorio) / f"{file_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return RespostaAPI(status_code=status_code, dados=dados)


def get_atleta(
    endereco_api: str,
    token: str,
    endpoint: str,
    atleta_id: str = '',
    timeout: int = 30,
    diretorio: str = ''
) -> RespostaAPI:
    url = f"{endereco_api.rstrip('/')}/{endpoint.lstrip('/')}/{atleta_id.lstrip('/')}"

    headers = {
        "token": f"{token}",
    }

    dados: Any = []
    status_code = -1
    resposta = None

    try:
        resposta = requests.get(url, headers=headers, timeout=timeout)
        status_code = resposta.status_code

        if status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 1))
            print(f"Limite de requisições atingido. Aguardando {espera} segundos...")
            time.sleep(espera)
            return get_atleta(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                atleta_id=atleta_id,
                timeout=timeout,
                diretorio=diretorio
            )

        if status_code == 503:
            return get_atleta(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                atleta_id=atleta_id,
                timeout=timeout,
                diretorio=diretorio
            )

        resposta.raise_for_status()
        corpo = resposta.json()
        dados = corpo.get("resultados", {}).get("atleta", [])

    except requests.exceptions.Timeout:
        print("A API demorou demais para responder.")

    except requests.exceptions.HTTPError:
        print(f"A API retornou erro: {status_code}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")

    file_name = endpoint.replace('/', '') + '_' + atleta_id
    file_path = Path(diretorio) / f"{file_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return RespostaAPI(status_code=status_code, dados=dados)


def get_confrontos(
    endereco_api: str,
    token: str,
    endpoint: str,
    temporada: Optional[int] = None,
    rodada: Optional[int] = None,
    timeout: int = 30,
    diretorio: str = ''
) -> RespostaAPI:
    """
    Realiza uma requisição GET a um endpoint de uma API, autenticando via
    token no header e repassando query params opcionais.

    Args:
        endereco_api: URL base da API.
        token: Token de autenticação, enviado no header da requisição.
        endpoint: Caminho do endpoint (ex.: "/confrontos").
        temporada: Filtro obrigatorio de temporada.
        rodada: Filtro opcional de id da rodada.
        timeout: Timeout (em segundos) para a requisição. Padrão: 30s.
        diretorio: Diretório onde o JSON de resposta será salvo.

    Returns:
        Sempre um RespostaAPI(status_code, dados).
    """
    url = f"{endereco_api.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        "token": f"{token}",
    }

    params_candidatos = {
        "temporada": temporada,
        "rodada": rodada,
    }
    params = {chave: valor for chave, valor in params_candidatos.items() if valor is not None}

    dados: Any = []
    status_code = -1
    resposta = None

    try:
        resposta = requests.get(url, headers=headers, params=params, timeout=timeout)
        status_code = resposta.status_code

        if status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 1))
            print(f"Limite de requisições atingido. Aguardando {espera} segundos...")
            time.sleep(espera)
            return get_confrontos(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                temporada=temporada,  # corrigido: antes era perdido no retry
                rodada=rodada,
                timeout=timeout,
                diretorio=diretorio
            )

        if status_code == 503:
            return get_confrontos(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                temporada=temporada,  # corrigido: antes era perdido no retry
                rodada=rodada,
                timeout=timeout,
                diretorio=diretorio
            )

        resposta.raise_for_status()
        corpo = resposta.json()
        dados = corpo.get("resultados", {}).get("confrontos", [])

    except requests.exceptions.Timeout:
        print("A API demorou demais para responder.")

    except requests.exceptions.HTTPError:
        print(f"A API retornou erro: {status_code}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")

    partes = [endpoint.replace('/', '')]
    for chave, valor in params.items():
        partes.append(str(chave))
        partes.append(str(valor))

    file_name = "_".join(partes)
    file_path = Path(diretorio) / f"{file_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return RespostaAPI(status_code=status_code, dados=dados)


def get_equipes(
    endereco_api: str,
    token: str,
    endpoint: str,
    timeout: int = 30,
    diretorio: str = ''
) -> RespostaAPI:
    """
    Realiza uma requisição GET a um endpoint de uma API, autenticando via
    token no header.

    Returns:
        Sempre um RespostaAPI(status_code, dados).
    """
    url = f"{endereco_api.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        "token": f"{token}",
    }

    dados: Any = []
    status_code = -1
    resposta = None

    try:
        resposta = requests.get(url, headers=headers, timeout=timeout)
        status_code = resposta.status_code

        if status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 1))
            print(f"Limite de requisições atingido. Aguardando {espera} segundos...")
            time.sleep(espera)
            return get_equipes(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                timeout=timeout,
                diretorio=diretorio
            )

        if status_code == 503:
            return get_equipes(
                endereco_api=endereco_api,
                token=token,
                endpoint=endpoint,
                timeout=timeout,
                diretorio=diretorio
            )

        resposta.raise_for_status()
        corpo = resposta.json()
        dados = corpo.get("resultados", {}).get("equipes", [])

    except requests.exceptions.Timeout:
        print("A API demorou demais para responder.")

    except requests.exceptions.HTTPError:
        print(f"A API retornou erro: {status_code}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na requisição: {erro}")

    file_name = endpoint.replace('/', '')
    file_path = Path(diretorio) / f"{file_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return RespostaAPI(status_code=status_code, dados=dados)
