from random import randint
from time import sleep
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from model.arma import Arma
from model.jogador import Jogador
from model.tipoItem import TipoItem
from ui.interface import Interface
from tkinter import simpledialog, messagebox


class PlayerInterface(DogPlayerInterface):
    def __init__(self, interface: Interface):
        super().__init__()
        self.__id_local = None
        self.__arma = Arma()
        self.__status_partida = "1"
        self.__player_local = Jogador()
        self.__player_remoto = Jogador()
        self.__interface = interface
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.__dog_server = DogActor()
        message = self.__dog_server.initialize(player_name, self)
        messagebox.showinfo(message=message)

    @property
    def id_local(self):
        return self.__id_local

    @id_local.setter
    def id_local(self, value):
        self.__id_local = value

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
            self.interface.atualizar_ui()
        else:
            self.interface.reiniciar_interface()
            self.start_match(start_status.get_players())
            self.arma.carregar()
            self.interface.balas = self.arma.municoes
            self.interface.trocar_visibilidade_pente()
            self.interface.atualizar_ui()

    def start_match(self, players):
        # inicializar arma aqui
        self.interface.atualizar_ui()
        player_local = players[0]
        player_remoto = players[1]

        self.player_local = self.player_local.iniciar_player(player_local)
        self.player_remoto = self.player_remoto.iniciar_player(player_remoto)

        self.distribuir_itens()
        if self.player_local.is_turno:
            self.status_partida = "3"
        elif self.player_remoto.is_turno:
            self.status_partida = "5"

    def usar_item_command(self, item, dono):
        self.usar_item_e_enviar_jogada(item, dono)

    def usar_item(self, item, dono):
        if dono == "Player":
            item = item.split('/')[-1].split('.')[0].upper()
            item = self.player_local.inventario.identificar_item(item)
            self.player_local.inventario.remover_item(item)
        elif dono == "Oponente" and self.status_partida != "5":
            item = item.split('/')[-1].split('.')[0].upper()
            item = self.player_remoto.inventario.identificar_item(item)
            self.player_remoto.inventario.remover_item(item)

        itens_player_formatado = self.formatar_itens_para_icone(self.player_local.inventario.itens)
        itens_oponente_formatado = self.formatar_itens_para_icone(self.player_remoto.inventario.itens)
        self.interface.adicionar_itens(itens_player_formatado, itens_oponente_formatado)
        self.interface.atualizar_ui()

    def usar_item_e_enviar_jogada(self, item, dono):
        if (self.status_partida == "3" or self.status_partida == "4") and dono == "Player":
            itens_player = []
            itens_oponente = []
            self.usar_item(item, dono)
            self.status_partida = "4"
            for item_inventario in self.player_remoto.inventario.itens:
                itens_player.append(item_inventario.tipo.name)
            for item_inventario in self.player_local.inventario.itens:
                itens_oponente.append(item_inventario.tipo.name)
            jogada = {"item_usado": item, "dono": "Oponente", "itens_player": itens_player,
                      "itens_oponente": itens_oponente, "balas": self.arma.municoes, 
                      "tipo_jogada": "usar_item","match_status": "next"}
            self.dog_server.send_move(jogada)

    def enviar_sincronizacao(self):
        itens_player = []
        itens_oponente = []
        for item in self.player_remoto.inventario.itens:
            itens_player.append(item.tipo.name)
        for item in self.player_local.inventario.itens:
            itens_oponente.append(item.tipo.name)


        jogada = {"itens_player": itens_player, "itens_oponente": itens_oponente,
                  "balas": self.arma.municoes, "match_status": self.status_partida}
        self.dog_server.send_move(jogada)


    def reiniciar_jogo_command(self):
        if not self.is_partida_em_andamento():
            self.reiniciar_jogo()
        else:
            self.interface.nova_msg("Nao existe partida em andamento")
        self.interface.atualizar_ui()

    def reiniciar_jogo(self):
        self.arma = Arma()
        self.player_local = Jogador()
        self.player_remoto = Jogador()
        self.status_partida = "1"
        self.interface.reiniciar_interface()

    def receive_move(self, a_move: dict):
        self.status_partida = a_move["match_status"]
        self.arma.municoes = a_move["balas"]
        if any("itens" in chave for chave in a_move):
            self.player_local.inventario.itens = []
            self.player_remoto.inventario.itens = []
            for item in a_move["itens_player"]:
                self.player_local.inventario.adicionar_item(TipoItem[item])
            for item in a_move["itens_oponente"]:
                self.player_remoto.inventario.adicionar_item(TipoItem[item])
            self.adicionar_itens_na_interface()
            self.interface.atualizar_ui()

    def set_start(self, start_status):
        players = start_status.get_players()
        self.id_local = start_status.get_local_id()

        self.player_local.id_jogador = players[0][1]
        self.player_remoto.id_jogador = players[1][1]

        if players[0][2] == "1":
            self.status_partida = "3"
            self.player_local.mudar_turno()
        else:
            self.status_partida = "5"
            self.player_remoto.mudar_turno()
        


    def receive_start(self, start_status):
        self.reiniciar_jogo()
        self.set_start(start_status)
        self.interface.atualizar_ui()

    def is_partida_em_andamento(self):
        if self.status_partida == "3" or self.status_partida == "4" or self.status_partida == "5":
            return True
        return False

    def distribuir_itens(self):
        itens = [TipoItem["ALGEMAS"], TipoItem["CERVEJA"], TipoItem["CIGARRO"], TipoItem["LUPA"], TipoItem["SERRA"]]
        for _ in range(4):
            index_player_local = randint(0, 4)
            self.player_local.inventario.adicionar_item(itens[index_player_local])
            index_player_remoto = randint(0, 4)
            self.player_remoto.inventario.adicionar_item(itens[index_player_remoto])
        self.enviar_sincronizacao()
        
        self.adicionar_itens_na_interface()
        self.interface.atualizar_ui()

    def adicionar_itens_na_interface(self):
        itens_player_formatado = self.formatar_itens_para_icone(self.player_local.inventario.itens)
        itens_oponente_formatado = self.formatar_itens_para_icone(self.player_remoto.inventario.itens)
        self.interface.adicionar_itens(itens_player_formatado, itens_oponente_formatado)

    def formatar_itens_para_icone(self, itens):
        itens_formatado = []
        for item in itens:
            itens_formatado.append(item.icone())
        return itens_formatado

    def atirar(self, alvo):
        if self.status_partida == "3" or self.status_partida == "4":
            tipo_bala = self.arma.atirar()
            if tipo_bala and alvo == "Player":
                self.player_local.vida -= 1
                self.interface.nova_msg(f"Player atirou {tipo_bala}")
            self.interface.balas = self.arma.municoes
            self.interface.atualizar_ui()
            if self.arma.is_vazio:
                self.interface.nova_msg("Arma vazia")
            self.player_local.mudar_turno()
            self.player_remoto.mudar_turno()
            self.status_partida = "5"
            self.dog_server.send_move({"balas": self.arma.balas, "match_status": "3"})

    def receive_withdrawal_notification(self):
        self.interface.nova_msg("Oponente Desconectou")
        self.interface.atualizar_ui()
