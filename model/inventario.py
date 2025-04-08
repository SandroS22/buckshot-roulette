class Inventario:
    def __init__(self):
        self.__itens = []

    @property
    def itens(self):
        return self.__itens

    @itens.setter
    def itens(self, value):
        self.__itens = value

    def adicionar_item(self, item):
        self.itens.append(item)

    def remover_item(self, item):
        self.itens.remove(item)

    def listar_itens(self):
        return [item.tipo.name for item in self.itens]
