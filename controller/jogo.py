from model.player_interface import PlayerInterface
from ui.interface import Interface


class JogoController:
    def __init__(self):
        self.__interface = Interface
        self.__player_interface = PlayerInterface

    @property
    def interface(self):
        return self.__interface

    @interface.setter
    def interface(self, interface: Interface):
        self.__interface = interface

    @property
    def player_interface(self):
        return self.__player_interface

    @player_interface.setter
    def player_interface(self, value):
        self.__player_interface = value

    def iniciar(self):
        self.interface = Interface()
        self.partida = PlayerInterface(self.interface)
        self.interface.iniciar_partida_command = self.partida.comecar_nova_partida_command
        self.interface.usar_item_command = self.partida.usar_item_command
        self.interface.criar_ui()
