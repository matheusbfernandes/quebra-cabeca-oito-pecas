import os
import time
import platform
from metodos_busca import *
from quebra_cabeca import QuebraCabeca


def limpar_tela():
    if platform.system() == "Linux":
        os.system("clear")
    else:
        os.system("cls")


def main():
    try:
        continuar_resolvendo = True
        while continuar_resolvendo:
            qc = QuebraCabeca()
            solucionador = BuscaCustoUniforme(qc.tabuleiro)
            passos = solucionador.buscar_solucao()
            if passos == "ERRO":
                print("Essa instância do jogo não possui solução.\n")
            else:
                conf_inicial = passos.pop()
                tabuleiro_inicial = qc.montar_tabuleiro(conf_inicial.tabuleiro)
                if not passos:
                    limpar_tela()
                    print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                    print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(1, tabuleiro_inicial, ('#' * 13)))
                    input("Pressione ENTER para continuar.\n")
                else:
                    cont = 1
                    while passos:
                        time.sleep(.05)
                        limpar_tela()
                        print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                        temp = passos.pop()
                        print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(cont, qc.montar_tabuleiro(temp.tabuleiro), ('#' * 13)))
                        input("Pressione ENTER para continuar.\n")
                        cont += 1
            resposta = 'inf'
            while resposta != 's' and resposta != 'n':
                resposta = input("Resolver outro quebra cabeça? (s ou n): ")
            if resposta == 'n':
                continuar_resolvendo = False
    except KeyboardInterrupt:
        pass
    finally:
        print("\nFechando o jogo...")


if __name__ == "__main__":
    main()
