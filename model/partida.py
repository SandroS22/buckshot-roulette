from time import sleep, time
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from model.arma import Arma
from model.jogador import Jogador
from ui.interface import Interface
from tkinter import simpledialog, messagebox


class Partida(DogPlayerInterface):
    def __init__(self, interface: Interface):
        super().__init__()
        self.__arma = Arma()
        self.__status_partida = 1
        self.__player_local = Jogador()
        self.__player_remoto = Jogador()
        self.__interface = interface
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.__dog_server = DogActor()
        message = self.__dog_server.initialize(player_name, self)
        messagebox.showinfo(message=message)
        self.__interface.atualizar_ui()



    @property
    def arma(self):
        return self.__arma

    @arma.setter
    def arma(self, value):
        self.__arma = value

    @property
    def status_partida(self):
        return self.__status_partida

    @status_partida.setter
    def status_partida(self, value):
        self.__status_partida = value

    @property
    def player_local(self):
        return self.__player_local

    @player_local.setter
    def player_local(self, value):
        self.__player_local = value

    @property
    def player_remoto(self):
        return self.__player_remoto

    @player_remoto.setter
    def player_remoto(self, value):
        self.__player_remoto = value

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
        if self.player_local.venceu:
            return self.player_local.nome
        elif self.player_remoto.venceu:
            return self.player_remoto.nome
        return None

    def desconectar(self):
        pass

    def comecar_nova_partida_command(self):
        if self.is_partida_em_andamento():
            return

        start_status = self.dog_server.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()
 
        if code == "0" or code == "1":
            self.interface.nova_msg(message)
        else:
            self.comecar_partida(start_status.get_players())
            self.interface.atualizar_ui()

    def comecar_partida(self, players):
        player_local = players[0]
        player_remoto = players[1]
        print(players)

        self.player_local = self.player_local.iniciar_player(player_local)
        self.player_remoto = self.player_remoto.iniciar_player(player_remoto)
        
        if self.player_local.is_turno:
            self.status_partida = "3"
        elif self.player_remoto.is_turno:
            self.status_partida = "5"

    def usar_item_command(self, item):
        print(item)
        

    def receber_jogada(self, jogada):
        pass


    def is_partida_em_andamento(self):
        if self.status_partida == "3" or self.status_partida == "4" or self.status_partida == "5":
            return True
        return False

