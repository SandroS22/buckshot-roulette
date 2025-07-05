from random import randint
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
        vida_player = self.player_local.vida
        vida_oponente = self.player_remoto.vida
        if vida_oponente < 1:
            self.player_local.venceu = True
            self.interface.nova_msg("Voce venceu")
            self.status_partida = "1"
        if vida_player < 1:
            self.player_remoto.venceu = True
            self.interface.nova_msg("Vitoria do oponente")
            self.status_partida = "1"
        self.atualizar_ui()

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
            self.atualizar_ui()
        else:
            self.start_match(start_status.get_players())
            self.interface.trocar_visibilidade_pente()
            self.atualizar_ui()

    def start_match(self, players):
        # inicializar arma aqui
        self.atualizar_ui()
        player_local = players[0]
        player_remoto = players[1]

        self.player_local = self.player_local.iniciar_player(player_local)
        self.player_remoto = self.player_remoto.iniciar_player(player_remoto)
        print("Player local: ", self.player_local.is_turno)
        print("Player remoto: ", self.player_remoto.is_turno)

        self.distribuir_itens()
        if self.player_local.is_turno:
            self.status_partida = "3"
        elif self.player_remoto.is_turno:
            self.status_partida = "5"
        self.arma.carregar()
        status = self.get_turno_para_player_remoto()
        self.enviar_sincronizacao(status)
        self.arma.embaralhar_municao()
        self.enviar_sincronizacao(status)

    def get_turno_para_player_remoto(self):
        status = ""
        if self.player_local.is_turno:
            status = "5"
        elif self.player_remoto.is_turno:
            status = "3"
        return status

    def usar_item_command(self, item, dono):
        print(self.status_partida)
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
        self.atualizar_ui()

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
            jogada = {"item_usado": item, "dono": "Oponente",
                      "tipo_jogada": "usar_item","match_status": "5"}
            self.dog_server.send_move(jogada)

    def enviar_sincronizacao(self, status_partida):
        itens_player = []
        itens_oponente = []
        for item in self.player_remoto.inventario.itens:
            itens_player.append(item.tipo.name)
        for item in self.player_local.inventario.itens:
            itens_oponente.append(item.tipo.name)

        jogada = {"itens_player": itens_player, "itens_oponente": itens_oponente,
                  "balas": self.arma.municoes, "match_status": status_partida, "tipo_jogada": "sincronizacao"}
        self.dog_server.send_move(jogada)


    def reiniciar_jogo_command(self):
        if not self.is_partida_em_andamento():
            self.reiniciar_jogo()
        else:
            self.interface.nova_msg("Nao existe partida em andamento")
        self.atualizar_ui()

    def reiniciar_jogo(self):
        self.arma = Arma()
        self.player_local = Jogador()
        self.player_remoto = Jogador()
        self.status_partida = "0"
        self.interface.reiniciar_interface()

    def receive_move(self, a_move: dict):
        tipo_jogada = a_move["tipo_jogada"]
        if tipo_jogada == "usar_item":
            self.status_partida = a_move["match_status"]
            self.usar_item(a_move["item_usado"], a_move["dono"])
        elif tipo_jogada == "atirar":
            self.atirar(a_move["alvo"])
            vazio = self.arma.is_vazio
            if vazio:
                self.arma.carregar()
                status_partida = self.get_turno_para_player_remoto()
                self.enviar_sincronizacao(status_partida)
                #self.interface.trocar_visibilidade_pente()
                # sleep(5)
                self.atualizar_ui()
                #self.interface.trocar_visibilidade_pente()
                self.distribuir_itens()
                self.arma.embaralhar_municao()
                self.enviar_sincronizacao(status_partida)
        elif tipo_jogada == "sincronizacao":
            self.status_partida = a_move["match_status"]
            if self.status_partida == "3":
                self.player_local.mudar_turno()
            self.player_local.atualizar_itens(a_move["itens_player"])
            self.player_remoto.atualizar_itens(a_move["itens_oponente"])
            self.arma.municoes = a_move["balas"]
            self.arma.is_vazio = False
            #self.interface.trocar_visibilidade_pente()
            self.atualizar_ui()
            # sleep(5)
            #self.interface.trocar_visibilidade_pente()
        self.atualizar_ui()


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
        self.set_start(start_status)
        self.atualizar_ui()

    def is_partida_em_andamento(self):
        if self.status_partida == "3" or self.status_partida == "4" or self.status_partida == "5":
            return True
        return False

    def distribuir_itens(self):
        itens = [TipoItem["ALGEMAS"], TipoItem["CERVEJA"], TipoItem["CIGARRO"], TipoItem["LUPA"], TipoItem["SERRA"]]
        inventario_player_local_cheio = self.player_local.inventario.is_inventario_cheio()
        inventario_player_remoto_cheio = self.player_remoto.inventario.is_inventario_cheio()
        if not inventario_player_local_cheio:
            total = self.player_local.total_itens()
            max = 8 - total
            for _ in range(max):
                index = randint(0, 4)
                self.player_local.inventario.adicionar_item(itens[index])
        if not inventario_player_remoto_cheio:
            total = self.player_remoto.total_itens()
            max = 8 - total
            for _ in range(max):
                index = randint(0, 4)
                self.player_remoto.inventario.adicionar_item(itens[index])

    def formatar_itens_para_icone(self, itens):
        itens_formatado = []
        for item in itens:
            itens_formatado.append(item.icone())
        return itens_formatado

    def atirar(self, alvo):
        tipo_bala = self.arma.atirar()
        if tipo_bala:
            if self.arma.serrada:
                if alvo == "Player":
                    self.player_local.vida -= 2
                elif alvo == "Oponente":
                    self.player_remoto.vida -= 2
            else:
                if alvo == "Player":
                    self.player_local.vida -= 1
                elif alvo == "Oponente":
                    self.player_remoto.vida -= 1
            preso = self.player_remoto.preso
            if not preso:
                self.player_local.mudar_turno()
                self.player_remoto.mudar_turno()
        else:
            if alvo == "Player":
                self.status_partida = "3"
            elif alvo == "Oponente":
                self.status_partida = "5"
                self.player_local.mudar_turno()
                self.player_remoto.mudar_turno()
        self.checa_ganhador()

    def atirar_e_enviar_jogada(self, alvo):
        if self.status_partida == "3" or self.status_partida == "4":
            self.atirar(alvo)
            if alvo == "Player":
                alvo = "Oponente"
            elif alvo == "Oponente":
                alvo = "Player"
            self.dog_server.send_move({"match_status": self.status_partida, "tipo_jogada": "atirar", "alvo": alvo})

    def receive_withdrawal_notification(self):
        self.interface.nova_msg("Oponente Desconectou")
        self.atualizar_ui()

    def atualizar_ui(self):
        #TODO: remove a linha debaixo
        self.interface.status = self.status_partida
        self.interface.balas = self.arma.municoes
        self.interface.vida_oponente = self.player_remoto.vida
        self.interface.vida_player = self.player_local.vida
        self.interface.itens_oponente = self.formatar_itens_para_icone(self.player_remoto.inventario.itens)
        self.interface.itens_player = self.formatar_itens_para_icone(self.player_local.inventario.itens)
        self.interface.vida_oponente = self.player_remoto.vida
        self.interface.vida_player = self.player_local.vida
        self.interface.atualizar_ui()
        

