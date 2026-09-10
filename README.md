# Gato-Mestre

**Gato-Mestre** é um projeto de ciência de dados que prevê a pontuação de jogadores do futebol brasileiro (baseado nas regras do estilo "Cartola") a partir de dados históricos de jogadores, times, jogos e resultados de partidas do Campeonato Brasileiro, cobrindo as temporadas de **2022 a 2025**.

O fluxo do projeto passa pelas seguintes etapas:

1. **Extração de dados**: os dados são obtidos via API e exportados em formato `.json`.
2. **ETL (Extract, Transform, Load)**: tratamento de tipagem dos dados, valores ausentes, valores extremos (outliers) e engenharia de features (feature engineering).
3. **Predição**: geração das previsões de pontuação por jogador, temporada, rodada e partida, utilizando o modelo **LightGBM**.

Ao final do processo, você terá um arquivo de saída com as previsões de pontuação prontas para análise.

<br/>

## Sumário

- [Antes de começar](#antes-de-começar)
- [1. Instalando o uv](#1-instalando-o-uv)
- [2. Clonando o repositório](#2-clonando-o-repositório)
- [3. Instalando as dependências do projeto](#3-instalando-as-dependências-do-projeto)
- [4. Configurando o token de acesso à API](#4-configurando-o-token-de-acesso-à-api)
- [5. Executando o projeto passo a passo](#5-executando-o-projeto-passo-a-passo)
- [6. Onde encontrar o resultado](#6-onde-encontrar-o-resultado)
- [Estrutura de pastas do projeto](#estrutura-de-pastas-do-projeto)
- [Questões para respostas](#questões-para-respostas)

<br/>

## Antes de começar

Este guia foi escrito pensando em quem **nunca usou o `uv`** (o gerenciador de pacotes e ambientes Python utilizado neste projeto) e quer conseguir rodar o Gato-Mestre do zero no próprio computador. Vamos passar por cada etapa com calma.

De forma resumida, o `uv` é uma ferramenta que substitui `pip` + `venv` (e outras ferramentas parecidas), cuidando automaticamente de:
- Baixar a versão correta do Python exigida pelo projeto (definida no arquivo `.python-version`);
- Criar um ambiente virtual isolado para o projeto (assim ele não interfere em outros projetos Python da sua máquina);
- Instalar exatamente as dependências (bibliotecas) listadas no `pyproject.toml`, na versão travada pelo `uv.lock`.

Você **não precisa instalar Python manualmente** antes: o `uv` cuida disso para você.

<br/>

## 1. Instalando o uv

Abra um terminal e escolha o comando de acordo com o seu sistema operacional.

### macOS ou Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Após a instalação, **feche e abra o terminal novamente** (ou abra um novo) para garantir que o comando `uv` fique disponível, e confira se a instalação funcionou:

```bash
uv --version
```

Se aparecer um número de versão (ex: `uv 0.x.x`), está tudo certo.

<br/>

## 2. Clonando o repositório

Ainda no terminal, navegue até a pasta onde você quer salvar o projeto e execute:

```bash
git clone https://github.com/PedroHenFerreira/Gato-Mestre.git
cd Gato-Mestre
```

> Você precisa ter o **Git** instalado na sua máquina para este comando funcionar. Caso não tenha, baixe em [git-scm.com](https://git-scm.com/downloads).

<br/>

## 3. Instalando as dependências do projeto

Dentro da pasta `Gato-Mestre`, rode:

```bash
uv sync
```

Esse comando faz três coisas automaticamente:
1. Instala a versão do Python indicada no arquivo `.python-version` (Python 3.12 ou superior), caso ela ainda não esteja disponível na sua máquina;
2. Cria um ambiente virtual local, dentro de uma pasta `.venv`;
3. Instala todas as bibliotecas listadas no `pyproject.toml` (LightGBM, pandas, scikit-learn, entre outras), nas versões travadas pelo `uv.lock`.

Ao final, você terá um ambiente pronto para rodar o projeto, sem precisar ativar nada manualmente — basta usar `uv run` (explicado adiante) na frente de cada comando.

<br/>

## 4. Configurando o token de acesso à API

O projeto se conecta a uma API para buscar os dados dos jogadores, times e partidas. Essa conexão exige um **token de autenticação**, que é sensível e **não deve ser enviado ao GitHub**.

Por isso, o token fica guardado em uma pasta chamada `.secrets/`, que é ignorada pelo Git (ou seja, mesmo quem clonar o repositório não vai vê-la, pois ela nunca é enviada ao GitHub). Cada pessoa que for rodar o projeto precisa criar essa pasta e esse arquivo manualmente na sua própria máquina.

### Como criar a pasta e o arquivo

Na raiz do projeto, crie a pasta `.secrets` e, dentro dela, um arquivo `secrets.toml`:

```bash
mkdir .secrets
```

Crie o arquivo `.secrets/secrets.toml` com o seguinte conteúdo, substituindo pelo seu token real:

```toml
[api]
token = "SEU_TOKEN_AQUI"
```

<br/>

## 5. Executando o projeto passo a passo

Com as dependências instaladas (`uv sync`) e o token configurado (`.secrets/secrets.toml`), execute os passos **na ordem abaixo**. Sempre a partir da raiz do projeto (`Gato-Mestre/`), usando `uv run` na frente de cada comando — isso garante que o comando rode dentro do ambiente virtual criado pelo `uv`, sem precisar ativá-lo manualmente.

### Passo 1 — Subir o servidor da API

```bash
uv run material_apoio/api_apoio/servidor.py
```

Esse script sobe o servidor que disponibiliza os dados que serão consumidos na próxima etapa. **Deixe esse terminal aberto e rodando** enquanto executa os próximos passos (pode ser necessário abrir um novo terminal para continuar, lembrando de rodar `cd Gato-Mestre` nele também).

### Passo 2 — Gerar/baixar os dados

Em outro terminal (com o servidor do Passo 1 ainda rodando):

```bash
uv run src/gerar_dados.py
```

Esse script consulta a API e exporta os dados brutos em formato `.json` na pasta `src/api_outputs/`.

### Passo 3 — Rodar o notebook de ETL

```bash
uv run jupyter notebook src/notebooks/ETL.ipynb
```

Isso abrirá o Jupyter no navegador. Execute **todas as células do notebook, na ordem, do início ao fim** ("Run All"). Essa etapa trata a tipagem dos dados, valores ausentes, outliers e realiza a engenharia de features, gerando uma base tratada (por exemplo, `src/outputs/base_gm_tratada.parquet`).

> Alternativa (via VS Code): se você usa o VS Code, pode abrir o arquivo `.ipynb` diretamente pela interface e selecionar o interpretador Python do ambiente `.venv` criado pelo `uv` como kernel do notebook.

### Passo 4 — (Opcional) Rodar o notebook de EDA

```bash
uv run jupyter notebook src/notebooks/EDA.ipynb
```

Esse notebook contém a Análise Exploratória de Dados (EDA). Ele é **opcional** — não é necessário para gerar as previsões, mas ajuda a entender melhor a base de dados tratada.

### Passo 5 — Rodar o notebook de predição

```bash
uv run jupyter notebook src/notebooks/Prediction.ipynb
```

Execute **todas as células, do início ao fim**. Esse notebook treina/aplica o modelo **LightGBM** sobre a base tratada e gera as previsões finais de pontuação por jogador, temporada, rodada e partida.

<br/>

## 6. Onde encontrar o resultado

Ao final da execução completa do `Prediction.ipynb`, o resultado da predição estará disponível em:

```
src/outputs/previsoes_{data_e_hora}.json
```

O `{data_e_hora}` no nome do arquivo é gerado automaticamente, representando o momento em que a predição foi executada — assim, cada execução gera um novo arquivo, sem sobrescrever as previsões anteriores.

<br/>

## Estrutura de pastas do projeto

```
Gato-Mestre/
│
├── material_apoio/           # Material de apoio e dados de exemplo/base
│   ├── api_apoio/             # Recursos de apoio relacionados à API (ex: servidor.py)
│   └── base_case_gm.csv       # Caso-base de dados para referência
│
├── src/
│   ├── api_client/
│   │   └── api_client.py      # Cliente responsável por se conectar e consumir a API
│   │
│   ├── notebooks/
│   │   ├── EDA.ipynb           # Análise exploratória dos dados (opcional)
│   │   ├── ETL.ipynb           # Tratamento e engenharia de features
│   │   └── Prediction.ipynb    # Treinamento/predição com LightGBM
│   │
│   ├── outputs/
│   │   └── base_gm_tratada.parquet   # Base tratada gerada pelo ETL
│   │   └── previsoes_{data_hora}.json # Resultado final das previsões
│   │
│   ├── gerar_dados.py          # Script que extrai/exporta os dados via API
│   ├── main.py                 # Ponto de entrada geral do projeto
│   └── utils.py                # Funções utilitárias usadas ao longo do pipeline
│
├── .secrets/                   # Pasta com o token da API (NÃO versionada — veja seção 4)
├── .gitignore
├── .python-version             # Versão do Python usada pelo uv
├── README.md
├── pyproject.toml              # Dependências e metadados do projeto
└── uv.lock                     # Versões travadas das dependências
```

<br/>

## Questões para respostas

1. Que inconsistências você encontrou na base? Para cada uma, qual foi o tratamento adotado e por quê?
```
Foram encontradas algumas inconsistências na base como um todo. Para cada caso, foi adotada a abordagem adequada:

Colunas removidas por alto percentual de valores ausentes:
- adversario_id
- equipe_id
- equipe_id_escalacoes
- home_dummy
- jogo_id_escalacoes
- rodada_confrontos
- titular
- opponent # A coluna 'equipe_visitante_id' traz a mesma informação
- temporada # A coluna 'ano' traz a mesma informação
- edicao # Cerca de 5% de valores ausentes e coluna 'ano' traz a mesma informação
- rodada # Cerca de 5% de valores ausentes
- jogo_id # Cerca de 5% de valores ausentes
- DD

Colunas com valores ausentes droppados:
# Ambas possuíam um pouco menos de 5% de valores ausentes.
# Por ambas representarem informações importantes, os registros com essas colunas
# com valores ausentes foram removidas.
- 'equipe_mandante_id'
- 'equipe_visitante_id'

preco_num:
Essa coluna possuía valores ausentes. Por se tratar do preço do jogador na rodada, ela foi preenchida com a média do jogador.

minutos_jogados:
Foram utilizadas duas condições para o preenchimento dos valores ausentes dessa coluna:
- Se entrou_em_campo for verdadeiro, preenchido com 90;
- Se entrou_em_campo for falso, preenchido com 0.

status_inicial:
Correção de valor. Existiam registros com o valor '0' (como string). Os registros com esse valor foram substituídos por 'reserva'

momento_entrou:
Valores ausentes foram convertidos para 0. A coluna foi convertida de string para int.

momento_substituido:
A coluna foi convertida de string para int. Foi criada uma coluna booleana chamada momento_substituido_ausencia (como valor padrão 0). O preenchimento dos valores ausentes foi feito nas seguintes condições:
- Se entrou_em_campo for verdadeiro, preenchido com 90 e momento_substituido_ausencia recebeu o valor 1;
- Se entrou_em_campo for falso, preenchido com 0 e momento_substituido_ausencia recebeu o valor 1.

equipe_media_pontos_conquistados:
Foi criada uma coluna booleana chamada equipe_media_pontos_conquistados_ausencia (como valor padrão 0). O preenchimento dos valores ausentes foi feito nas seguintes condições:
- Se rodada_id for 1, preenchido com 0 e equipe_media_pontos_conquistados_ausencia recebeu o valor 0;
- Se rodada_id for falso, preenchido com 0 e equipe_media_pontos_conquistados_ausencia recebeu o valor 1.

adversario_media_pontos_cedidos:
Foi criada uma coluna booleana chamada adversario_media_pontos_cedidos_ausencia (como valor padrão 0). O preenchimento dos valores ausentes foi feito nas seguintes condições:
- Se rodada_id for 1, preenchido com 0 e adversario_media_pontos_cedidos_ausencia recebeu o valor 0;
- Se rodada_id for falso, preenchido com 0 e adversario_media_pontos_cedidos_ausencia recebeu o valor 1.

Colunas removidas por não terem relevância para o problema:
- status_inicial
- apelido

status_pre:
A coluna passou por uma limpeza na má formatação de seus valores e criação de dummies.

Tratamento de duplicatas:
- Linhas completamente duplicadas: removidas;
- Linhas com as chaves 'atleta_id' e 'match_id' duplicadas: removidas.

minutos_jogados:
Essa coluna foi winsorizada com p02 e p98 como limite inferior e superior respectivamente.

rodada_id:
Foi criada uma coluna booleana chamada rodada_id_corrigido (como valor padrão 0). O preenchimento dos valores ausentes foi feito nas seguintes condições:
- Se rodada_id for 0, preenchido com 1 e rodada_id_corrigido recebeu o valor 1;
- Se rodada_id for maior que 38, preenchido com 38 e rodada_id_corrigido recebeu o valor 1.
```

<br/>

2. Como você dividiu os dados entre treino e validação? Justifique tecnicamente o critério escolhido.
```
A divisão treino, validação e teste foi feita da seguinte forma:
- Treino: As temporadas completas de 2022 a 2024;
- Validação: A temporada 2025 da rodada 1 até 19;
- Teste: A temporada 2025 da rodada 20 até 38.

Essa escolha foi pensada priorizando 2 pontos muito importantes:
I. Integridade temporal, evitando vazamentos de dados futuros para a divisão de treino;
II. A realidade operacional do modelo. O objetivo é que o modelo preveja as pontuações dos jogadores durante o andamento da temporada.
```

<br/>

3.  Quais  colunas  da  base  você  utilizou  como  variáveis  do  modelo,  e  quais  deixou  de  fora?  Explique  os  dois
lados da decisão.
```
Além das colunas removidas na etapa de ETL (Questão 1), houve outras colunas que não foram utilizadas.

Features sem relevância:
- adversario_quantidade_titulares
- adversario_quantidade_titulares_defensivos
- adversario_quantidade_titulares_ofensivos
- clube_quantidade_titulares
- clube_quantidade_titulares_defensivos
- clube_quantidade_titulares_ofensivos
- equipe_mandante_id
- match_id

Features de vazamento:
- eh_titular
- eh_titular_defensivo
- eh_titular_ofensivo
- jogos_num
- media_num
- minutos_jogados
- minutos_jogados_ausencia
- momento_entrou
- momento_entrou_ausencia
- momento_substituido
- momento_substituido_ausencia
- preco_num
- preco_num_variacao_ultima_1
- status_inicial_nao_relacionado
- status_inicial_reserva
- variacao_num

As demais colunas foram utilizadas como fetures. Devido à grande quantidade, não listarei aqui. Mas elas podem ser encontradas na base `base_gm_tratada.csv`.
```

<br/>

4. Que métricas você usou para avaliar o modelo, e por quê? O resultado obtido justifica colocar a solução em uso?
```
As méttricas utilizadas foram RMSE, MAE e R2. A escolha foi baseada na avaliação por meio da compreensão da magnitude do erro do modelo e no score R2 de cobertura explicativa das features para com a target.

O desemoenho do modelo no dataset de teste foi o seguinte:
RMSE: 2.5634
MAE: 1.4094
R2: 0.3119

O MAE mostra que o modelo erra relativamente pouco em termos de unidades de pontuação. O RMSE nos retorna que existem erros grosseiros, por parte do modelo, de predição em alguns casos.

A maior preocupação é em relação ao R2_score. Ele mostra uma baixa cobertura explicativa dos dados. É um contexto esperado já que tratamos do cenários de desempenho esportivo, porém é um ponto de atenção.

Por compromentimento com uma entrega de qualidade para o usuário final, não seguiria com essa versão do modelo. Porém não descartaria a possibilidade de implementação dessa feature.

Vejo um grande potencial e gostaria de explorar a evolução do desempenho com mais features e outros modelos preditivos.
```