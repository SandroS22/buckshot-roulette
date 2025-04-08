from model.partida import Partida

from ui.interface import Interface


class JogoController:
    def __init__(self):
        self.__interface = None
        self.__partida = None

    @property
    def interface(self):
        return self.__interface

    @interface.setter
    def interface(self, interface: Interface):
        self.__interface = interface

    @property
    def partida(self):
        return self.__partida

    @partida.setter
    def partida(self, value):
        self.__partida = value

    def iniciar(self):
        self.interface = Interface()
        self.partida = Partida(self.interface)
        self.interface.conectar = self.partida.comecar_nova_partida
        self.interface.desconectar = self.partida.comecar_nova_partida
        self.interface.criar_ui()
