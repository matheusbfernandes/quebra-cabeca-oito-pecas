import numpy as np
from queue import PriorityQueue


class No(object):
    def __init__(self, tabuleiro, no_pai, c_n, h_n=0):
        self.tabuleiro = tabuleiro
        self.no_pai = no_pai
        self.c_n = c_n
        self.h_n = h_n
        self.c_total = self._computar_custo_total()

    def _computar_custo_total(self):
        if self.no_pai is None:
            return self.c_n
        return self.no_pai.c_total + self.c_n

    def __lt__(self, other):
        return self.c_total < other.c_total

    def __eq__(self, other):
        return self.c_total == other.c_total


class BuscaCustoUniforme(object):
    TABULEIRO_FINAL = np.array([[1, 2, 3],
                                [8, 0, 4],
                                [7, 6, 5]])

    def __init__(self, tabuleiro_inicial):
        no_inicial = No(tabuleiro_inicial, None, 0)

        self.visitados = []
        self.nao_visitados = PriorityQueue()
        self.nao_visitados.put((no_inicial.c_n, no_inicial))

    def _final_jogo(self, tabuleiro_atual):
        return np.all(self.TABULEIRO_FINAL == tabuleiro_atual)

    def _calcular_custo(self, temp):
        return 9 - np.sum((self.TABULEIRO_FINAL == temp).astype(int))

    def _get_filhos(self, estado_atual):
        vazio_i, vazio_j = np.where(estado_atual.tabuleiro == 0)
        no_filhos = PriorityQueue()

        if (vazio_i - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] - 1][vazio_j[0]]
            temp[vazio_i[0] - 1][vazio_j[0]] = 0
            novo_no = No(temp, estado_atual, self._calcular_custo(temp))
            no_filhos.put((novo_no.c_n, novo_no))

        if (vazio_i + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] + 1][vazio_j[0]]
            temp[vazio_i[0] + 1][vazio_j[0]] = 0
            novo_no = No(temp, estado_atual, self._calcular_custo(temp))
            no_filhos.put((novo_no.c_n, novo_no))

        if (vazio_j - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] - 1]
            temp[vazio_i[0]][vazio_j[0] - 1] = 0
            novo_no = No(temp, estado_atual, self._calcular_custo(temp))
            no_filhos.put((novo_no.c_n, novo_no))

        if (vazio_j + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] + 1]
            temp[vazio_i[0]][vazio_j[0] + 1] = 0
            novo_no = No(temp, estado_atual, self._calcular_custo(temp))
            no_filhos.put((novo_no.c_n, novo_no))

        return no_filhos

    def buscar_solucao(self):
        while True:
            if self.nao_visitados.empty():
                return "ERRO"

            _, estado_atual = self.nao_visitados.get()
            self.visitados.append(estado_atual)

            if self._final_jogo(estado_atual.tabuleiro):
                pilha_nos = [estado_atual]
                while estado_atual.no_pai is not None:
                    estado_atual = estado_atual.no_pai
                    pilha_nos.append(estado_atual)
                return pilha_nos

            no_filhos = self._get_filhos(estado_atual)

            while not no_filhos.empty():
                _, temp = no_filhos.get()
                ja_visitado = False
                for no in self.visitados:
                    if np.all(no.tabuleiro == temp.tabuleiro):
                        ja_visitado = True
                        break
                if not ja_visitado:
                    self.nao_visitados.put((temp.c_n, temp))
