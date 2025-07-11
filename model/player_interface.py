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
        self.__sincs_feita = 0
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

    @property
    def sincs_feita(self):
        return self.__sincs_feita

    @sincs_feita.setter
    def sincs_feita(self, value):
        self.__sincs_feita = value

    def checa_ganhador(self):
        vida_player = self.player_local.vida
        vida_oponente = self.player_remoto.vida
        if vida_oponente < 1:
            self.player_local.venceu = True
            self.interface.nova_msg("Voce venceu")
            self.status_partida = "1"
        if vida_player < 1:
            self.player_remoto.venceu = True
            self.interface.nova_msg("Voce perdeu")
            self.status_partida = "1"
        self.atualizar_ui()

    def comecar_nova_partida_command(self):
        self.start_match()

    def set_start(self, start_status):
        players = start_status.get_players()
        self.id_local = start_status.get_local_id()

        self.player_local.id_jogador = players[0][1]
        self.player_remoto.id_jogador = players[1][1]

        if players[0][2] == "1":
            self.status_partida = "3"
            self.player_local.mudar_turno()
            self.interface.nova_msg("Sua vez")
        else:
            self.status_partida = "5"
            self.player_remoto.mudar_turno()
            self.interface.nova_msg("Turno do oponente")

    def start_match(self):
        partida_em_andamento = self.is_partida_em_andamento()
        if not partida_em_andamento:
            start_status = self.dog_server.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()
            players = start_status.get_players()
            if code == "0" or code == "1":
                self.interface.nova_msg(message)
            else:
                inf_player_local = players[0]
                inf_player_remoto = players[1]

                self.player_local = self.player_local.iniciar_player(inf_player_local)
                self.player_remoto = self.player_remoto.iniciar_player(inf_player_remoto)

                if self.player_local.is_turno:
                    self.interface.nova_msg("Sua vez")
                    self.status_partida = "3"
                elif self.player_remoto.is_turno:
                    self.interface.nova_msg("Turno do oponente")
                    self.status_partida = "5"
                self.arma.carregar()
                status = self.get_status_para_outro_jogador()
                self.distribuir_itens()
                self.enviar_sincronizacao(status, False, False)
                self.interface.trocar_visibilidade_pente()
                self.atualizar_ui()
                self.interface.root.update_idletasks()
                self.interface.root.update()
                sleep(5)
                self.interface.trocar_visibilidade_pente()
                self.atualizar_ui()
                self.arma.embaralhar_municao()
                self.enviar_sincronizacao(status, True, False)
                self.interface.msg = ""

    def reiniciar_jogo_command(self):
        self.reiniciar_jogo()


    def reiniciar_jogo(self):
        self.arma = Arma()

        self.player_local.vida = 6
        self.player_local.preso = False
        self.player_local.venceu = False
        self.player_local.inventario.itens = []

        self.player_remoto.vida = 6
        self.player_remoto.preso = False
        self.player_remoto.venceu = False
        self.player_remoto.inventario.itens = []

        if randint(0, 1) == 0:
            self.player_local.is_turno = True
            self.player_remoto.is_turno = False
            self.status_partida = "3"
            self.interface.nova_msg("Sua vez")
        else:
            self.player_local.is_turno = False
            self.player_remoto.is_turno = True
            self.status_partida = "5"
            self.interface.nova_msg("Turno do oponente")

        self.distribuir_itens()
        self.arma.carregar()
        status = self.get_status_para_outro_jogador()
        self.enviar_sincronizacao(status, False, True)
        self.interface.trocar_visibilidade_pente()
        self.atualizar_ui()
        self.interface.root.update_idletasks()
        self.interface.root.update()
        sleep(5)
        self.interface.trocar_visibilidade_pente()
        self.atualizar_ui()
        self.arma.embaralhar_municao()
        self.enviar_sincronizacao(status, True, False)
        self.interface.msg = ""


    def usar_item_command(self, item, dono):
        self.usar_item_e_enviar_jogada(item, dono)

    def usar_item(self, item_escolhido, dono):
        item_formatado = item_escolhido.split('/')[-1].split('.')[0].upper()
        if item_formatado == "SERRA":
            self.arma.serrada = True
        elif item_formatado == "ALGEMAS":
            if dono == "Player":
                self.player_remoto.preso= True
            elif dono == "Oponente":
                self.player_local.preso = True
        elif item_formatado == "LUPA":
            bala = self.arma.municoes[0]
            if bala:
                bala = "verdadeira"
            else:
                bala = "falsa"
            if self.status_partida == "3" or self.status_partida == "4":
                self.interface.nova_msg(f"Bala {bala}")
                self.atualizar_ui()
        elif item_formatado == "CERVEJA":
            vazio = self.arma.is_vazio
            if not vazio:
                bala = self.arma.municoes[0]
                if bala:
                    self.interface.nova_msg("Bala verdadeira removida")
                else:
                    self.interface.nova_msg("Bala falsa removida")
                self.arma.remover_municao()
                self.atualizar_ui()
                if len(self.arma.municoes) < 1:
                    self.arma.is_vazio = True
                vazio = self.arma.is_vazio
                if vazio and dono == "Player":
                    self.arma.carregar()
                    status = self.get_status_para_outro_jogador()
                    self.enviar_sincronizacao(status, False, False)
                    self.interface.trocar_visibilidade_pente()
                    self.atualizar_ui()
                    self.interface.root.update_idletasks()
                    self.interface.root.update()
                    sleep(5)
                    self.interface.trocar_visibilidade_pente()
                    self.atualizar_ui()
                    self.arma.embaralhar_municao()
                    self.enviar_sincronizacao(status, True, False)
        elif item_formatado == "CIGARRO":
            if dono == "Player":
                if self.player_local.vida < 6:
                    self.player_local.vida += 1
            elif dono == "Oponente":
                if self.player_remoto.vida < 6:
                    self.player_remoto.vida += 1

        if dono == "Player":
            item_a_remover = self.player_local.inventario.identificar_item(item_formatado)
            self.player_local.inventario.remover_item(item_a_remover)
        elif dono == "Oponente":
            item_a_remover = self.player_remoto.inventario.identificar_item(item_formatado)
            self.player_remoto.inventario.remover_item(item_a_remover)

        self.atualizar_ui()

    def usar_item_e_enviar_jogada(self, item, dono):
        if (self.status_partida == "3" or self.status_partida == "4") and dono == "Player":
            self.usar_item(item, dono)
            self.status_partida = "4"
            jogada = {"item_usado": item, "dono": "Oponente",
                      "tipo_jogada": "usar_item","match_status": "5"}
            self.dog_server.send_move(jogada)

    def enviar_sincronizacao(self, status_partida, segunda_sinc, reinicio):
        itens_player = []
        itens_oponente = []
        for item in self.player_remoto.inventario.itens:
            itens_player.append(item.tipo.name)
        for item in self.player_local.inventario.itens:
            itens_oponente.append(item.tipo.name)

        primeira_sinc = False
        if not self.sincs_feita > 2:
             self.sincs_feita += 1
        else:
            primeira_sinc = True
        jogada = {"itens_player": itens_player, "itens_oponente": itens_oponente, "primeira_sinc": primeira_sinc,
                  "balas": self.arma.municoes, "match_status": status_partida, "tipo_jogada": "sincronizacao",
                  "segunda_sinc": segunda_sinc, "reinicio": reinicio}
        self.dog_server.send_move(jogada)

    def get_status_para_outro_jogador(self):
        if self.status_partida == "3" or self.status_partida == "4":
            return "5"
        elif self.status_partida == "5":
            return "3"
        return self.status_partida



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
                status = self.get_status_para_outro_jogador()
                self.enviar_sincronizacao(status, False, False)
                self.interface.trocar_visibilidade_pente()
                self.atualizar_ui()
                sleep(5)
                self.interface.trocar_visibilidade_pente()
                self.distribuir_itens()
                self.arma.embaralhar_municao()
                self.enviar_sincronizacao(status, True, False)
        elif tipo_jogada == "sincronizacao":
            if a_move["reinicio"]:
                self.player_local.reiniciar_player()
                self.player_remoto.reiniciar_player()
            self.status_partida = a_move["match_status"]
            if self.status_partida == "3" and a_move["primeira_sinc"] == False:
                self.player_local.mudar_turno()
                if self.player_local.is_turno:
                    self.interface.nova_msg("Sua vez")
            self.player_local.atualizar_itens(a_move["itens_player"])
            self.player_remoto.atualizar_itens(a_move["itens_oponente"])
            self.arma.municoes = a_move["balas"]
            self.arma.is_vazio = False
            if not a_move["segunda_sinc"]:
                self.interface.trocar_visibilidade_pente()
                self.atualizar_ui()
                self.interface.root.update_idletasks()
                self.interface.root.update()
                sleep(5)
                self.interface.trocar_visibilidade_pente()
        self.atualizar_ui()


    def receive_start(self, start_status):
        self.set_start(start_status)
        self.atualizar_ui()
        self.interface.msg = ""

    def is_partida_em_andamento(self):
        if self.status_partida == "3" or self.status_partida == "4" or self.status_partida == "5":
            return True
        return False

    def distribuir_itens(self):
        itens = [TipoItem["ALGEMAS"], TipoItem["CERVEJA"], TipoItem["CIGARRO"], TipoItem["LUPA"], TipoItem["SERRA"]]
        inventario_player_local_cheio = self.player_local.inventario.is_inventario_cheio()
        if not inventario_player_local_cheio:
            total = self.player_local.total_itens()
            max = 8 - total
            if max > 4:
                max = 4
            for _ in range(max):
                index = randint(0, 4)
                self.player_local.inventario.adicionar_item(itens[index])
        inventario_player_remoto_cheio = self.player_remoto.inventario.is_inventario_cheio()
        if not inventario_player_remoto_cheio:
            total = self.player_remoto.total_itens()
            max = 8 - total
            if max > 4:
                max = 4
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
                self.arma.serrada = False
            else:
                if alvo == "Player":
                    self.player_local.vida -= 1
                elif alvo == "Oponente":
                    self.player_remoto.vida -= 1

            remoto_turno_local = self.player_remoto.preso and (self.status_partida == "3" or self.status_partida == "4")
            local_turno_remoto = self.status_partida == "5" and self.player_local.preso
            preso = remoto_turno_local or local_turno_remoto
            if not preso:
                self.player_local.mudar_turno()
                self.player_remoto.mudar_turno()
                if self.status_partida == "3" or self.status_partida == "4":
                    self.interface.nova_msg("Turno do oponente")
                    self.status_partida = "5"
                elif self.status_partida == "5":
                    self.status_partida = "3"
                    self.interface.nova_msg("Sua vez")
            else:
                if self.player_local.preso:
                    self.player_local.preso = False
                elif self.player_remoto.preso:
                    self.player_remoto.preso = False
        else:
            if alvo == "Player":
                self.status_partida = "3"
                self.interface.nova_msg("Sua vez")
            elif alvo == "Oponente":
                self.status_partida = "5"
                self.player_local.mudar_turno()
                self.player_remoto.mudar_turno()
                self.interface.nova_msg("Turno do oponente")
        print(self.arma.municoes)
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
        if self.is_partida_em_andamento():
            self.status_partida = "6"
            self.player_local.venceu = True
            self.interface.nova_msg("O oponente desconectou. Voce venceu!")
        else:
            self.interface.nova_msg("Oponente Desconectou")

    def atualizar_ui(self):
        self.interface.balas = self.arma.municoes
        self.interface.vida_oponente = self.player_remoto.vida
        self.interface.vida_player = self.player_local.vida
        self.interface.itens_oponente = self.formatar_itens_para_icone(self.player_remoto.inventario.itens)
        self.interface.itens_player = self.formatar_itens_para_icone(self.player_local.inventario.itens)
        self.interface.vida_oponente = self.player_remoto.vida
        self.interface.vida_player = self.player_local.vida
        self.interface.atualizar_ui()
