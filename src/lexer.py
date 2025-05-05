import re
import json
from pathlib import Path
from afd_definitions import token_regex
from tokens import TOKENS


TABELA_SIMBOLOS = {}
SIMBOLO_POS = 0

def eh_palavra_reservada(lexema):
    for token in ["TIPO", "SE", "ENTAO", "SENAO", "FIMSE", "PARA", "ATE", "PASSO", "FIMPARA", "LEIA", "ESCREVA", "E", "OU", "NAO"]:
        if re.fullmatch(token_regex[token], lexema):
            return token
    return None

def adicionar_simbolo(lexema):
    global SIMBOLO_POS
    if lexema not in TABELA_SIMBOLOS:
        TABELA_SIMBOLOS[lexema] = SIMBOLO_POS
        SIMBOLO_POS += 1
    return TABELA_SIMBOLOS[lexema]

def analisar_lexico(caminho_entrada, caminho_saida):
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        codigo = f.read()

    tokens_encontrados = []
    pos = 0

    while pos < len(codigo):
        if codigo[pos].isspace():
            pos += 1
            continue

        match = None
        for token_name, pattern in token_regex.items():
            regex = re.compile(pattern)
            m = regex.match(codigo, pos)
            if m:
                lexema = m.group()
                token = token_name

                if token == "ID":
                    reservado = eh_palavra_reservada(lexema)
                    if reservado:
                        token = reservado
                    else:
                        pos_simbolo = adicionar_simbolo(lexema)
                        tokens_encontrados.append((TOKENS["ID"], pos_simbolo))
                        pos += len(lexema)
                        break

                elif token == "STRING" or token == "NUMINT":
                    tokens_encontrados.append((TOKENS[token], lexema))
                    pos += len(lexema)
                    break
                else:
                    tokens_encontrados.append((TOKENS[token], lexema))
                    pos += len(lexema)
                    break

        if not match and not m:
            print(f"[ERRO] Lexema não reconhecido próximo de: {codigo[pos:pos+10]}")
            pos += 1  # ignora caractere inválido (pode-se abortar o programa se preferir)

    # Token final de arquivo
    tokens_encontrados.append((TOKENS["EOF"], "EOF"))

    # Escrever arquivo de saída (.OBJ)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        for codigo, valor in tokens_encontrados:
            f.write(f"{codigo} {valor}\n")

    # Escrever tabela de símbolos
    with open("obj/tabela_simbolos.json", "w", encoding="utf-8") as f:
        json.dump(TABELA_SIMBOLOS, f, indent=4, ensure_ascii=False)

    print("[✔] Análise léxica concluída com sucesso.")

