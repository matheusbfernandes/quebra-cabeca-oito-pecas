import numpy as np
import math


class QuebraCabeca(object):
    TAMANHO_QUEBRA_CABECA = 8
    CONFIG_FINAL = np.array([[1, 2, 3],
                             [8, 0, 4],
                             [7, 6, 5]])

    def __init__(self):
        self.dimensao = int(math.sqrt(self.TAMANHO_QUEBRA_CABECA + 1))
        self.tabuleiro = np.arange(self.TAMANHO_QUEBRA_CABECA + 1).reshape((self.dimensao, self.dimensao))
        np.random.shuffle(self.tabuleiro)
        while not self._possui_solucao():
            np.random.shuffle(self.tabuleiro)

    @staticmethod
    def _adjacente_vazio(vazio_i, vazio_j, peca_i, peca_j):
        if vazio_i == peca_i:
            if vazio_j == (peca_j + 1):
                return True
            elif vazio_j == (peca_j - 1):
                return True
        elif vazio_j == peca_j:
            if vazio_i == (peca_i + 1):
                return True
            elif vazio_i == (peca_i - 1):
                return True
        return False

    def mover(self, peca):
        vazio_i, vazio_j = np.where(self.tabuleiro == 0)
        peca_i, peca_j = np.where(self.tabuleiro == peca)

        if self._adjacente_vazio(vazio_i[0], vazio_j[0], peca_i[0], peca_j[0]):
            self.tabuleiro[vazio_i[0]][vazio_j[0]] = peca
            self.tabuleiro[peca_i[0]][peca_j[0]] = 0
            return True

        return False

    def final_jogo(self):
        if np.all(self.CONFIG_FINAL == self.tabuleiro):
            return True
        return False

    def _possui_solucao(self):
        count = 0
        temp = np.reshape(self.tabuleiro, -1)
        for i in range(self.TAMANHO_QUEBRA_CABECA):
            for j in range(i + 1, self.TAMANHO_QUEBRA_CABECA + 1):
                if (temp[i] > 0) and (temp[j] > 0) and (temp[i] > temp[j]):
                    count += 1

        return not((count % 2) == 0)

    def montar_tabuleiro(self, novo_tabuleiro=None):
        if novo_tabuleiro is not None:
            instancia = novo_tabuleiro
        else:
            instancia = self.tabuleiro

        s = ""
        for i in range(instancia.shape[0]):
            s += "+{}+\n|".format('-' * (self.TAMANHO_QUEBRA_CABECA + 3))
            for j in range(instancia.shape[1]):
                s += " {:d} |".format(instancia[i][j])
            s += "\n"
        s += "+{}+".format('-' * (self.TAMANHO_QUEBRA_CABECA + 3))

        return s
