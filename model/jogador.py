from model import inventario
from model.inventario import Inventario
from model.tipoItem import TipoItem

class Jogador:
    def __init__(self):
        self.__id_jogador = ""
        self.__nome = ""
        self.__vida = 6
        self.__is_turno = False
        self.__venceu = False
        self.__inventario = Inventario()
        self.__preso = False

    @property
    def id_jogador(self):
        return self.__id_jogador

    @id_jogador.setter
    def id_jogador(self, value):
        self.__id_jogador = value

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, value):
        self.__vida = value

    @property
    def is_turno(self):
        return self.__is_turno

    @is_turno.setter
    def is_turno(self, value):
        self.__is_turno = value

    @property
    def venceu(self):
        return self.__venceu

    @venceu.setter
    def venceu(self, value):
        self.__venceu = value


    @property
    def inventario(self):
        return self.__inventario

    @inventario.setter
    def inventario(self, value):
        self.__inventario = value

    @property
    def preso(self):
        return self.__preso

    @preso.setter
    def preso(self, preso):
        self.__preso = preso

    def mudar_turno(self):
        if self.is_turno:
            self.is_turno = False
        elif not self.is_turno:
            self.is_turno = True

    def iniciar_player(self, player):
        ordem_jogador = player[2]
        print("Ordem: ", ordem_jogador)
        novo_jogador = Jogador()

        if str(ordem_jogador) == "1":
            novo_jogador.mudar_turno()

        return novo_jogador

    def identificar_item(self, item):
        item = self.inventario.identificar_item(item)
        return item

    def atualizar_itens(self, itens):
        self.inventario.itens = []
        for item in itens:
            self.inventario.adicionar_item(TipoItem[item])

    def total_itens(self):
        return len(self.inventario.itens)

    def reiniciar_player(self):
        self.inventario = Inventario()
        self.vida = 6
        self.is_turno = False
        self.venceu = False
        self.preso = False

