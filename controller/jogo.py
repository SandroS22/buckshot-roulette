from model.player_interface import PlayerInterface
from ui.interface import Interface


class Jogo:
    def __init__(self):
        self.__interface = Interface()
        self.__player_interface = PlayerInterface(self.__interface)

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
        self.interface.iniciar_partida_command = self.player_interface.comecar_nova_partida_command
        self.interface.usar_item_command = self.player_interface.usar_item_command
        self.interface.reiniciar_jogo_command = self.player_interface.reiniciar_jogo_command
        self.interface.atirar_command = self.player_interface.atirar_e_enviar_jogada
        self.interface.criar_ui()
