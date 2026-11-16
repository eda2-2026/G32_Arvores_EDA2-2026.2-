import os
import pandas as pd
import streamlit as st

from src.avl_tree import ArvoreAVL

CAMINHO_CSV = os.path.join("dados", "livros.csv")
COLUNAS = ["isbn", "titulo", "autor", "genero", "status_leitura"]
STATUS_OPCOES = ["Quero Ler", "Lendo", "Lido", "Abandonado"]

st.set_page_config(page_title="Biblioteca em Ordem", layout="wide")

def carregar_csv():
    if os.path.exists(CAMINHO_CSV):
        df = pd.read_csv(CAMINHO_CSV, dtype=str).fillna("")
        for col in COLUNAS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUNAS]
    return pd.DataFrame(columns=COLUNAS)


def montar_arvore(df):
    arvore = ArvoreAVL()
    for _, linha in df.iterrows():
        arvore.inserir(linha["isbn"], linha.to_dict())
    return arvore


if "arvore" not in st.session_state:
    df_inicial = carregar_csv()
    st.session_state.df = df_inicial
    st.session_state.arvore = montar_arvore(df_inicial)

arvore = st.session_state.arvore

st.sidebar.header("Novo Livro")
with st.sidebar.form("form_novo_livro", clear_on_submit=True):
    isbn = st.text_input("ISBN")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    genero = st.text_input("Gênero")
    status = st.selectbox("Status de leitura", STATUS_OPCOES)
    enviar = st.form_submit_button("Cadastrar")

if enviar:
    if not isbn.strip() or not titulo.strip():
        st.sidebar.error("ISBN e Título são obrigatórios.")
    else:
        livro = {
            "isbn": isbn.strip(),
            "titulo": titulo.strip(),
            "autor": autor.strip(),
            "genero": genero.strip(),
            "status_leitura": status,
        }
        if arvore.inserir(livro["isbn"], livro):
            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([livro])], ignore_index=True
            )
            os.makedirs("dados", exist_ok=True)
            st.session_state.df.to_csv(CAMINHO_CSV, index=False)
            st.sidebar.success("Livro cadastrado com sucesso.")
        else:
            st.sidebar.warning("Já existe um livro com esse ISBN.")

st.title("Biblioteca em Ordem")
st.caption("Acervo organizado em Árvore AVL")

col1, col2, col3 = st.columns(3)
col1.metric("Livros no acervo", arvore.tamanho)
col2.metric("Altura da árvore AVL", arvore.altura_arvore())
col3.metric("Rotações realizadas", arvore.rotacoes)

st.subheader("Buscar por ISBN")
isbn_busca = st.text_input("Digite o ISBN", key="busca_isbn")
if isbn_busca.strip():
    resultado = arvore.buscar(isbn_busca)
    if resultado:
        st.success("Livro encontrado.")
        st.table(pd.DataFrame([resultado]))
    else:
        st.error("Nenhum livro encontrado com esse ISBN.")

st.subheader("Acervo (em ordem de ISBN)")
registros = [dados for _, dados in arvore.em_ordem()]
if registros:
    st.dataframe(pd.DataFrame(registros, columns=COLUNAS), use_container_width=True)
else:
    st.info("O acervo está vazio.")