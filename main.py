import random
from functools import total_ordering
from collections import Counter


@total_ordering
class Jogador:

    def __init__(self, saldo=300):
        self.saldo = saldo
        self.posicao_tabuleiro = 0
        self.ativo = True
        self.propriedades = list()

    def __eq__(self, other):
        return self.saldo == other.saldo

    def __lt__(self, other):
        return self.saldo < other.saldo

    def add_propriedade(self, propriedade):
        self.propriedades.append(propriedade)

    def pagar_aluguel(self, jogador, propriedade):
        self.saldo -= propriedade.valor_de_aluguel
        jogador.saldo += propriedade.valor_de_aluguel

    def comprar(self, propriedade, estrategia):
        if estrategia:
            self.saldo -= propriedade.custo_de_venda
            propriedade.proprietario = self
            self.add_propriedade(propriedade=propriedade)
        elif propriedade.proprietario is not None:
            self.pagar_aluguel(jogador=propriedade.proprietario, propriedade=propriedade)

        if self.saldo < 0:
            self.ativo = False
            for propriedade in self.propriedades:
                propriedade.proprietario = None
            self.propriedades = list()

    def mover(self, num):
        if num + self.posicao_tabuleiro > 19:
            self.posicao_tabuleiro = self.posicao_tabuleiro + num - 20
            self.saldo += 100
        else:
            self.posicao_tabuleiro += num


class JogadorImpulsivo(Jogador):

    def comprar_propriedade(self, propriedade):
        estrategia = propriedade.proprietario is None and self.saldo >= propriedade.custo_de_venda
        self.comprar(propriedade=propriedade, estrategia=estrategia)

    def __str__(self):
        return f'Impulsivo'


class JogadorExigente(Jogador):

    def comprar_propriedade(self, propriedade):
        estrategia = (propriedade.proprietario is None
                      and self.saldo >= propriedade.custo_de_venda
                      and propriedade.valor_de_aluguel > 50)
        self.comprar(propriedade=propriedade, estrategia=estrategia)

    def __str__(self):
        return f'Exigente'


class JogadorCauteloso(Jogador):

    def comprar_propriedade(self, propriedade):
        estrategia = (propriedade.proprietario is None
                      and self.saldo - 80 >= propriedade.custo_de_venda)
        self.comprar(propriedade=propriedade, estrategia=estrategia)

    def __str__(self):
        return f'Cauteloso'


class JogadorAleatorio(Jogador):

    def comprar_propriedade(self, propriedade):
        estrategia = (propriedade.proprietario is None
                      and self.saldo >= propriedade.custo_de_venda
                      and bool(random.randrange(2)))
        self.comprar(propriedade=propriedade, estrategia=estrategia)

    def __str__(self):
        return f'Aleatório'


class Propriedade:

    def __init__(self, custo_de_venda, valor_de_aluguel):
        self.custo_de_venda = custo_de_venda
        self.valor_de_aluguel = valor_de_aluguel
        self.proprietario = None


class Tabuleiro:

    def __init__(self, tamanho_tabuleiro):
        self.tablero = [Propriedade(custo_de_venda=(random.randint(70, 280)),
                                    valor_de_aluguel=(random.randint(10, 100)))
                        for _ in range(tamanho_tabuleiro)]

    def get_propriedade(self, posicao_tabuleiro):
        return self.tablero[posicao_tabuleiro]


def partida():
    jogadores = [
        JogadorImpulsivo(),
        JogadorExigente(),
        JogadorCauteloso(),
        JogadorAleatorio()
    ]
    random.shuffle(jogadores, random.random)

    tabuleiro = Tabuleiro(tamanho_tabuleiro=20)

    rodadas = 0
    while rodadas < 1000 and len(jogadores) > 1:
        for jogador in jogadores:
            jogador.mover(num=random.randint(1, 6))
            posicao_tabuleiro = jogador.posicao_tabuleiro
            propriedade = tabuleiro.get_propriedade(posicao_tabuleiro=posicao_tabuleiro)
            jogador.comprar_propriedade(propriedade=propriedade)

            if not jogador.ativo:
                jogadores.remove(jogador)

        rodadas += 1

    if len(jogadores) == 1:
        ganhador = jogadores[0]
    else:
        ganhador = max(jogadores)

    return rodadas, str(ganhador)


if __name__ == '__main__':
    rodadas = list()
    jogadores = list()
    for i in range(300):
        cant_rodadas, ganhador = partida()
        rodadas.append(cant_rodadas)
        jogadores.append(ganhador)

    print(f'Terminam por time-out {rodadas.count(1000)} partidas.')
    print(f'Uma partida demora em média {(sum(rodadas) / len(rodadas)):.2f} turnos.')
    word_counts = Counter(jogadores)
    exigente = word_counts['Exigente']
    cauteloso = word_counts['Cauteloso']
    aleatorio = word_counts['Aleatório']
    impulsivo = word_counts['Impulsivo']
    print(f'Porcentagem de vitórias do Exigente: {(exigente / len(jogadores) * 100):.2f} %.')
    print(f'Porcentagem de vitórias do Cauteloso: {(cauteloso / len(jogadores) * 100):.2f} %.')
    print(f'Porcentagem de vitórias do Aleatório: {(aleatorio / len(jogadores) * 100):.2f} %.')
    print(f'Porcentagem de vitórias do Impulsivo: {(impulsivo / len(jogadores) * 100):.2f} %.')
    vencedor, cantidad = word_counts.most_common(1)[0]
    print(f'O comportamento que mais vence é {vencedor} com {cantidad} vitórias.')