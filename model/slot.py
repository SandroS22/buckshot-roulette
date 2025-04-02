from tipoItem import TipoItem

class Slot:
    def __init__(self):
        self.__item = None
    
    @property
    def item(self):
        return self.__item
    
    @item.setter
    def item(self, item):
        if(isinstance(item, TipoItem)):
            self.__item = item
