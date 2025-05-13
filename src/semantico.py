class AnalisadorSemantico:
    def __init__(self, ast):
        self.ast = ast
        self.variaveis_declaradas = set()
        self.erros = []

    def analisar(self):
        self._verificar_no(self.ast)

        if self.erros:
            print("Erros semânticos encontrados:")
            for erro in self.erros:
                print(" -", erro)
        else:
            print("Análise semântica concluída com sucesso.")

    def _verificar_no(self, no):
        if no.tipo == "DECLARACAO":
            id_node = next((filho for filho in no.filhos if filho.tipo == "ID"), None)
            if id_node:
                nome = id_node.valor
                if nome in self.variaveis_declaradas:
                    self.erros.append(f"Variável '{nome}' já declarada.")
                else:
                    self.variaveis_declaradas.add(nome)

        elif no.tipo in {"LEIA", "ATRIBUICAO"}:
            id_node = next((filho for filho in no.filhos if filho.tipo == "ID"), None)
            if id_node and id_node.valor not in self.variaveis_declaradas:
                self.erros.append(f"Variável '{id_node.valor}' usada sem declaração.")

        elif no.tipo == "ESCREVA":
            expr_node = next((filho for filho in no.filhos), None)
            if expr_node and expr_node.tipo == "ID":
                if expr_node.valor not in self.variaveis_declaradas:
                    self.erros.append(f"Variável '{expr_node.valor}' usada sem declaração.")

        # Recursão para os filhos
        for filho in no.filhos:
            self._verificar_no(filho)