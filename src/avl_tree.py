class NoAVL:
    def __init__(self, chave, dados=None):
        self.chave = chave          
        self.dados = dados or {}   
        self.esquerda = None
        self.direita = None
        self.altura = 1            

class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0
        self.rotacoes = 0         

    @staticmethod
    def altura(no):
        return no.altura if no else 0

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def rotacao_direita(self, y):
        x = y.esquerda
        y.esquerda = x.direita
        x.direita = y
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        self.rotacoes += 1
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda
        y.esquerda = x
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        self.rotacoes += 1
        return y

    def rotacao_dupla_direita(self, no):
        no.esquerda = self.rotacao_esquerda(no.esquerda)
        return self.rotacao_direita(no)

    def rotacao_dupla_esquerda(self, no):
        no.direita = self.rotacao_direita(no.direita)
        return self.rotacao_esquerda(no)

    def _balancear(self, no):
        self._atualizar_altura(no)
        fb = self.fator_balanceamento(no)

        if fb > 1:  
            if self.fator_balanceamento(no.esquerda) >= 0:
                return self.rotacao_direita(no)          
            return self.rotacao_dupla_direita(no)        

        if fb < -1:  
            if self.fator_balanceamento(no.direita) <= 0:
                return self.rotacao_esquerda(no)         
            return self.rotacao_dupla_esquerda(no)       

        return no

    def inserir(self, chave, dados=None):
        chave = str(chave).strip()
        self._inseriu = False
        self.raiz = self._inserir(self.raiz, chave, dados)
        if self._inseriu:
            self.tamanho += 1
        return self._inseriu

    def _inserir(self, no, chave, dados):
        if no is None:
            self._inseriu = True
            return NoAVL(chave, dados)

        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, dados)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, dados)
        else:
            return no  

        return self._balancear(no)

    def buscar(self, chave):
        chave = str(chave).strip()
        no = self.raiz
        while no is not None:
            if chave == no.chave:
                return no.dados
            no = no.esquerda if chave < no.chave else no.direita
        return None

    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is not None:
            self._em_ordem(no.esquerda, resultado)
            resultado.append((no.chave, no.dados))
            self._em_ordem(no.direita, resultado)

    def altura_arvore(self):
        return self.altura(self.raiz)


if __name__ == "__main__":
    arvore = ArvoreAVL()
    for i in range(1, 16):
        arvore.inserir(f"{i:03d}", {"titulo": f"Livro {i}"})
    print("Altura:", arvore.altura_arvore())    
    print("Rotações:", arvore.rotacoes)
    print("Em ordem:", [c for c, _ in arvore.em_ordem()])
    print("Busca 007:", arvore.buscar("007"))