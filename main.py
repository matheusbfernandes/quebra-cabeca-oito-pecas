import os
import platform
from metodos_busca import *
from quebra_cabeca import QuebraCabeca
import time


class InferfaceUsuario(object):
    def __init__(self):
        self.opcoes_selecionadas = {"Op1": [1, 0],
                                    "Op2": False,
                                    "Op3": 600.0,
                                    "Op4": 100}

    @staticmethod
    def limpar_tela():
        if platform.system() == "Linux":
            os.system("clear")
        else:
            os.system("cls")

    @staticmethod
    def _opcoes_tabuleiro():
        s = "*** Selecione a opção desejada ***\n" \
            "   1. Tabuleiro aleatório\n" \
            "   2. Tabuleiro embaralhado\n" \
            "\n    3. Retornar ao menu principal\n"
        return s

    def _montar_opcoes(self):
        s = "*** Selecione as opções desejadas ***\n" \
            "   1. Opções do tabuleiro\n"

        if not self.opcoes_selecionadas["Op2"]:
            s += "   2. Não usar uma função heurística\n"
        else:
            s += "   2. Usar uma função heurística\n"

        s += "   3. Colocar limite de tempo\n" \
             "   4. Colocar limite de movimentações\n" \
             "\n   5. Resolver\n"
        return s

    def interface_escolhas(self):
        continuar = False
        while not continuar:
            self.limpar_tela()
            print(self._montar_opcoes())
            opcao = int(input("Digite a opção desejada: "))
            while (opcao < 1) and (opcao > 5):
                self.limpar_tela()
                print(self._montar_opcoes())
                opcao = int(input("Opção inválida, digite uma opção válida: "))
            if opcao == 5:
                continuar = True
            elif opcao == 1:
                self.limpar_tela()
                print(self._opcoes_tabuleiro())
                opcao_tabuleiro = int(input("Digite a opção desejada: "))
                while (opcao_tabuleiro < 1) or (opcao_tabuleiro > 3):
                    self.limpar_tela()
                    print(self._opcoes_tabuleiro())
                    opcao_tabuleiro = int(input("Opção inválida, digite uma opção válida: "))
                if opcao_tabuleiro == 2:
                    self.limpar_tela()
                    print(self._opcoes_tabuleiro())
                    quantidade_embaralhamento = int(input("Digite a quantidade de vezes que o tabuleiro deverá ser embaralhado: "))
                    self.opcoes_selecionadas["Op1"] = [opcao_tabuleiro, quantidade_embaralhamento]
                elif opcao_tabuleiro != 3:
                    self.opcoes_selecionadas["Op1"] = [opcao_tabuleiro, 0]
            elif opcao == 2:
                self.limpar_tela()
                print(self._montar_opcoes())
                if not self.opcoes_selecionadas["Op2"]:
                    print("O programa não utilizará uma função heurística na resolução do jogo.\nAguarde...")
                    self.opcoes_selecionadas["Op2"] = True
                else:
                    print("O programa utilizará uma função heurística na resolução do jogo.\nAguarde...")
                    self.opcoes_selecionadas["Op2"] = False
                time.sleep(3)
            elif opcao == 3:
                self.limpar_tela()
                print(self._montar_opcoes())
                self.opcoes_selecionadas["Op3"] = float(input("Digite o tempo máximo para resolução do jogo (em segundos): "))
            else:
                self.limpar_tela()
                print(self._montar_opcoes())
                self.opcoes_selecionadas["Op4"] = int(input("Digite o número máximo de movimentações permitidas: "))


def main():
    try:
        continuar_resolvendo = True
        while continuar_resolvendo:
            iu = InferfaceUsuario()
            iu.interface_escolhas()
            qc = QuebraCabeca(iu.opcoes_selecionadas["Op1"])
            if iu.opcoes_selecionadas["Op2"]:
                solucionador = BuscaCustoUniforme(qc.tabuleiro, iu.opcoes_selecionadas["Op3"], iu.opcoes_selecionadas["Op4"])
            elif (iu.opcoes_selecionadas["Op1"][0] == 2) and (iu.opcoes_selecionadas["Op3"] > 50) and (iu.opcoes_selecionadas["Op4"] > 30):
                solucionador = BuscaCustoUniforme(qc.tabuleiro, iu.opcoes_selecionadas["Op3"], iu.opcoes_selecionadas["Op4"])
            else:
                solucionador = AEstrela(qc.tabuleiro, iu.opcoes_selecionadas["Op3"], iu.opcoes_selecionadas["Op4"])
            iu.limpar_tela()
            print("Resolvendo utilizando o método: {:s}\nPor favor aguarde...".format(solucionador.nome))
            cod, passos = solucionador.buscar_solucao()
            if cod == "ERRO":
                print("\nEssa instância do jogo não possui solução.\n")
            elif cod == "TEMP_MAX":
                conf_inicial = passos.pop()
                tabuleiro_inicial = qc.montar_tabuleiro(conf_inicial.tabuleiro)
                iu.limpar_tela()
                print("Tempo máximo estourado, exibindo até onde foi possível resolver.\n")
                print("Quebra-cabeça parcialmente resolvido utilizando o método: {:s}".format(solucionador.nome))
                print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(1, tabuleiro_inicial, ('#' * 13)))
                input("Pressione ENTER para continuar.\n")
                cont = 2
                while passos:
                    iu.limpar_tela()
                    print("Tempo máximo estourado, exibindo até onde foi possível resolver.\n")
                    print("Quebra-cabeça parcialmente resolvido utilizando o método: {:s}".format(solucionador.nome))
                    print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                    temp = passos.pop()
                    print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(cont, qc.montar_tabuleiro(temp.tabuleiro), ('#' * 13)))
                    input("Pressione ENTER para continuar.\n")
                    cont += 1
            elif cod == "LIM_MAX":
                conf_inicial = passos.pop()
                tabuleiro_inicial = qc.montar_tabuleiro(conf_inicial.tabuleiro)
                iu.limpar_tela()
                print("Limite máximo de movimentações estourado, exibindo até onde foi possível resolver.\n")
                print("Quebra-cabeça parcialmente resolvido utilizando o método: {:s}".format(solucionador.nome))
                print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(1, tabuleiro_inicial, ('#' * 13)))
                input("Pressione ENTER para continuar.\n")
                cont = 2
                while passos:
                    iu.limpar_tela()
                    print("Limite máximo de movimentações estourado, exibindo até onde foi possível resolver.\n")
                    print("Quebra-cabeça parcialmente resolvido utilizando o método: {:s}".format(solucionador.nome))
                    print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                    temp = passos.pop()
                    print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(cont, qc.montar_tabuleiro(temp.tabuleiro), ('#' * 13)))
                    input("Pressione ENTER para continuar.\n")
                    cont += 1
            elif cod == "CONCLUIDO":
                conf_inicial = passos.pop()
                tabuleiro_inicial = qc.montar_tabuleiro(conf_inicial.tabuleiro)
                iu.limpar_tela()
                print("Quebra-cabeça resolvido utilizando o método: {:s}".format(solucionador.nome))
                print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(1, tabuleiro_inicial, ('#' * 13)))
                input("Pressione ENTER para continuar.\n")
                cont = 2
                while passos:
                    iu.limpar_tela()
                    print("Quebra-cabeça resolvido utilizando o método: {:s}".format(solucionador.nome))
                    print("Configuração inicial:\n{:s}\n\n{:s}\n".format(tabuleiro_inicial, ('#' * 13)))
                    temp = passos.pop()
                    print("Configuração {:d}:\n{:s}\n\n{:s}\n".format(cont, qc.montar_tabuleiro(temp.tabuleiro), ('#' * 13)))
                    input("Pressione ENTER para continuar.\n")
                    cont += 1
            resposta = 'inf'
            while resposta != 's' and resposta != 'n':
                resposta = input("Resolver outro quebra cabeça? ('s' ou 'n'): ")
            if resposta == 'n':
                continuar_resolvendo = False
    except KeyboardInterrupt:
        pass
    finally:
        print("\nFechando o jogo...")


if __name__ == "__main__":
    main()
