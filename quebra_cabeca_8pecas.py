import numpy as np
import math
import os
import time
import platform


class QuebraCabeca(object):
    TAMANHO_QUEBRA_CABECA = 8

    def __init__(self):
        self.dimensao = int(math.sqrt(self.TAMANHO_QUEBRA_CABECA + 1))
        self.tabuleiro = np.arange(self.TAMANHO_QUEBRA_CABECA + 1).reshape((self.dimensao, self.dimensao))
        np.random.shuffle(self.tabuleiro)

    @staticmethod
    def adjacente_vazio(vazio_i, vazio_j, peca_i, peca_j):
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

        if self.adjacente_vazio(vazio_i[0], vazio_j[0], peca_i[0], peca_j[0]):
            self.tabuleiro[vazio_i[0]][vazio_j[0]] = peca
            self.tabuleiro[peca_i[0]][peca_j[0]] = 0
            return True

        return False

    def final_jogo(self):
        temp = np.reshape(self.tabuleiro, -1)

        for i in range(temp.shape[0] - 2):
            if temp[i + 1] < temp[i]:
                return False
        return True

    def possui_solucao(self):
        count = 0
        temp = np.reshape(self.tabuleiro, -1)
        for i in range(self.TAMANHO_QUEBRA_CABECA):
            for j in range(i + 1, self.TAMANHO_QUEBRA_CABECA + 1):
                if (temp[i] > 0) and (temp[j] > 0) and (temp[i] > temp[j]):
                    count += 1

        return (count % 2) == 0

    def montar_tabuleiro(self):
        s = ""
        for i in range(self.tabuleiro.shape[0]):
            s += "+{}+\n|".format('-' * (self.TAMANHO_QUEBRA_CABECA + 3))
            for j in range(self.tabuleiro.shape[1]):
                s += " {:d} |".format(self.tabuleiro[i][j])
            s += "\n"
        s += "+{}+".format('-' * (self.TAMANHO_QUEBRA_CABECA + 3))

        return s


def main():
    qb = QuebraCabeca()

    try:
        while not qb.final_jogo():
            time.sleep(.05)

            if platform.system() == "Linux":
                os.system("clear")
            else:
                os.system("cls")

            if qb.possui_solucao():
                print("Essa instância possui solução.")
            else:
                print("Essa instância não possui solução.")

            print(qb.montar_tabuleiro())

            peca = int(input("Informe a peça que será movimentada: "))
            while not qb.mover(peca):
                peca = int(input("Peça inválida, digite uma válida: "))
    except KeyboardInterrupt:
        print("\nFechando o jogo...")


if __name__ == "__main__":
    main()
