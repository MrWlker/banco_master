# Sistema de Análise de Clientes

Trabalho prático de Linguagem de Programação.

O programa lê o arquivo `test.csv`, que contém 110.023 clientes de um banco, permite buscar e filtrar esses clientes em uma janela gráfica e apresenta estatísticas dos resultados da consulta.

## Como rodar

O passo a passo completo para quem nunca instalou o programa está no arquivo [COMO_INSTALAR.md](COMO_INSTALAR.md).

Na primeira execução, instale as dependências:

```bash
pip install -r requirements.txt
```

Depois, sempre que quiser abrir o programa, execute o comando abaixo dentro da pasta `Programa_Estatiticas`:

```bash
python src/app.py
```

## Como usar a tela

- **Barra de busca (parte superior):** digite o sobrenome ou o código do cliente e pressione Enter.
- **Filtros:** permitem filtrar por país, faixa de idade, gênero, situação (ativo/inativo), faixa de score e saldo mínimo. Os filtros funcionam todos juntos e em conjunto com a busca. Para ver os **inativos com saldo alto**, escolha Situação = Inativos e um saldo mínimo.
- **Tabela:** apresenta os clientes encontrados.
- **Caixa inferior:** mostra a quantidade de clientes encontrados.
- **Aba Estatísticas:** apresenta as médias de saldo, salário, score e idade; o total de clientes por país; a quantidade de clientes em cada faixa de score; e três gráficos (país, faixa de score e idades). Todas as estatísticas são calculadas com base nos resultados da consulta exibidos na tabela.

## Como o projeto está organizado

```text
Programa_Estatiticas/
│
├── src/                         # Todo o código do programa
│   ├── app.py                   # Ponto de entrada: arquivo que inicia o programa
│   ├── services/                # Lógica de leitura, busca, filtros e cálculos
│   │   ├── filtros.py           # Leitura, busca e filtros (código do Colab)
│   │   ├── estatisticas.py      # Médias, contagens por país e faixas de score
│   │   └── graficos.py          # Gráficos com pandas e matplotlib
│   ├── styles/                  # Interface gráfica (PyQt5)
│   │   ├── windows.py           # Monta a janela e chama as funções
│   │   ├── tables.py            # Tabela de clientes
│   │   └── style.py             # Cores e aparência
│   └── data/                    # Arquivos de dados
│       ├── test.csv
│       └── train.csv
│
└── docs/                        # Material do trabalho (enunciado, rascunhos
                                 # da tela e notebook original do Colab)
```

## Explicando cada parte em uma frase

| Pasta ou arquivo | O que faz | Comparação |
|---|---|---|
| `src/app.py` | Liga tudo: carrega os dados e abre a tela. | O botão de ligar |
| `src/services` | Executa o trabalho com os dados. | A cozinha do restaurante |
| `src/styles` | Mostra os resultados e recebe as interações do usuário. | O salão e o garçom |
| `src/data` | Armazena os arquivos com os dados dos clientes. | A despensa |

**Regra principal:** a interface (`styles`) nunca realiza buscas, filtros ou cálculos diretamente. Ela apenas chama as funções (`services`) e apresenta os resultados. Assim, é possível trocar a interface sem alterar a lógica do programa, ou modificar a lógica sem precisar reconstruir a interface.

## Caminho que o programa percorre

1. `app.py` chama `leitura()`, que abre o arquivo `test.csv` e armazena os clientes em uma lista.
2. `app.py` abre a janela e entrega essa lista para ela.
3. O usuário digita uma busca ou seleciona um filtro na janela.
4. A janela chama `pesquisar_nome_id()` para realizar a busca e, em seguida, `pesquisar_idade_genero_atividade()` (gênero e situação) e `pesquisar_pais_idade_score_saldo()` (país, idade, score e saldo) para aplicar os filtros.
5. As funções devolvem a lista de clientes encontrados, e a janela apresenta os resultados na tabela.
6. Na aba Estatísticas, a janela envia essa mesma lista para as funções de `estatisticas.py` e `graficos.py` e apresenta os resultados obtidos.

## Onde aparecem os itens obrigatórios do trabalho

| Item obrigatório | Onde está implementado |
|---|---|
| Manipulação de arquivos | `leitura()` abre e lê o arquivo `test.csv`. |
| Funções | `leitura()`, `pesquisar_nome_id()`, `pesquisar_idade_genero_atividade()`, `pesquisar_pais_idade_score_saldo()`, `calcular_media()`, `contar_por_pais()`, `classificar_score()` e `contar_por_faixa_score()`. |
| Estruturas condicionais | Os comandos `if` dos filtros e as condições de `classificar_score()`. |
| Estruturas de repetição | Os comandos `for` que percorrem as linhas do arquivo, a lista de clientes e realizam as contagens. |

## Funções de busca e filtro (`src/services/filtros.py`)

- **`leitura()`** — lê o arquivo `test.csv` uma única vez e monta a lista `dados_gerais`, na qual cada cliente é representado por um dicionário.
- **`pesquisar_nome_id(dados_gerais, nome_id)`** — busca clientes pelo sobrenome ou pelo código do cliente (`CustomerId`).
- **`pesquisar_idade_genero_atividade(dados_gerais, idade, genero, membro_ativo)`** — filtra os clientes por idade, gênero e/ou situação de membro ativo.

O código dessas três funções é o mesmo utilizado no notebook original do Colab (`docs/codigo_original_colab.ipynb`). A única alteração foi o caminho do arquivo `test.csv` dentro da função `leitura()`.

- **`pesquisar_pais_idade_score_saldo(dados_gerais, pais, idade_minima, idade_maxima, faixa_score, saldo_minimo)`** — filtra os clientes por país, faixa de idade, faixa de score de crédito e/ou saldo mínimo. Foi adicionada depois, seguindo o mesmo padrão da função de cima: cada filtro é opcional e, se o cliente não passar em um deles, o `continue` pula para o próximo cliente.

## Funções de estatística (`src/services/estatisticas.py`)

- **`media_saldo(dados)`, `media_salario(dados)`, `media_score(dados)` e `media_idade(dados)`** — calculam as respectivas médias. Todas utilizam a função auxiliar `calcular_media(dados, coluna)`.
- **`contar_por_pais(dados)`** — contabiliza a quantidade de clientes em cada país.
- **`classificar_score(score)`** — classifica o score como Excelente, Bom, Regular ou Ruim.
- **`contar_por_faixa_score(dados)`** — contabiliza a quantidade de clientes em cada faixa de score.

## Gráficos (`src/services/graficos.py`)

Os gráficos utilizam duas bibliotecas:

- **Pandas:** transforma a lista de clientes em uma tabela e permite agrupar e contabilizar os valores.
- **Matplotlib:** gera os gráficos a partir dos dados processados.

A janela apresenta os gráficos por meio do componente `FigureCanvasQTAgg`.

Funções disponíveis:

- **`grafico_por_pais(dados, eixo)`** — gera um gráfico de barras com a quantidade de clientes por país.
- **`grafico_por_faixa_score(dados, eixo)`** — gera um gráfico de barras com a quantidade de clientes por faixa de score.
- **`grafico_idades(dados, eixo)`** — gera um histograma com a distribuição das idades.