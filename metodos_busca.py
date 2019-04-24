import numpy as np
from queue import PriorityQueue


class No(object):
    def __init__(self, tabuleiro, no_pai, custo_parcial, custo_huristico=0):
        self.tabuleiro = tabuleiro
        self.no_pai = no_pai
        self.custo_parcial = custo_parcial
        self.custo_huristico = custo_huristico
        self.custo_total = self._computar_custo_total()

    def __lt__(self, other):
        return self.custo_total < other.custo_total

    def __eq__(self, other):
        return self.custo_total == other.custo_total

    def _computar_custo_total(self):
        return self.custo_parcial + self.custo_huristico


class BuscaCustoUniforme(object):
    TABULEIRO_FINAL = np.array([[1, 2, 3],
                                [8, 0, 4],
                                [7, 6, 5]])

    def __init__(self, tabuleiro_inicial):
        no_inicial = No(tabuleiro_inicial, None, 0)

        self.visitados = []
        self.nao_visitados = PriorityQueue()
        self.nao_visitados.put((no_inicial.custo_parcial, no_inicial))

    def _final_jogo(self, tabuleiro_atual):
        return np.all(self.TABULEIRO_FINAL == tabuleiro_atual)

    def _get_filhos(self, estado_atual):
        vazio_i, vazio_j = np.where(estado_atual.tabuleiro == 0)
        no_filhos = PriorityQueue()

        if (vazio_i - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] - 1][vazio_j[0]]
            temp[vazio_i[0] - 1][vazio_j[0]] = 0
            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1)
            no_filhos.put((novo_no.custo_parcial, novo_no))

        if (vazio_i + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] + 1][vazio_j[0]]
            temp[vazio_i[0] + 1][vazio_j[0]] = 0
            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1)
            no_filhos.put((novo_no.custo_parcial, novo_no))

        if (vazio_j - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] - 1]
            temp[vazio_i[0]][vazio_j[0] - 1] = 0
            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1)
            no_filhos.put((novo_no.custo_parcial, novo_no))

        if (vazio_j + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] + 1]
            temp[vazio_i[0]][vazio_j[0] + 1] = 0
            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1)
            no_filhos.put((novo_no.custo_parcial, novo_no))

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
                    self.nao_visitados.put((temp.custo_parcial, temp))


class AEstrela(object):
    TABULEIRO_FINAL = np.array([[1, 2, 3],
                                [8, 0, 4],
                                [7, 6, 5]])

    def __init__(self, tabuleiro_inicial):
        no_inicial = No(tabuleiro_inicial, None, 0, self._custo_heuristico(tabuleiro_inicial))

        self.visitados = []
        self.nao_visitados = PriorityQueue()
        self.nao_visitados.put((no_inicial.custo_parcial, no_inicial))

    def _custo_heuristico(self, temp):
        custo = 0
        for elem in range(9):
            pos_i, pos_j = np.where(temp == elem)
            final_i, final_j = np.where(self.TABULEIRO_FINAL == elem)
            custo += abs(final_i[0] - pos_i[0]) + abs(final_j[0] - pos_j[0])

        return custo

    def _final_jogo(self, tabuleiro_atual):
        return np.all(self.TABULEIRO_FINAL == tabuleiro_atual)

    def _get_filhos(self, estado_atual):
        vazio_i, vazio_j = np.where(estado_atual.tabuleiro == 0)
        no_filhos = PriorityQueue()

        if (vazio_i - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] - 1][vazio_j[0]]
            temp[vazio_i[0] - 1][vazio_j[0]] = 0

            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1, self._custo_heuristico(temp))
            no_filhos.put((novo_no.custo_total, novo_no))

        if (vazio_i + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0] + 1][vazio_j[0]]
            temp[vazio_i[0] + 1][vazio_j[0]] = 0

            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1, self._custo_heuristico(temp))
            no_filhos.put((novo_no.custo_total, novo_no))

        if (vazio_j - 1) >= 0:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] - 1]
            temp[vazio_i[0]][vazio_j[0] - 1] = 0

            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1, self._custo_heuristico(temp))
            no_filhos.put((novo_no.custo_total, novo_no))

        if (vazio_j + 1) < self.TABULEIRO_FINAL.shape[0]:
            temp = np.copy(estado_atual.tabuleiro)
            temp[vazio_i[0]][vazio_j[0]] = temp[vazio_i[0]][vazio_j[0] + 1]
            temp[vazio_i[0]][vazio_j[0] + 1] = 0

            novo_no = No(temp, estado_atual, estado_atual.custo_parcial + 1, self._custo_heuristico(temp))
            no_filhos.put((novo_no.custo_total, novo_no))

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
                    if np.all(no.tabuleiro == temp.tabuleiro) and (no.custo_total < temp.custo_total):
                        ja_visitado = True
                        break
                if not ja_visitado:
                    self.nao_visitados.put((temp.custo_total, temp))
