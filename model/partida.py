from model.arma import Arma
from model.inventario import Inventario

class Partida:
    def __init__(self):
        self.__arma = Arma()
        self.__partida_em_andamento = False
        self.__jogadores = []

    @property
    def arma(self):
        return self.__arma

    @arma.setter
    def arma(self, value):
        self.__arma = value

    @property
    def partida_em_andamento(self):
        return self.__partida_em_andamento

    @partida_em_andamento.setter
    def partida_em_andamento(self, value):
        self.__partida_em_andamento = value

    @property
    def jogadores(self):
        return self.__jogadores

