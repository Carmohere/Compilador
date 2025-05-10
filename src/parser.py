
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
