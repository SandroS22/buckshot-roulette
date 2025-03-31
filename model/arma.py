from random import randint

class Gun:
    def __init__(self):
        self.__pente = []
    
    @property
    def pente(self):
        """The pente property."""
        return self.__pente

    @pente.setter
    def pente(self, value):
        self.__pente = value
    
    def atirar(self):
        bala = self.pente[0]
        self.pente.pop(0)
        return bala

    def carregar(self):
        for i in range(6):
            result = randint(0,1)
            self.pente.append(bool(result))

