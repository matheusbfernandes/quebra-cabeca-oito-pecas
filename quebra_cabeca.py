import numpy as np
import math
import random


class QuebraCabeca(object):
    TAMANHO_QUEBRA_CABECA = 8

    CONFIG_FINAL = np.array([[1, 2, 3],
                             [8, 0, 4],
                             [7, 6, 5]])

    def __init__(self, tipo_tabuleiro):
        self.dimensao = int(math.sqrt(self.TAMANHO_QUEBRA_CABECA + 1))

        if tipo_tabuleiro[0] == 1:
            self.tabuleiro = np.arange(self.TAMANHO_QUEBRA_CABECA + 1).reshape((self.dimensao, self.dimensao))
            np.random.shuffle(self.tabuleiro.flat)
            while not self._possui_solucao():
                np.random.shuffle(self.tabuleiro)
        else:
            self.tabuleiro = np.copy(self.CONFIG_FINAL)
            for i in range(tipo_tabuleiro[1]):
                vazio_i, vazio_j = np.where(self.tabuleiro == 0)
                pecas = self._adjacente_vazio(vazio_i[0], vazio_j[0])
                peca_aleatoria = random.choice(pecas)
                peca_i, peca_j = np.where(self.tabuleiro == peca_aleatoria)
                self.tabuleiro[vazio_i[0]][vazio_j[0]] = peca_aleatoria
                self.tabuleiro[peca_i[0]][peca_j[0]] = 0

    def _adjacente_vazio(self, vazio_i, vazio_j):
        pecas = []
        if (vazio_i + 1) < 3:
            pecas.append(self.tabuleiro[vazio_i + 1][vazio_j])
        if (vazio_i - 1) >= 0:
            pecas.append(self.tabuleiro[vazio_i - 1][vazio_j])
        if (vazio_j + 1) < 3:
            pecas.append(self.tabuleiro[vazio_i][vazio_j + 1])
        if (vazio_j - 1) >= 0:
            pecas.append(self.tabuleiro[vazio_i][vazio_j - 1])
        return pecas

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
            s += "{}+\n|".format('+---' * 3)
            for j in range(instancia.shape[1]):
                s += " {:d} |".format(instancia[i][j])
            s += "\n"
        s += "{}+".format('+---' * 3)

        return s
