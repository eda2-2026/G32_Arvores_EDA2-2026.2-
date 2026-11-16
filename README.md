# Biblioteca em Ordem — Gerenciador e Busca de Acervo

## Integrantes
| Matrícula | Nome | 
| ----- | ----- | 
| 231027005 | Maria Samara | 
| 2310391400 | Marjorie Mitzi | 

!!! info "Vídeo da Apresentação"
    **Assista à nossa apresentação:** [Insira o link aqui]

---

## 1. Sobre o projeto

O **Biblioteca em Ordem** é uma aplicação em Python desenvolvida para gerenciar acervos de livros. O diferencial do sistema é a utilização de **Árvores Binárias de Busca Balanceadas** para garantir que a busca por qualquer livro (via ISBN) seja feita em tempo logarítmico $O(\log n)$, mesmo com milhares de registros. Foram implementadas e comparadas a **Árvore AVL** e a **Árvore Rubro-Negra** (Estruturas de Dados 2 - EDA2).

## 2. Funcionalidades

* **Cadastro de Acervo:** Inserção de novos livros (ISBN, Título, Autor, Gênero e Status).
* **Busca Instantânea:** Pesquisa otimizada por ISBN utilizando travessia em árvores balanceadas.
* **Mecanismos de Balanceamento:** Implementação nativa de rotações (Esquerda/Direita) e recoloração (Rubro-Negra).
* **Comparativo de Desempenho:** Painel analítico que compara o tempo de inserção e busca (em milissegundos) entre a Árvore AVL e a Rubro-Negra.
* **Testes Automatizados:** Bateria de testes validando as regras matemáticas de altura (AVL) e propriedades de cor (Rubro-Negra).

## 3. Tecnologias utilizadas

* **Python 3** (Linguagem principal)
* **Streamlit** (Interface Web)
* **Pandas** (Estruturação e leitura de dados do CSV)
* **Unittest** (Testes de unidade e validação das árvores)

## 4. Estrutura do projeto

```text
biblioteca_ordem/
├── app.py                   # Interface web principal e integração
├── requirements.txt         # Dependências do sistema (streamlit==1.10.0, pandas==1.1.5)
├── README.md                # Documentação MkDocs
├── dados/
│   └── livros.csv           # Banco de dados com 5.000 livros gerados para teste
├── src/
│   ├── __init__.py
│   ├── avl_tree.py          # Lógica, nós e rotações da Árvore AVL
│   ├── rb_tree.py           # Lógica, nós e recoloração da Árvore Rubro-Negra
│   └── analise.py           # Integração de busca e captura de tempo (ms)
└── tests/
    ├── __init__.py
    └── test_arvores.py      # Validação rigorosa das regras de balanceamento
```

## 5. Como executar o sistema

### Passo 1 — Crie e ative o ambiente virtual
No Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

!!! tip "Execução no Windows"
    Utilize `python -m venv .venv` e ative o ambiente virtual executando `.\.venv\Scripts\Activate.ps1`

### Passo 2 — Instale as dependências
```bash
python3 -m pip install -r requirements.txt
```

### Passo 3 — Execute a bateria de testes
```bash
python3 -m unittest discover -s tests -v
```

!!! success "Qualidade Garantida"
    Os testes garantem que o Fator de Balanceamento da AVL esteja entre -1 e 1, e que a raiz da Rubro-Negra seja sempre preta.

### Passo 4 — Inicie a aplicação Web
```bash
python3 -m streamlit run app.py
```

A aplicação abrirá no seu navegador padrão (`http://localhost:8501`).