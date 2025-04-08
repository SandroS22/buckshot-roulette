import tkinter as tk
from tkinter import Label, Frame, PhotoImage, Menu


class Interface:
    def __init__(self):
        self.__itens = []
        self.__player_icone = "ui/jogador.png"
        self.__root = tk.Tk()
        self.__status_bar = None
        self.__balas = []
        self.__msg = ""
        self.__itens_player =[]
        self.__itens_oponente = []
        self.__vida_player = 6
        self.__vida_oponente = 6
        self.__conectar = None
        self.__desconectar = None

    @property
    def itens(self):
        return self.__itens

    @itens.setter
    def itens(self, itens):
        self.__itens = itens

    @property
    def player_icone(self):
        return self.__player_icone

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        self.__root = value

    @property
    def status_bar(self):
        return self.__status_bar

    @status_bar.setter
    def status_bar(self, value):
        self.__status_bar = value

    @property
    def balas(self):
        return self.__balas

    @balas.setter
    def balas(self, value):
        self.__balas = value

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, value):
        self.__msg = value

    @property
    def itens_player(self):
        return self.__itens_player

    @itens_player.setter
    def itens_player(self, value):
        self.__itens_player = value

    @property
    def itens_oponente(self):
        return self.__itens_oponente

    @itens_oponente.setter
    def itens_oponente(self, value):
        self.__itens_oponente = value

    @property
    def vida_player(self):
        return self.__vida_player

    @vida_player.setter
    def vida_player(self, value):
        self.__vida_player = value

    @property
    def vida_oponente(self):
        return self.__vida_oponente

    @vida_oponente.setter
    def vida_oponente(self, value):
        self.__vida_oponente = value


    @property
    def conectar(self):
        return self.__conectar

    @conectar.setter
    def conectar(self, value):
        self.__conectar = value

    @property
    def desconectar(self):
        return self.__desconectar

    @desconectar.setter
    def desconectar(self, value):
        self.__desconectar = value

    def on_icon_click(self, icon_name):
        if icon_name == "Jogador 0":
            icon_name = "Oponente"
        if icon_name == "Jogador 1":
            icon_name = "Player"
        print(f"Ícone clicado: {icon_name}")

    def criar_ui(self):
        self.root.title("Buckshot Roulette")
        self.root.geometry("800x450")
        self.root.configure(bg="gray")

        # Menu
        self.criar_menu()

        # Área dos jogadores
        self.criar_players()

        # Indicador de vez
        self.criar_mensagens()

        # Slots
        self.criar_slots()

        # Barra lateral de status
        self.criar_pente_bar()

        self.root.mainloop()

    def criar_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menu = Menu(menubar, tearoff=False)
        menu.add_command(label="Conectar", command=self.conectar)
        menu.add_command(label="Desconectar", command=self.desconectar)
        menubar.add_cascade(label="Menu", menu=menu)

    def criar_players(self):
        player_icon = PhotoImage(file=self.player_icone).subsample(8)

        for i, y in enumerate([50, 300]):
            # Criar o frame do jogador
            player_frame = Frame(self.root, bg='gray')
            player_frame.place(x=300, y=y, width=200, height=100)

            # Ícone do jogador
            player_label = Label(player_frame, image=player_icon, bg='gray')
            player_label.image = player_icon  # Evita que o garbage collector remova a imagem
            player_label.bind("<Button-1>", lambda e, name=f"Jogador {i}": self.on_icon_click(name))
            player_label.pack()

            # Criar frame para a barra de vida
            health_bar_frame = Frame(player_frame, bg='black')
            health_bar_frame.pack(pady=5)

            # Criar vidas dentro da barra
            if y == 50:
                for vida in range(self.vida_oponente):
                    vida_frame = Frame(health_bar_frame, bg='green', width=10, height=10)
                    vida_frame.grid(row=0, column=vida, padx=2, pady=2)
            if y == 300:
                for vida in range(self.vida_player):
                    vida_frame = Frame(health_bar_frame, bg='green', width=10, height=10)
                    vida_frame.grid(row=0, column=vida, padx=2, pady=2)

    def criar_slots(self):
        # Criar iteradores compartilhados
        icon_iter_cima = iter([PhotoImage(file=item).subsample(15) for item in self.itens_oponente])
        item_iter_cima = iter(self.itens_oponente)

        icon_iter_baixo = iter([PhotoImage(file=item).subsample(15) for item in self.itens_player])
        item_iter_baixo = iter(self.itens_player)

        # Criar os quadrantes de cima compartilhando os iteradores
        self.criar_quadrante(50, 50, icon_iter_cima, item_iter_cima)
        self.criar_quadrante(600, 50, icon_iter_cima, item_iter_cima)

        # Criar os quadrantes de baixo compartilhando os iteradores
        self.criar_quadrante(50, 300, icon_iter_baixo, item_iter_baixo)
        self.criar_quadrante(600, 300, icon_iter_baixo, item_iter_baixo)

    def criar_quadrante(self, x_base, y_base, icon_iter, item_iter):
        for row in range(2):
            for col in range(2):
                x = x_base + col * 50
                y = y_base + row * 50
                self.criar_slot(x, y, icon_iter, item_iter)

    def criar_slot(self, x, y, icon_iter, item_iter):
        icone_frame = Frame(self.root, bg='gray')
        icone_frame.place(x=x, y=y, width=50, height=50)

        border = Frame(icone_frame, bg='white', width=80, height=80)
        border.pack(padx=5, pady=5, fill='both', expand=True)

        try:
            icone_imagem = next(icon_iter)
            nome_item = next(item_iter)

            label = Label(border, image=icone_imagem, bg='white', borderwidth=2, relief="solid")
            label.image = icone_imagem
            label.bind("<Button-1>", lambda e, nome=nome_item: self.nova_msg(nome))
            label.pack(fill='both', expand=True)

        except StopIteration:
            empty_label = Label(border, bg='white', borderwidth=2, relief="solid")
            empty_label.pack(fill='both', expand=True)

    def criar_mensagens(self):
        turn_label = Label(self.root, text=self.msg, bg='white', borderwidth=2, relief="solid")
        turn_label.place(x=300, y=200, width=200, height=30)

    def criar_pente_bar(self):
        self.status_bar = Frame(self.root, bg='gray', width=20, height=200)
        self.status_bar.place(x=700, y=150)

        for bala in self.balas:
            color = 'blue' if bala else 'red'
            Label(self.status_bar, bg=color, width=2, height=1, borderwidth=2, relief="solid").pack()

    def atualizar_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Criar componentes
        self.criar_menu()
        self.criar_players()
        self.criar_mensagens()
        self.criar_slots()
        self.criar_pente_bar()

    def nova_msg(self, msg):
        self.msg = msg
        self.atualizar_ui()

    def adicionar_itens(self, itens_player, itens_oponente):
        self.itens_player = itens_player
        self.itens_oponente = itens_oponente
        self.atualizar_ui()

    def alterar_vida(self, vida_player, vida_oponente):
        self.vida_player = vida_player
        self.vida_oponente = vida_oponente
        self.atualizar_ui()
