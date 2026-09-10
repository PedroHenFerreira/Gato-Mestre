from api_client import api_client
import tomllib
import time
import json
from tqdm import tqdm
from pathlib import Path

def main():
    # Variáveis da api
    # print("CWD:", Path.cwd())
    # print(Path("./.secrets/secrets.toml"))
    # print(Path("./.secrets/secrets.toml").exists())
    config = tomllib.load(open(Path("./.secrets/secrets.toml"), "rb"))
    token = config["api"]["token"]
    endereco_api="http://localhost:8080"
    diretorio = "./src/api_outputs"

    api_client.get_equipes(
        endereco_api=endereco_api,
        token=token,
        endpoint="/equipes",
        diretorio=diretorio + "/equipes"
    )

    for ano in tqdm([2022, 2023, 2024, 2025], desc="Confrontos -Temporada"):
        for rod in tqdm(range(2,38), desc="Confrontos - Rodadas"):
            api_client.get_confrontos(
                endereco_api=endereco_api,
                token=token,
                endpoint="/confrontos",
                temporada=ano,
                rodada=rod,
                diretorio=diretorio + f'/confrontos/{ano}'
            )

            time.sleep(0.25)

    # Leitura dos jogos de cada temporada
    jogos = []
    for ano in tqdm([2022, 2023, 2024, 2025], desc="Jogos - Temporada"):
        for pag in [1, 2]:
            resposta = api_client.get_jogos(
                endereco_api=endereco_api,
                token=token,
                endpoint="/jogos",
                edicao=ano,
                pagina=pag,
                por_pagina=180,
                diretorio=diretorio + f"/jogos/{ano}"
            )

            # try:
            #     jogos.extend(resposta.dados)
            # except AttributeError:
            #     jogos.extend([])
            jogos.extend(resposta.dados)
            time.sleep(1)


    for i in tqdm(range(len(jogos)), desc="Realizando busca de escalação"):
        jogo_id = jogos[i]["jogo_id"]
        api_client.get_escalacao_by_jogo_id(
            endereco_api=endereco_api,
            token=token,
            endpoint='/jogos',
            jogo_id=f"{jogo_id}",
            diretorio=diretorio + f'/escalacoes'
        )

        if i % 100 == 0:
            time.sleep(5)
        else:
            time.sleep(0.25)
    
    caminho = Path("./src/api_outputs/escalacoes")

    atletas_ids = set()
    registros_com_problema = []  # auditoria: jogos/arquivos com algum tipo de exceção

    for arquivo_json in caminho.glob("*.json"):
        with open(arquivo_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if isinstance(dados, dict):
            itens_jogos = dados.items()
        elif isinstance(dados, list):
            itens_jogos = enumerate(dados)
        else:
            registros_com_problema.append((arquivo_json.name, None, "arquivo raiz em formato inesperado"))
            continue

        for jogo_id, jogo in itens_jogos:
            if not isinstance(jogo, dict):
                registros_com_problema.append((arquivo_json.name, jogo_id, "jogo não é dict"))
                continue

            titulares = jogo.get("titulares") or []
            reservas = jogo.get("reservas") or []

            if not titulares and not reservas:
                registros_com_problema.append((arquivo_json.name, jogo_id, "sem titulares/reservas"))

            for lista_jogadores in (titulares, reservas):
                for jogador in lista_jogadores:
                    if isinstance(jogador, dict) and "atleta_id" in jogador:
                        atletas_ids.add(jogador["atleta_id"])
                    else:
                        registros_com_problema.append((arquivo_json.name, jogo_id, "jogador sem atleta_id"))

    i = 0
    for id in tqdm(atletas_ids, desc="Realizando busca de atletas"):
        api_client.get_atleta(
            endereco_api=endereco_api,
            token=token,
            endpoint="/atletas",
            atleta_id=f"{id}",
            diretorio=diretorio + f'/atletas'
        )
        
        if i % 100 == 0:
            time.sleep(5)
        else:
            time.sleep(0.25)

        i += 1

if __name__ == "__main__":
    main()
