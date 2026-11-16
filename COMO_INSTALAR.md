# Como instalar e rodar o programa (Windows)

Leva uns 10 minutos. Só precisa fazer os passos 1 a 3 **uma vez**.
Depois disso, para abrir o programa é só o passo 4.

---

## Passo 1 — Baixar a pasta do projeto

1. Baixe a pasta `Programa_Estatiticas` do Drive do grupo.
2. Se vier como `.zip`, clique com o botão direito → **Extrair tudo**.
3. Coloque a pasta em um lugar fácil, por exemplo na **Área de Trabalho**.

Confira se dentro dela tem isto:

```
Programa_Estatiticas/
├── requirements.txt
└── src/
    ├── app.py
    └── data/
        └── test.csv  ← sem esse arquivo o programa não abre
```

---

## Passo 2 — Instalar o Python (Miniconda)

> Se você já tem Python ou Anaconda instalado, pule para o passo 3.

1. Entre em **https://www.anaconda.com/download/success** e baixe o **Miniconda** para Windows.
2. Abra o instalador e vá clicando em **Next** até o fim (pode deixar tudo como já vem marcado).
3. Quando terminar, abra o menu Iniciar e procure por **Anaconda Prompt**.
   É uma janela preta — é nela que vamos digitar os comandos.

---

## Passo 3 — Instalar as bibliotecas (PyQt5, pandas e matplotlib)

1. Abra o **Anaconda Prompt**.
2. Entre na pasta do projeto. Se ela está na Área de Trabalho, digite:

   ```
   cd Desktop\Programa_Estatiticas
   ```

   Dica: dá para digitar `cd ` (com espaço) e **arrastar a pasta** para dentro da janela preta.
   O caminho aparece sozinho. Depois é só apertar Enter.

3. Instale as bibliotecas:

   ```
   pip install -r requirements.txt
   ```

   Espere aparecer `Successfully installed ...`.

---

## Passo 4 — Abrir o programa

Ainda no Anaconda Prompt, dentro da pasta do projeto:

```
python src/app.py
```

A janela do programa abre em 2 ou 3 segundos (ele está lendo os 110 mil clientes).

**Nas próximas vezes:** abrir o Anaconda Prompt → `cd` até a pasta → `python src/app.py`.

---

## Se der erro

| O que aparece | O que fazer |
|---|---|
| `'python' não é reconhecido...` ou abre a Microsoft Store | Você está no Prompt de Comando comum. Feche e abra o **Anaconda Prompt**. |
| `No module named 'PyQt5'`, `'pandas'` ou `'matplotlib'` | Faltou o passo 3. Rode `pip install -r requirements.txt`. |
| `can't open file ... app.py` | Você não está na pasta certa. Use `cd` para entrar na pasta `Programa_Estatiticas`. Digite `dir` e veja se a pasta `src` aparece na lista. |
| `No module named 'services'` ou `'styles'` | Faltou algum arquivo. Confira se `src/services` e `src/styles` vieram do Drive. |
| `FileNotFoundError ... test.csv` | O `test.csv` não está dentro de `src/data`. Baixe de novo do Drive. |
| O sistema não encontra o caminho (no `cd`) | Seu Desktop pode estar no OneDrive. Use a dica de arrastar a pasta para a janela. |

---

## Usando o VS Code (opcional)

1. Abra o VS Code → **Arquivo → Abrir Pasta** → escolha `Programa_Estatiticas`.
2. Aperte `Ctrl + Shift + P`, digite **Python: Select Interpreter** e escolha o que tem **miniconda3** no nome.
3. Abra o `src/app.py` e clique no botão ▶ no canto de cima.
