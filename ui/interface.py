import tkinter as tk
from tkinter import Label, Frame, PhotoImage, Menu

class Interface:
    def __init__(self):
        self.__itens = ["algemas.png"]
        self.__player_icone = "jogador.png"
        self.__root = tk.Tk()
        self.__status_bar = None
        self.__balas = []
        self.__msg = ""

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

    def on_icon_click(self, icon_name):
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
        menu.add_command(label="Add", command=self.atualizar_ui)
        menubar.add_cascade(label="Menu", menu=menu)

    def criar_players(self):
        player_icon = PhotoImage(file=self.player_icone).subsample(8)
        for i, y in enumerate([50, 300]):
            player_frame = Frame(self.root, bg='gray')
            player_frame.place(x=300, y=y, width=200, height=100)
            player_label = Label(player_frame, image=player_icon, bg='gray')
            player_label.image = player_icon
            player_label.bind("<Button-1>", lambda e, name=f"Jogador {i+1}": self.on_icon_click(name))
            player_label.pack()

            health_bar = Frame(player_frame, bg='green', width=100, height=10)
            health_bar.pack()

    def criar_slots(self):
        icons = [PhotoImage(file=item).subsample(15) for item in self.itens]
        positions = [(50, 50), (550, 50), (50, 300), (550, 300)]

        for x, y in positions:
            print(x, y)
            icon_frame = Frame(self.root, bg='gray')
            icon_frame.place(x=x, y=y, width=100, height=100)

            for row in range(2):
                for col in range(2):
                    border = Frame(icon_frame, bg='white', width=45, height=45)
                    border.grid(row=row, column=col, padx=5, pady=5)
                    if len(self.itens) > 0:
                        icon_index = (row * 2 + col) % len(icons)
                        label = Label(border, image=icons[icon_index], bg='white', borderwidth=2, relief="solid")
                        label.image = icons[icon_index]
                        label.bind("<Button-1>", lambda e, name=self.itens[icon_index]: self.nova_msg(name))
                        label.pack()

    def criar_mensagens(self):
        turn_label = Label(self.root, text=self.msg, bg='white', borderwidth=2, relief="solid")
        turn_label.place(x=300, y=200, width=200, height=30)

    def criar_pente_bar(self):
        self.status_bar = Frame(self.root, bg='gray', width=20, height=200)
        self.status_bar.place(x=700, y=150)

        for bala in self.balas:
            color = 'blue' if bala else 'red'
            Label(self.status_bar, bg=color, width=2, height=1, borderwidth=2, relief="solid").pack()

    def conectar(self):
        print("Conectando")

    def desconectar(self):
        print("Desconectando")

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

    def adicionar_itens(self, itens):
        self.itens.extend(itens)
        self.atualizar_ui()


interface = Interface()
interface.criar_ui()


