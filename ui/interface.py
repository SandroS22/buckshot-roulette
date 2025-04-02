import tkinter as tk
from tkinter import Label, Frame, PhotoImage, Menu

class Interface:
    def __init__(self):
        self.__icones = ["lupa.png", "algemas.png", "cerveja.png", "cigarro.png", "serra.png"]
        self.__player_icone = "jogador.png"
        self.__root = tk.Tk()
        self.status_bar = None
        self.numeroBalas = []

    @property
    def icones(self):
        return self.__icones

    @property
    def player_icone(self):
        return self.__player_icone

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        self._root = value

    def on_icon_click(self, icon_name):
        print(f"Ícone clicado: {icon_name}")

    def criar_ui(self):
        self.root.title("Buckshot Roulette")
        self.root.geometry("800x450")
        self.root.configure(bg="gray")

        # Menu
        self.criarMenu()

        # Área dos jogadores
        self.criarPlayers()

        # Indicador de vez
        self.criarMensagens("ALSFKJ")

        # Slots
        self.criarSlots()

        # Barra lateral de status
        self.criarPenteBar()

        self.atualizar_ui()

        self.root.mainloop()

    def criarMenu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menu = Menu(menubar, tearoff=False)
        menu.add_command(label="Conectar", command=self.conectar)
        menu.add_command(label="Desconectar", command=self.desconectar)
        menu.add_command(label="Add", command=self.atualizar_ui)

        menubar.add_cascade(label="Menu", menu=menu)

    def criarPlayers(self):
        player_icon = PhotoImage(file=self.player_icone).subsample(8, 8)
        for i, y in enumerate([50, 300]):
            player_frame = Frame(self.root, bg='gray')
            player_frame.place(x=300, y=y, width=200, height=100)
            player_label = Label(player_frame, image=player_icon, bg='gray')
            player_label.image = player_icon
            player_label.bind("<Button-1>", lambda e, name=f"Jogador {i+1}": self.on_icon_click(name))
            player_label.pack()

            health_bar = Frame(player_frame, bg='green', width=100, height=10)
            health_bar.pack()

    def criarSlots(self):
        icon_paths = self.icones
        icons = [PhotoImage(file=path).subsample(15, 15) for path in icon_paths]
        positions = [(50, 50), (550, 50), (50, 300), (550, 300)]

        for x, y in positions:
            icon_frame = Frame(self.root, bg='gray')
            icon_frame.place(x=x, y=y, width=100, height=100)

            for row in range(2):
                for col in range(2):
                    border = Frame(icon_frame, bg='black', width=45, height=45)
                    border.grid(row=row, column=col, padx=5, pady=5)
                    icon_index = (row * 2 + col) % len(icons)
                    label = Label(border, image=icons[icon_index], bg='white', borderwidth=2, relief="solid")
                    label.image = icons[icon_index]
                    label.bind("<Button-1>", lambda e, name=icon_paths[icon_index]: self.on_icon_click(name))
                    label.pack()

    def criarMensagens(self, msg):
        turn_label = Label(self.root, text=msg, bg='white', borderwidth=2, relief="solid")
        turn_label.place(x=300, y=200, width=200, height=30)

    def criarPenteBar(self):
        if self.status_bar:
            self.status_bar.destroy()  # Remove a barra anterior para recriar

        self.status_bar = Frame(self.root, bg='black', width=20, height=200)
        self.status_bar.place(x=700, y=150)

        for bala in self.numeroBalas:
            color = 'blue' if bala else 'red'
            Label(self.status_bar, bg=color, width=2, height=1, borderwidth=2, relief="solid").pack()

    def conectar(self):
        print("Conectando")

    def desconectar(self):
        print("Desconectando")

    def atualizar_ui(self):
        """Recria toda a interface"""
        # Remove todos os widgets da tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Criar menu
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menu = Menu(menubar, tearoff=False)
        menu.add_command(label="Conectar", command=self.conectar)
        menu.add_command(label="Desconectar", command=self.desconectar)
        menu.add_command(label="Add", command=self.atualizar_ui)  # Chama o updateGui no clique
        menubar.add_cascade(label="Menu", menu=menu)

        # Criar componentes
        self.criarPlayers()
        self.criarMensagens("LASKDJ")
        self.criarSlots()
        self.criarPenteBar()
        self.numeroBalas.append(True)

Interface().criar_ui()
