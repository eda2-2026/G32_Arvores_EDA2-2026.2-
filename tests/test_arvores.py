import unittest
from src.avl_tree import ArvoreAVL
from src.rb_tree import ArvoreRB, PRETO, VERMELHO

class TestArvoresBalanceadas(unittest.TestCase):

    def setUp(self):
        self.avl = ArvoreAVL()
        self.rb = ArvoreRB()
        # Popula as árvores com dados sequenciais para forçar o pior caso de desbalanceamento
        for i in range(100):
            isbn = f"978-0000{i:03d}"
            self.avl.inserir(isbn, {"id": i})
            self.rb.inserir(isbn, {"id": i})

    # --- Testes Árvore AVL ---
    def verifica_balanceamento_avl(self, no):
        if no is None:
            return True
        fb = self.avl.fator_balanceamento(no)
        # O Fator de Balanceamento deve estar estritamente entre -1 e 1
        if abs(fb) > 1:
            return False
        return self.verifica_balanceamento_avl(no.esquerda) and self.verifica_balanceamento_avl(no.direita)

    def test_avl_fator_balanceamento(self):
        self.assertTrue(self.verifica_balanceamento_avl(self.avl.raiz), 
                        "Árvore AVL possui nós com fator de balanceamento fora do limite [-1, 1]")

    # --- Testes Árvore Rubro-Negra ---
    def verifica_propriedade_vermelha_rb(self, no):
        if no is None:
            return True
        # Se o nó é vermelho, nenhum dos filhos pode ser vermelho
        if no.cor == VERMELHO:
            if no.esquerda and no.esquerda.cor == VERMELHO:
                return False
            if no.direita and no.direita.cor == VERMELHO:
                return False
        return self.verifica_propriedade_vermelha_rb(no.esquerda) and self.verifica_propriedade_vermelha_rb(no.direita)

    def test_rb_raiz_preta(self):
        self.assertEqual(self.rb.raiz.cor, PRETO, "A raiz da Árvore Rubro-Negra deve ser PRETA.")

    def test_rb_filhos_de_vermelhos_sao_pretos(self):
        self.assertTrue(self.verifica_propriedade_vermelha_rb(self.rb.raiz),
                        "Violação RB: Encontrado nó VERMELHO com filho VERMELHO.")

    # --- Testes Comuns ---
    def test_busca_sucesso(self):
        resultado = self.avl.buscar("978-0000050")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["id"], 50)
        
        resultado_rb = self.rb.buscar("978-0000050")
        self.assertIsNotNone(resultado_rb)
        self.assertEqual(resultado_rb["id"], 50)

    def test_busca_falha(self):
        self.assertIsNone(self.avl.buscar("978-INEXISTENTE"))
        self.assertIsNone(self.rb.buscar("978-INEXISTENTE"))

if __name__ == "__main__":
    unittest.main()