VERMELHO = True
PRETO = False

class NoRB:
    def __init__(self, chave, dados=None):
        self.chave = chave
        self.dados = dados or {}
        self.cor = VERMELHO  # Novos nós são sempre vermelhos na inserção
        self.esquerda = None
        self.direita = None
        self.pai = None

class ArvoreRB:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0
        self.rotacoes = 0

    def rotacao_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda is not None:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y
        self.rotacoes += 1

    def rotacao_direita(self, y):
        x = y.esquerda
        y.esquerda = x.direita
        if x.direita is not None:
            x.direita.pai = y
        x.pai = y.pai
        if y.pai is None:
            self.raiz = x
        elif y == y.pai.direita:
            y.pai.direita = x
        else:
            y.pai.esquerda = x
        x.direita = y
        y.pai = x
        self.rotacoes += 1

    def inserir(self, chave, dados=None):
        chave = str(chave).strip()
        novo_no = NoRB(chave, dados)
        
        y = None
        x = self.raiz

        # Busca a posição de inserção (estilo BST)
        while x is not None:
            y = x
            if novo_no.chave < x.chave:
                x = x.esquerda
            elif novo_no.chave > x.chave:
                x = x.direita
            else:
                return False  # Chave já existe

        novo_no.pai = y
        if y is None:
            self.raiz = novo_no
        elif novo_no.chave < y.chave:
            y.esquerda = novo_no
        else:
            y.direita = novo_no

        self.tamanho += 1
        self._inserir_fixup(novo_no)
        return True

    def _inserir_fixup(self, z):
        while z.pai is not None and z.pai.cor == VERMELHO:
            if z.pai == z.pai.pai.esquerda:
                y = z.pai.pai.direita  # Tio
                if y is not None and y.cor == VERMELHO:
                    z.pai.cor = PRETO
                    y.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.direita:
                        z = z.pai
                        self.rotacao_esquerda(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self.rotacao_direita(z.pai.pai)
            else:
                y = z.pai.pai.esquerda  # Tio
                if y is not None and y.cor == VERMELHO:
                    z.pai.cor = PRETO
                    y.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.esquerda:
                        z = z.pai
                        self.rotacao_direita(z)
                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self.rotacao_esquerda(z.pai.pai)
        self.raiz.cor = PRETO

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
        return self._calcular_altura(self.raiz)

    def _calcular_altura(self, no):
        if no is None:
            return 0
        return 1 + max(self._calcular_altura(no.esquerda), self._calcular_altura(no.direita))