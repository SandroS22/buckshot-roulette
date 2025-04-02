import tkinter as tk
from tkinter import Label, Frame, PhotoImage, Menu

class Interface:
    def __init__(self):
        self.__icones = ["lupa.png", "algemas.png", "cerveja.png", "cigarro.png", "serra.png"]
        self.__player_icone = "jogador.png"

    @property
    def icones(self):
        return self.__icones

    @property
    def player_icone(self):
        return self.__player_icone

    def on_icon_click(self, icon_name):
        print(f"Ícone clicado: {icon_name}")

    def criar_ui(self):
        root = tk.Tk()
        root.title("Buckshot Roulette")
        root.geometry("800x450")
        root.configure(bg='gray')
        
        # Menu
        menubar = Menu(root)

        root.config(menu=menubar)
        menu = Menu(menubar, tearoff=False)
        menu.add_command(label="Conectar", command=self.conectar)
        menu.add_command(label="Desconectar", command=self.desconectar)

        menubar.add_cascade(label="Menu", menu=menu)
        
        
        # Área dos jogadores
        for i, y in enumerate([50, 300]):
            player_frame = Frame(root, bg='gray')
            player_frame.place(x=300, y=y, width=200, height=100)
            
            player_label = Label(player_frame, image=PhotoImage(file=self.player_icone).subsample(8,8), bg='gray')
            player_label.bind("<Button-1>", lambda e, name=f"Jogador {i+1}": self.on_icon_click(name))
            player_label.pack()
            
            health_bar = Frame(player_frame, bg='green', width=100, height=10)
            health_bar.pack()
        
        # Indicador de vez
        self.criarMensagens(root)

        # Slots
        self.criarSlots(root)

        # Barra lateral de status
        totalBalas = self.getBalas()
        self.criarPenteBar(root, totalBalas)

        root.mainloop()

    def criarSlots(self, root):
        player_icon = PhotoImage(file=self.player_icone).subsample(8, 8)
        for i, y in enumerate([50, 300]):
            player_frame = Frame(root, bg='gray')
            player_frame.place(x=300, y=y, width=200, height=100)
            
            player_label = Label(player_frame, image=player_icon, bg='gray')
            player_label.bind("<Button-1>", lambda e, name=f"Jogador {i+1}": self.on_icon_click(name))
            player_label.pack()
            
            health_bar = Frame(player_frame, bg='green', width=100, height=10)
            health_bar.pack()

        # Indicador de vez
        turn_label = Label(root, text="VEZ DO JOGADOR 1", bg='white')
        turn_label.place(x=300, y=200, width=200, height=30)
        
        # Ícones e botões com imagens PNG redimensionadas em um grid 2x2
        icon_paths = self.icones
        icons = [PhotoImage(file=path).subsample(15, 15) for path in icon_paths]  # Reduz o tamanho
        positions = [(50, 50), (550, 50), (50, 300), (550, 300)]
        
        for x, y in positions:
            icon_frame = Frame(root, bg='gray')
            icon_frame.place(x=x, y=y, width=100, height=100)
            
            for row in range(2):
                for col in range(2):
                    border = Frame(icon_frame, bg='black', width=45, height=45)
                    border.grid(row=row, column=col, padx=5, pady=5)
                    icon_index = (row * 2 + col) % len(icons)
                    label = Label(border, image=icons[icon_index], bg='white')
                    label.bind("<Button-1>", lambda e, name=icon_paths[icon_index]: self.on_icon_click(name))
                    label.pack()

    def criarMensagens(self, root):
        turn_label = Label(root, text="VEZ DO JOGADOR 1", bg='white')
        turn_label.place(x=300, y=200, width=200, height=30)
 

    def criarPenteBar(self, root, numeroBalas):
        status_bar = Frame(root, bg='black', width=20, height=200)
        status_bar.place(x=700, y=150)
        
        for i in numeroBalas:
            color = 'green' if i is True else 'red'
            Label(status_bar, bg=color, width=2, height=1).pack()
        
    def conectar(self):
        print("Conectando")

    def desconectar(self):
        print("Desconectando")

    def getBalas(self):
        return [True, False, False, True]


Interface().criar_ui()

