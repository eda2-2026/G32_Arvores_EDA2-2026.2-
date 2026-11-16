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

