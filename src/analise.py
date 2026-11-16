import time
from src.avl_tree import ArvoreAVL
from src.rb_tree import ArvoreRB

def medir_tempos_construcao(df):
    """Retorna as árvores montadas e o tempo (em ms) gasto na inserção em lote."""
    avl = ArvoreAVL()
    rb = ArvoreRB()

    # Mede inserção AVL
    inicio_avl = time.perf_counter()
    for _, linha in df.iterrows():
        avl.inserir(linha["isbn"], linha.to_dict())
    tempo_avl = (time.perf_counter() - inicio_avl) * 1000

    # Mede inserção Rubro-Negra
    inicio_rb = time.perf_counter()
    for _, linha in df.iterrows():
        rb.inserir(linha["isbn"], linha.to_dict())
    tempo_rb = (time.perf_counter() - inicio_rb) * 1000

    return avl, rb, tempo_avl, tempo_rb

def medir_tempo_busca(arvore, chave):
    """Executa a busca de uma chave e retorna o resultado e o tempo em ms."""
    inicio = time.perf_counter()
    resultado = arvore.buscar(chave)
    tempo = (time.perf_counter() - inicio) * 1000
    return resultado, tempo