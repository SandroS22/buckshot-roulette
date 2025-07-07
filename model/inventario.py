from model.item import Item

class Inventario:
    def __init__(self):
        self.__itens = []

    @property
    def itens(self):
        return self.__itens

    @itens.setter
    def itens(self, value):
        self.__itens = value

    def adicionar_item(self, tipo_item):
        item = Item(tipo_item)
        self.itens.append(item)

    def remover_item(self, item):
        self.itens.remove(item)

    def identificar_item(self, item):
        for item_inventario in self.itens:
            if item_inventario.tipo.name == item:
                return item_inventario
        return None

    def is_inventario_cheio(self):
        if len(self.itens) == 8:
            return True
        else:
            return False
