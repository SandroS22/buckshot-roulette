from random import randint, shuffle

class Arma:
    def __init__(self):
        self.__municoes = []
        self.__is_vazio = True
        self.__serrada = False


    @property
    def municoes(self):
        return self.__municoes

    @municoes.setter
    def municoes(self, value):
        self.__municoes = value

    @property
    def is_vazio(self):
        return self.__is_vazio

    @is_vazio.setter
    def is_vazio(self, value):
        self.__is_vazio = value

    @property
    def serrada(self):
        return self.__serrada

    @serrada.setter
    def serrada(self, serrada):
        self.__serrada = serrada

    def carregar(self):
        for _ in range(6):
            self.municoes.append(bool(randint(0, 1)))
        self.is_vazio = False

    def embaralhar_municao(self):
        shuffle(self.municoes)

    def atirar(self):
        if not self.is_vazio:
            self.municoes.pop(0)
            if len(self.municoes) == 0:
                self.is_vazio = True
            return True
        return False

    def remover_municao(self):
        if not self.is_vazio:
            return self.municoes.pop(0)

    def ver_camara(self):
        if not self.is_vazio:
            return self.municoes[0]
        return None

