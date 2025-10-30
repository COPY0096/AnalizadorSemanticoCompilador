
import sys
import ply.lex as lex
import ply.yacc as yacc

# ------------------------
# LÉXICO
# ------------------------
tokens = (
    'INT_KW', 'FLOAT_KW',
    'ID',
    'NUM_INT', 'NUM_FLOAT',
    'ASSIGN', 'SEMI',
    'PLUS', 'MINUS', 'TIMES', 'DIV',
    'LPAREN', 'RPAREN'
)

reserved = {
    'int': 'INT_KW',
    'float': 'FLOAT_KW'
}

t_ASSIGN = r'='
t_SEMI  = r';'
t_PLUS  = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV   = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

# Keep track of line numbers and simple column calculation
def find_column(input, lexpos):
    last_cr = input.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return (lexpos - last_cr)

def t_NUM_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    t.type = 'NUM_FLOAT'
    return t

def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUM_INT'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'\/\/.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    col = find_column(t.lexer.lexdata, t.lexpos)
    print(f"[Error léxico] Línea {t.lineno}, col {col}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()

# ------------------------
# SEMÁNTICA / TIPOS
# ------------------------
TYPE_INT = 'int'
TYPE_FLOAT = 'float'
TYPE_ERROR = 'error'

# symbol table: name -> {'type': TYPE_..., 'line': n}
symbol_table = {}

# record semantic errors
semantic_errors = []

def sym_declare(name, typ, lineno):
    if name in symbol_table:
        prev_line = symbol_table[name]['line']
        semantic_errors.append((lineno, f"Redeclaración de la variable '{name}' (declarada previamente en la línea {prev_line})"))
        return False
    symbol_table[name] = {'type': typ, 'line': lineno}
    return True

def sym_exists(name):
    return name in symbol_table

def sym_get_type(name):
    if name in symbol_table:
        return symbol_table[name]['type']
    return TYPE_ERROR

def type_name(t):
    return t

def result_type(t1, t2):
    if TYPE_ERROR in (t1, t2): return TYPE_ERROR
    if TYPE_FLOAT in (t1, t2): return TYPE_FLOAT
    return TYPE_INT

def compatible(dest, src):
    """Dest <- Src"""
    if dest == TYPE_ERROR or src == TYPE_ERROR: return False
    if dest == src: return True
    if dest == TYPE_FLOAT and src == TYPE_INT: return True  # allow promotion
    return False

# ------------------------
# SINTAXIS (GRAMÁTICA)
# ------------------------
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
)

def p_program(p):
    "program : stmt_list"
    p[0] = ('program', p[1])

def p_stmt_list_multi(p):
    "stmt_list : stmt_list stmt"
    p[0] = p[1] + [p[2]]

def p_stmt_list_single(p):
    "stmt_list : stmt"
    p[0] = [p[1]]

def p_stmt_decl(p):
    "stmt : decl SEMI"
    p[0] = p[1]

def p_stmt_assign(p):
    "stmt : assign SEMI"
    p[0] = p[1]

# declaration: type ID [= expr] ;
def p_decl_noassign(p):
    "decl : type ID"
    typ = p[1]
    name = p[2]
    lineno = p.lineno(2)
    sym_declare(name, typ, lineno)
    p[0] = ('decl', typ, name, None)

def p_decl_assign(p):
    "decl : type ID ASSIGN expression"
    typ = p[1]
    name = p[2]
    lineno = p.lineno(2)
    # declare (may report redeclaration)
    sym_declare(name, typ, lineno)
    expr_type = p[4]
    if not compatible(typ, expr_type):
        semantic_errors.append((lineno, f"Error de tipo: no se puede asignar una expresión de tipo {type_name(expr_type)} a la variable '{name}' de tipo {type_name(typ)}"))
    p[0] = ('decl_assign', typ, name, p[4])

# assignment: ID = expr ;
def p_assign(p):
    "assign : ID ASSIGN expression"
    name = p[1]
    lineno = p.lineno(1)
    if not sym_exists(name):
        semantic_errors.append((lineno, f"Variable no declarada '{name}'"))
        # still try to continue: treat as error type
        p[0] = ('assign', name, p[3])
    else:
        dest_type = sym_get_type(name)
        expr_type = p[3]
        if not compatible(dest_type, expr_type):
            semantic_errors.append((lineno, f"Error de tipo: no se puede asignar una expresión de tipo {type_name(expr_type)} a la variable '{name}' de tipo {type_name(dest_type)}"))
        p[0] = ('assign', name, p[3])

# type nonterminal
def p_type_int(p):
    "type : INT_KW"
    p[0] = TYPE_INT

def p_type_float(p):
    "type : FLOAT_KW"
    p[0] = TYPE_FLOAT

# expressions
def p_expression_binop(p):
    """expression : expression PLUS term
                  | expression MINUS term"""
    t1 = p[1]
    t2 = p[3]
    p[0] = result_type(t1, t2)

def p_expression_term(p):
    "expression : term"
    p[0] = p[1]

def p_term_binop(p):
    """term : term TIMES factor
            | term DIV factor"""
    t1 = p[1]
    t2 = p[3]
    p[0] = result_type(t1, t2)

def p_term_factor(p):
    "term : factor"
    p[0] = p[1]

def p_factor_num_int(p):
    "factor : NUM_INT"
    p[0] = TYPE_INT

def p_factor_num_float(p):
    "factor : NUM_FLOAT"
    p[0] = TYPE_FLOAT

def p_factor_id(p):
    "factor : ID"
    name = p[1]
    lineno = p.lineno(1)
    if not sym_exists(name):
        semantic_errors.append((lineno, f"Variable no declarada '{name}'"))
        p[0] = TYPE_ERROR
    else:
        p[0] = sym_get_type(name)

def p_factor_paren(p):
    "factor : LPAREN expression RPAREN"
    p[0] = p[2]

def p_error(p):
    if p:
        lineno = p.lineno if hasattr(p, 'lineno') else '?'
        val = p.value if hasattr(p, 'value') else '?'
        print(f"[Error sintáctico] Línea {lineno}: token inesperado '{val}'")
    else:
        print("[Error sintáctico] Fin inesperado de la entrada")

# Build parser
parser = yacc.yacc()

# ------------------------
# MAIN / IO
# ------------------------
def analyze_file(path):
    # read input
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    # attach input to lexer for column calc
    lexer.lexdata = data

    print("=== ENTRADA ===")
    print(data.rstrip())
    print("=============\n")

    # --- Mostrar tokens sin consumir el lexer que usará el parser ---
    print("Tokens (análisis léxico):")
    # Creamos un lexer temporal para inspección (no consumirá el lexer principal)
    temp_lex = lex.lex()   # crea instancia nueva
    temp_lex.input(data)
    for tok in temp_lex:
        col = find_column(data, tok.lexpos)
        print(f"  Línea {tok.lineno}, col {col}: {tok.type} -> {tok.value}")
    print("")

    # reset symbol table and errors for fresh analysis
    global symbol_table, semantic_errors
    symbol_table = {}
    semantic_errors = []

    # --- Reiniciamos el lexer principal para el parser ---
    lexer.input(data)
    lexer.lexdata = data
    lexer.lineno = 1

    # parse (and run semantic actions)
    parser.parse(data, lexer=lexer)

    # print results
    if semantic_errors:
        print("\nErrores semánticos/de tipo:")
        for ln, msg in semantic_errors:
            print(f"  Línea {ln}: {msg}")
    else:
        print("\nNo se detectaron errores semánticos.")

    # symbol table summary
    print("\nTabla de símbolos:")
    if symbol_table:
        for name, info in symbol_table.items():
            print(f"  {name} : {info['type']}   (declarada en la línea {info['line']})")
    else:
        print("  (sin símbolos)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python compiler.py <archivo-fuente.txt>")
        sys.exit(1)
    analyze_file(sys.argv[1])
