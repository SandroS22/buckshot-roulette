from enum import Enum

class TipoItem(Enum):
    ALGEMAS = "Algemas: impede o inimigo de jogar por uma rodada."
    CERVEJA = "Cerveja: remove a munição atual da arma."
    CIGARRO = "Cigarro: recupera 1 de vida."
    LUPA = "Lupa: revela a munição da câmara atual."
    SERRA = "Serra: duplica o dano da arma."
