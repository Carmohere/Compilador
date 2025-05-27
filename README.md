# Compilador PORTUGOL

Este projeto consiste no desenvolvimento de um compilador para a linguagem **PORTUGOL**, implementado na linguagem Python, como parte das atividades da disciplina de Compiladores. O compilador contempla as principais fases do processo de compilação, incluindo: **análise léxica**, **análise sintática**, **geração da árvore sintática abstrata (AST)** e **análise semântica**.
## Funcionalidades

- **Análise Léxica** com geração de tokens
- **Análise Sintática** com validação de comandos e estruturas
- **Geração da Árvore Sintática Abstrata (AST)**
- **Análise Semântica** com verificação de declaração e uso de variáveis
- **Mensagens de erro claras e posicionadas**
- Suporte às estruturas de controle **`se`, `senao`, `para`**
- Suporte a expressões aritméticas, lógicas e relacionais
- Suporte a entrada e saída com **`leia` e `escreva`**
- Suporte a declarações e atribuições de variáveis do tipo **`inteiro`**

## Estrutura do Projeto
```plaintext
Compilador/
├── entrada/
│   └── exemplo.POR
├── obj/
│   ├── saida_lexica.obj
│   └── saida_sinttica.obj
├── src/
│   ├── afd_definitions.py
│   └── ast.py
│   └── lexer.py
│   └── parser.py
│   └── semantico.py
│   └── tokens.py
├── main.py
└── README.md
```

### Pré-requisitos
- Python 3.13 (Versões anteriores podem não funcionar corretamente)
- Sistema Operacional: Compatível com Windows, Linux e macOS.


## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Carmohere/Compilador.git
   cd Compilador
   ```

2. Prepare um arquivo de entrada com código PORTUGOl no exemplo.POR, exemplo:
    ```bash
    inteiro:x
    x <- 10
    escreva(x)
    ```

3. Execute o **main.py**

4. Verifique as saídas:
   - A análise léxica será salva em: **obj/saida_lexica.obj**
   - A análise sintática **(AST)** será salva em: **obj/saida_sintatica.obj**
   - Se houver erros léxicos, sintáticos ou semânticos, o compilador imprimirá mensagens detalhadas com a descrição e posição do erro.
