import os
import pandas as pd
import streamlit as st

from src.analise import medir_tempos_construcao, medir_tempo_busca

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

# Carregamento e montagem inicial (executado apenas uma vez e armazenado em sessão)
if "avl" not in st.session_state:
    with st.spinner("Construindo árvores e analisando dados..."):
        df_inicial = carregar_csv()
        avl, rb, t_avl, t_rb = medir_tempos_construcao(df_inicial)
        
        st.session_state.df = df_inicial
        st.session_state.avl = avl
        st.session_state.rb = rb
        st.session_state.tempo_carga_avl = t_avl
        st.session_state.tempo_carga_rb = t_rb

avl = st.session_state.avl
rb = st.session_state.rb

# --- MENU LATERAL (Cadastro) ---
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
        # Insere em ambas as árvores em tempo real
        inseriu_avl = avl.inserir(livro["isbn"], livro)
        inseriu_rb = rb.inserir(livro["isbn"], livro)
        
        if inseriu_avl and inseriu_rb:
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([livro])], ignore_index=True)
            os.makedirs("dados", exist_ok=True)
            st.session_state.df.to_csv(CAMINHO_CSV, index=False)
            st.sidebar.success("Livro cadastrado com sucesso nas duas árvores.")
        else:
            st.sidebar.warning("Já existe um livro com esse ISBN.")

# --- TELA PRINCIPAL ---
st.title("📚 Biblioteca em Ordem")
st.caption("Gerenciador de Acervo e Comparativo de Árvores Balanceadas (EDA2)")

# Métricas das Árvores
col1, col2, col3 = st.columns(3)
col1.metric("Acervo Total", avl.tamanho)
col2.metric("Altura (AVL vs RB)", f"{avl.altura_arvore()} / {rb.altura_arvore()}")
col3.metric("Rotações (AVL vs RB)", f"{avl.rotacoes} / {rb.rotacoes}")

# --- BUSCA INSTANTÂNEA ---
st.subheader("🔍 Buscar por ISBN")
isbn_busca = st.text_input("Digite o ISBN exato para pesquisa", key="busca_isbn")

if isbn_busca.strip():
    resultado_avl, tempo_b_avl = medir_tempo_busca(avl, isbn_busca)
    resultado_rb, tempo_b_rb = medir_tempo_busca(rb, isbn_busca)
    
    if resultado_avl:
        st.success("Livro encontrado com sucesso!")
        st.table(pd.DataFrame([resultado_avl]))
        
        # Comparativo de tempo de busca específica
        df_busca = pd.DataFrame({
            "Estrutura": ["Árvore AVL", "Árvore Rubro-Negra"],
            "Tempo de Busca (ms)": [tempo_b_avl, tempo_b_rb]
        })
        st.caption("Desempenho da pesquisa:")
        st.bar_chart(df_busca.set_index("Estrutura"))
    else:
        st.error("Nenhum livro encontrado com esse ISBN.")

st.markdown("---")

# --- ANÁLISE DE DESEMPENHO (Inserção em Lote) ---
st.subheader("📊 Análise de Desempenho Global (Inserção em Lote)")
st.write(f"Tempo total gasto para instanciar e inserir **{avl.tamanho}** livros lidos do CSV na memória.")

df_carga = pd.DataFrame({
    "Estrutura": ["Árvore AVL", "Árvore Rubro-Negra"],
    "Tempo de Carga Total (ms)": [st.session_state.tempo_carga_avl, st.session_state.tempo_carga_rb]
})
st.bar_chart(df_carga.set_index("Estrutura"))

st.markdown("---")

# --- TABELA DE ACERVO ---
st.subheader("📖 Acervo (Ordenado por ISBN)")
registros = [dados for _, dados in avl.em_ordem()]
if registros:
    st.dataframe(pd.DataFrame(registros, columns=COLUNAS))
else:
    st.info("O acervo está vazio.")