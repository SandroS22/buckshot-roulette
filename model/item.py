from model.tipoItem import TipoItem


class Item:
    def __init__(self, tipo_item: TipoItem):
        self.__tipo = tipo_item
        self.__descricao = tipo_item.value

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, value):
        self.__tipo = value
        
    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        self.__descricao = value

    def icone(self):
        nome_icone = "ui/" + self.tipo.name.lower() + ".png"
        return nome_icone 
