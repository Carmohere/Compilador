import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lexer import analisar_lexico

if __name__ == "__main__":
    analisar_lexico("entrada/exemplo.POR", "obj/saida_lexica.OBJ")
