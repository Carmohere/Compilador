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
        return (str(TOKENS["EOF"]), "EOF")

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
            elif tipo == 'PARA':
                node = self.cmd_para()
            elif tipo == 'EOF':
                break
            else:
                self.erro("Comando não reconhecido", token)
                self.proximo_token()
                continue

            if node:
                raiz.adicionar_filho(node)

        print("Análise sintática concluída com sucesso!")
        return raiz

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

        return ASTNode("LEIA", valor=id_token[1])

    def cmd_para(self):
        print("Reconhecendo comando 'para'")

        # Consome o token 'PARA'
        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PARA":
            self.erro("Esperado 'para'", token)

        # Identificador de controle
        id_token = self.proximo_token()
        if TOKEN_MAP.get(id_token[0]) != "ID":
            self.erro("Esperado identificador no comando 'para'", id_token)

        # Operador de atribuição <-
        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ATR":
            self.erro("Esperado operador de atribuição '<-'", token)

        # Expressão inicial
        inicio_expr = self.expressao()

        # Palavra-chave 'ate'
        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ATE":
            self.erro("Esperado 'ate'", token)

        # Expressão final
        fim_expr = self.expressao()

        # Palavra-chave 'passo'
        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "PASSO":
            self.erro("Esperado 'passo'", token)

        # Expressão de incremento
        passo_expr = self.expressao()

        # Bloco de comandos do loop
        comandos = []
        while TOKEN_MAP.get(self.token_atual()[0]) not in ("FIMPARA", "EOF"):
            comandos.append(self.analisar())  # ou self.cmd()

        print("Comando 'para' reconhecido com sucesso.")
        return ASTNode("PARA", filhos=[
            ASTNode("ID", valor=id_token[1]),
            ASTNode("INICIO", filhos=[inicio_expr]),
            ASTNode("FIM", filhos=[fim_expr]),
            ASTNode("PASSO", filhos=[passo_expr]),
            ASTNode("COMANDOS", filhos=comandos)
        ])

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

        print("Declaração de variável reconhecida com sucesso.")
        return ASTNode("DECLARACAO", filhos=[
            ASTNode("TIPO", valor=tipo_nome),
            ASTNode("ID", valor=id_token[1])
        ])

    def expressao(self):
        return self.expressao_logica()

    def expressao_logica(self):
        esquerda = self.expressao_relacional()
        while TOKEN_MAP.get(self.token_atual()[0]) in ("E", "OU"):
            op_token = self.proximo_token()
            direita = self.expressao_relacional()
            esquerda = ASTNode("EXP_LOGICA", valor=op_token[1], filhos=[esquerda, direita])
        return esquerda

    def expressao_relacional(self):
        esquerda = self.expressao_aritmetica()
        if TOKEN_MAP.get(self.token_atual()[0]) in (
            "LOGIGUAL", "LOGDIFF", "LOGMAIOR", "LOGMENOR", "LOGMAIORIGUAL", "LOGMENORIGUAL"
        ):
            op_token = self.proximo_token()
            direita = self.expressao_aritmetica()
            return ASTNode("EXP_RELACIONAL", valor=op_token[1], filhos=[esquerda, direita])
        return esquerda

    def expressao_aritmetica(self):
        termo1 = self.proximo_token()
        if TOKEN_MAP.get(termo1[0]) not in ("ID", "NUMINT"):
            self.erro("Esperado identificador ou número inteiro na expressão", termo1)

        node = ASTNode("OPERANDO", valor=termo1[1])

        if self.token_atual()[0] in ("19", "20", "18", "21"):
            op_token = self.proximo_token()
            termo2 = self.proximo_token()
            if TOKEN_MAP.get(termo2[0]) not in ("ID", "NUMINT"):
                self.erro("Esperado segundo operando após operador", termo2)

            return ASTNode("EXP_ARITMETICA", filhos=[
                ASTNode("OPERANDO", valor=termo1[1]),
                ASTNode("OPERADOR", valor=op_token[1]),
                ASTNode("OPERANDO", valor=termo2[1])
            ])

        return node

    def cmd_atribuicao(self):
        print("Reconhecendo comando de atribuição")

        id_token = self.proximo_token()
        if TOKEN_MAP.get(id_token[0]) != "ID":
            self.erro("Esperado identificador no início da atribuição", id_token)

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ATR":
            self.erro("Esperado operador de atribuição '<-'", token)

        expressao_node = self.expressao()

        print("Comando de atribuição reconhecido com sucesso.")

        return ASTNode("ATRIBUICAO", filhos=[
            ASTNode("ID", valor=id_token[1]),
            expressao_node
        ])

    def cmd_se(self):
        print("Reconhecendo comando 'se'")
        self.proximo_token()  # consome 'SE'

        condicao = self.expressao()

        token = self.proximo_token()
        if TOKEN_MAP.get(token[0]) != "ENTAO":
            self.erro("Esperado 'entao' após condição", token)

        # Bloco do 'entao'
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
            elif tipo == "SE":
                comandos_entao.append(self.cmd_se())  # Suporte a aninhamento
            elif tipo == "SENAO" or tipo == "FIMSE":
                break
            else:
                self.erro("Comando inválido dentro de 'se'", token)
                break

        # Bloco do 'senao'
        comandos_senao = []
        token = self.token_atual()
        if TOKEN_MAP.get(token[0]) == "SENAO":
            self.proximo_token()
            while True:
                token = self.token_atual()
                tipo = TOKEN_MAP.get(token[0])
                if tipo == "ESCREVA":
                    comandos_senao.append(self.cmd_escreva())
                elif tipo == "LEIA":
                    comandos_senao.append(self.cmd_leia())
                elif tipo == "ID":
                    comandos_senao.append(self.cmd_atribuicao())
                elif tipo == "SE":
                    comandos_senao.append(self.cmd_se())
                elif tipo == "FIMSE":
                    break
                else:
                    self.erro("Comando inválido dentro de 'senao'", token)
                    break

        # Finalização obrigatória
        token = self.token_atual()
        if TOKEN_MAP.get(token[0]) != "FIMSE":
            self.erro("Esperado 'fimse'", token)
        self.proximo_token()  # consome fimse

        print("Comando 'se' reconhecido com sucesso.")

        filhos = [
            condicao,
            ASTNode("ENTAO", filhos=comandos_entao)
        ]
        if comandos_senao:
            filhos.append(ASTNode("SENAO", filhos=comandos_senao))

        return ASTNode("SE", filhos=filhos)

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