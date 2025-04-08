from random import randint
class Arma:
    def __init__(self):
        self.__municoes = []


    @property
    def municoes(self):
        return self.__municoes

    @municoes.setter
    def municoes(self, value):
        self.__municoes = value

    def carregar(self):
        for _ in range(6):
            self.municoes.append(bool(randint(0, 1)))

    def atirar(self):
        if len(self.municoes) > 0:
            return None
        return self.municoes.pop(0)

    def remover_municao(self):
        if self.municoes:
            self.municoes.pop(0)

    def ver_camara(self):
        if self.municoes:
            return self.municoes[0]
        return None

