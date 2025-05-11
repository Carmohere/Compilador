import sys
import os
from src.parser import Parser
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lexer import analisar_lexico

if __name__ == "__main__":
    analisar_lexico("entrada/exemplo.POR", "obj/saida_lexica.OBJ")

with open("obj/saida_lexica.obj", "r", encoding="utf-8") as f:
    linhas = f.readlines()
    tokens = [tuple(linha.strip().split()) for linha in linhas]

parser = Parser(tokens)
parser.analisar()
print("Tokens reconhecidos:")
for t in tokens:
    print(t)
