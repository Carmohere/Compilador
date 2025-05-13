from src.ast import ASTNode
from src.tokens import TOKENS

# Inverter o dicionário para mapear código → nome
TOKEN_MAP = {str(v): k for k, v in TOKENS.items()}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def proximo_token(self):
        if self.posicao < len(self.tokens):
            token = self.tokens[self.posicao]
            self.posicao += 1
            return token
        return (str(TOKENS["EOF"]), "EOF")  # Retorna o token EOF

    def token_atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return (str(TOKENS["EOF"]), "EOF")

    def erro(self, mensagem, token):
        print(f"Erro Sintático: {mensagem} (token: {token}, posição: {self.posicao})")

    def analisar(self):
        raiz = ASTNode("PROGRAMA")
        while self.posicao < len(self.tokens):
            token = self.token_atual()
            tipo = TOKEN_MAP.get(token[0], 'DESCONHECIDO')

            if tipo == 'TIPO':
                node = self.cmd_declaracao()
            elif tipo == 'ID':
                node = self.cmd_atribuicao()
            elif tipo == 'LEIA':
                node = self.cmd_leia()
            elif tipo == 'ESCREVA':
                node = self.cmd_escreva()
            elif tipo == 'SE':
                node = self.cmd_se()
            elif tipo == 'EOF':
                break
            else:
                self.erro("Comando não reconhecido", token)
                self.proximo_token()
                continue

            if node:
                raiz.adicionar_filho(node)

        print("Análise sintática concluída com sucesso!")
        return raiz  # retorna a raiz da árvore

    def cmd_escreva(self):
        print("Reconhecendo comando 'escreva'")
        self.proximo_token()  # consome 'ESCREVA'

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            self.erro("Esperado '(' após 'escreva'", token)

        valor_token = self.proximo_token()
        if TOKEN_MAP.get(valor_token[0]) not in ("STRING", "ID", "NUMINT"):
            self.erro("Esperado STRING, ID ou NUMINT dentro de 'escreva'", valor_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            self.erro("Esperado ')' após valor em 'escreva'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            self.erro("Esperado ';' após 'escreva'", token)

        print("Comando 'escreva' reconhecido com sucesso.")

        return ASTNode("ESCREVA", filhos=[
            ASTNode("VALOR", valor=valor_token[1])
        ])

    def cmd_leia(self):
        self.proximo_token()  # consome 'LEIA'

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            self.erro("Esperado '(' após 'leia'", token)

        id_token = self.proximo_token()
        if TOKEN_MAP.get(id_token[0]) != "ID":
            self.erro("Esperado ID dentro de 'leia'", id_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            self.erro("Esperado ')' após ID em 'leia'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            self.erro("Esperado ';' após 'leia'", token)

        return ASTNode("LEIA", valor=id_token[1])

    def cmd_declaracao(self):
        print("Reconhecendo declaração de variável")
        tipo_token = self.proximo_token()  # consome TIPO
        tipo_nome = tipo_token[1]

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "DOIS_PONTOS":
            return self.erro("Esperado ':' após tipo na declaração", token)

        id_token = self.proximo_token()
        if TOKEN_MAP.get(id_token[0]) != "ID":
            return self.erro("Esperado identificador (ID) na declaração", id_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' ao final da declaração", token)

        print("Declaração de variável reconhecida com sucesso.")
        return ASTNode("DECLARACAO", filhos=[
            ASTNode("TIPO", valor=tipo_nome),
            ASTNode("ID", valor=id_token[1])
        ])

    def cmd_atribuicao(self):
        print("Reconhecendo comando de atribuição")

        id_token = self.proximo_token()
        if TOKEN_MAP.get(id_token[0]) != "ID":
            self.erro("Esperado identificador no início da atribuição", id_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ATR":
            self.erro("Esperado operador de atribuição '<-'", token)

        valor_token = self.proximo_token()
        if TOKEN_MAP.get(valor_token[0]) not in ("ID", "NUMINT", "STRING"):
            self.erro("Esperado valor numérico, identificador ou string na atribuição", valor_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            self.erro("Esperado ';' após valor na atribuição", token)

        print("Comando de atribuição reconhecido com sucesso.")

        return ASTNode("ATRIBUICAO", filhos=[
            ASTNode("ID", valor=id_token[1]),
            ASTNode("VALOR", valor=valor_token[1])
        ])

    def cmd_se(self):
        print("Reconhecendo comando 'se'")
        self.proximo_token()  # consome 'SE'

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            self.erro("Esperado '(' após 'se'", token)

        esquerda = self.proximo_token()
        if TOKEN_MAP.get(esquerda[0]) not in ("ID", "NUMINT"):
            self.erro("Esperado ID ou número na condição", esquerda)

        operador = self.proximo_token()
        if TOKEN_MAP.get(operador[0]) not in ("LOGMENOR", "LOGMAIOR", "LOGIGUAL", "LOGDIFF", "LOGMENORIGUAL",
                                              "LOGMAIORIGUAL"):
            self.erro("Esperado operador lógico na condição", operador)

        direita = self.proximo_token()
        if TOKEN_MAP.get(direita[0]) not in ("ID", "NUMINT"):
            self.erro("Esperado ID ou número após operador lógico", direita)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            self.erro("Esperado ')' após condição", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ENTAO":
            self.erro("Esperado 'entao' após condição", token)

        # Nó da condição
        condicao = ASTNode("CONDICAO", filhos=[
            ASTNode("OPERANDO", valor=esquerda[1]),
            ASTNode("OPERADOR", valor=operador[1]),
            ASTNode("OPERANDO", valor=direita[1])
        ])

        # Bloco 'entao'
        comandos_entao = []
        while True:
            token = self.token_atual()
            tipo = TOKEN_MAP.get(token[0])
            if tipo == "ESCREVA":
                comandos_entao.append(self.cmd_escreva())
            elif tipo == "LEIA":
                comandos_entao.append(self.cmd_leia())
            elif tipo == "ID":
                comandos_entao.append(self.cmd_atribuicao())
            elif tipo == "SENAO":
                break
            elif tipo == "FIMSE":
                break
            else:
                self.erro("Comando inválido dentro de 'se'", token)
                break

        # Bloco 'senao' (opcional)
        comandos_senao = []
        token = self.token_atual()
        if TOKEN_MAP.get(token[0]) == "SENAO":
            self.proximo_token()  # consome 'senao'
            while True:
                token = self.token_atual()
                tipo = TOKEN_MAP.get(token[0])
                if tipo == "ESCREVA":
                    comandos_senao.append(self.cmd_escreva())
                elif tipo == "LEIA":
                    comandos_senao.append(self.cmd_leia())
                elif tipo == "ID":
                    comandos_senao.append(self.cmd_atribuicao())
                elif tipo == "FIMSE":
                    break
                else:
                    self.erro("Comando inválido dentro de 'senao'", token)
                    break

        token = self.token_atual()
        if TOKEN_MAP.get(token[0]) != "FIMSE":
            self.erro("Esperado 'fimse'", token)
        self.proximo_token()

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            self.erro("Esperado ';' após 'fimse'", token)

        print("Comando 'se' reconhecido com sucesso.")
        return ASTNode("SE", filhos=[
            condicao,
            ASTNode("ENTAO", filhos=comandos_entao),
            ASTNode("SENAO", filhos=comandos_senao) if comandos_senao else None
        ])


def salvar_ast_em_arquivo(ast, caminho, nivel=0):
    with open(caminho, "w", encoding="utf-8") as f:
        def escrever_no_arquivo(no, nivel):
            indent = "  " * nivel
            if no.valor is not None:
                valor_formatado = repr(no.valor).replace("\n", "\\n")  # <- evita quebra real de linha
                f.write(f"{indent}{no.tipo}: {valor_formatado}\n")
            else:
                f.write(f"{indent}{no.tipo}\n")
            for filho in no.filhos:
                escrever_no_arquivo(filho, nivel + 1)

        escrever_no_arquivo(ast, nivel)
