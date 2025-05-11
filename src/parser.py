
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
        while self.posicao < len(self.tokens):
            token = self.token_atual()
            tipo = TOKEN_MAP.get(token[0], 'DESCONHECIDO')

            if tipo == 'ESCREVA':
                self.cmd_escreva()
            elif tipo == 'LEIA':
                self.cmd_leia()

            elif tipo == 'TIPO':
                self.cmd_declaracao()

            elif tipo == 'ID':
                self.cmd_atribuicao()

            elif tipo == 'SE':
                self.cmd_se()

            elif tipo == 'PARA':
                self.cmd_para()

            elif tipo == 'EOF':
                break
            else:
                self.erro("Comando não reconhecido", token)
                self.proximo_token()

        print("Análise sintática concluída com sucesso!")

    def cmd_escreva(self):
        print("Reconhecendo comando 'escreva'")
        self.proximo_token()  # consome ESCREVA

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            return self.erro("Esperado '(' após 'escreva'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) not in ("STRING", "ID", "NUMINT"):
            return self.erro("Esperado valor STRING, ID ou NUMINT dentro de 'escreva'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            return self.erro("Esperado ')' após valor em 'escreva'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' após 'escreva'", token)

        print("Comando 'escreva' reconhecido com sucesso.")

    def cmd_leia(self):
        print("Reconhecendo comando 'leia'")
        self.proximo_token()  # consome LEIA

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            return self.erro("Esperado '(' após 'leia'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ID":
            return self.erro("Esperado ID dentro de 'leia'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            return self.erro("Esperado ')' após ID em 'leia'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' após 'leia'", token)

        print("Comando 'leia' reconhecido com sucesso.")

    def cmd_declaracao(self):
        print("Reconhecendo declaração de variável")
        self.proximo_token()  # consome TIPO

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "DOIS_PONTOS":
            return self.erro("Esperado ':' após tipo na declaração", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ID":
            return self.erro("Esperado identificador (ID) na declaração", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' ao final da declaração", token)

        print("Declaração de variável reconhecida com sucesso.")

    def cmd_atribuicao(self):
        print("Reconhecendo comando de atribuição")
        token = self.proximo_token()  # consome ID

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ATR":
            return self.erro("Esperado operador de atribuição '<-'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) not in ("NUMINT", "ID", "STRING"):
            return self.erro("Esperado valor NUMINT, ID ou STRING na atribuição", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' após a atribuição", token)

        print("Comando de atribuição reconhecido com sucesso.")

    def cmd_se(self):
        print("Reconhecendo comando 'se'")
        self.proximo_token()  # consome 'SE'

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARAB":
            return self.erro("Esperado '(' após 'se'", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) not in ("ID", "NUMINT"):
            return self.erro("Esperado ID ou número na condição", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) not in ("LOGMENOR", "LOGMAIOR", "LOGIGUAL", "LOGDIFF", "LOGMENORIGUAL",
                                           "LOGMAIORIGUAL"):
            return self.erro("Esperado operador lógico na condição", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) not in ("ID", "NUMINT"):
            return self.erro("Esperado ID ou número após operador lógico", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARFE":
            return self.erro("Esperado ')' após condição", token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ENTAO":
            return self.erro("Esperado 'entao' após condição", token)

        # Reconhece comandos dentro do bloco
        while True:
            token = self.token_atual()
            tipo = TOKEN_MAP.get(token[0])

            if tipo == "ESCREVA":
                self.cmd_escreva()
            elif tipo == "LEIA":
                self.cmd_leia()
            elif tipo == "ID":
                self.cmd_atribuicao()
            elif tipo == "FIMSE":
                break
            else:
                return self.erro("Comando inválido dentro de 'se'", token)

        self.proximo_token()  # consome 'FIMSE'

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PONTO_VIRGULA":
            return self.erro("Esperado ';' após 'fimse'", token)

        print("Comando 'se' reconhecido com sucesso.")




