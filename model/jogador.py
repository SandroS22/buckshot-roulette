class Jogador:
    def __init__(self):
        self.__id_jogador = None
        self.__vida = 6
        self.__is_turno = False
        self.__venceu = False

    @property
    def id_jogador(self):
        return self.__id_jogador

    @id_jogador.setter
    def id(self, value):
        self.__id_jogador = value

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
