from dog.dog_actor import DogActor
from model.arma import Arma
from ui.interface import Interface


class Partida:
    def __init__(self, interface: Interface):
        self.__arma = Arma()
        self.__partida_em_andamento = False
        self.__jogadores = []
        self.__dog_server = DogActor()
        self.__interface = interface

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

    @property
    def dog_server(self):
        return self.__dog_server

    @dog_server.setter
    def dog_server(self, value):
        self.__dog_server = value

    @property
    def interface(self):
        return self.__interface

    @interface.setter
    def interface(self, value):
        self.__interface = value


    def checa_ganhador(self):
        if self.partida_em_andamento:
            for jogador in self.jogadores:
                if jogador.venceu:
                    return jogador
        return False

    def comecar_nova_partida(self):
        if self.partida_em_andamento:
            return

        start_status = self.dog_server.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            self.interface.nova_msg(message)
        else:
            self.interface.nova_msg(message)

