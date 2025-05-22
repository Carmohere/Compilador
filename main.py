import sys
import os
from src.parser import Parser
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.lexer import analisar_lexico
from src.semantico import AnalisadorSemantico


if __name__ == "__main__":
    analisar_lexico("entrada/exemplo.POR", "obj/saida_lexica.obj")

with open("obj/saida_lexica.obj", "r", encoding="utf-8") as f:
    linhas = f.readlines()
    tokens = [tuple(linha.strip().split()) for linha in linhas]

parser = Parser(tokens)
ast = parser.analisar()
print("Tokens reconhecidos:")
for t in tokens:
    print(t)

def salvar_ast_em_arquivo(ast, caminho_arquivo):
    # Verifica se a pasta 'obj' existe, caso contrário, cria
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(str(ast))

salvar_ast_em_arquivo(ast, 'obj/saida_sintatica.obj')
print("Arquivo AST gerado em 'obj/saida_sintatica.obj'")

# Análise semântica
analisador = AnalisadorSemantico(ast)
analisador.analisar()