class ASTNode:
    def __init__(self, tipo, valor=None, filhos=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = filhos if filhos is not None else []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def __repr__(self, nivel=0):
        espaco = "  " * nivel
        resultado = f"{espaco}{self.tipo}"
        if self.valor is not None:
            resultado += f": {self.valor}"
        resultado += "\n"
        for filho in self.filhos:
            resultado += filho.__repr__(nivel + 1)
        return resultado

class Programa(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos

class ComandoEscreva(ASTNode):
    def __init__(self, valor):
        self.valor = valor

class ComandoLeia(ASTNode):
    def __init__(self, variavel):
        self.variavel = variavel

class Atribuicao(ASTNode):
    def __init__(self, variavel, expressao):
        self.variavel = variavel
        self.expressao = expressao

class DeclaracaoVariavel(ASTNode):
    def __init__(self, tipo, variavel):
        self.tipo = tipo
        self.variavel = variavel

class ComandoSe(ASTNode):
    def __init__(self, condicao, corpo, senao=None):
        self.condicao = condicao  # expressão booleana
        self.corpo = corpo        # lista de comandos
        self.senao = senao        # lista de comandos (ou None)

class ExpressaoBinaria(ASTNode):
    def __init__(self, esquerda, operador, direita):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

class Valor(ASTNode):
    def __init__(self, tipo, valor):
        self.tipo = tipo  # "NUMINT", "STRING", "ID"
        self.valor = valor