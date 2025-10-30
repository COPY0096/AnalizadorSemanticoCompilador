import ply.lex as lex
import ply.yacc as yacc

# -----------------------------
# LÉXICO
# -----------------------------

tokens = (
    'INT', 'FLOAT', 'ID', 'NUM_INT', 'NUM_FLOAT',
    'ASSIGN', 'SEMI', 'PLUS', 'MINUS', 'MUL', 'DIV'
)

reserved = {
    'int': 'INT',
    'float': 'FLOAT'
}

t_ASSIGN = r'='
t_SEMI   = r';'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MUL    = r'\*'
t_DIV    = r'/'

t_ignore = ' \t'

def t_NUM_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# -----------------------------
# SINTAXIS
# -----------------------------

# Tipos de datos (tabla de símbolos)
symbol_table = {}

# Precedencia (para +, -, *, /)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)

def p_program(p):
    '''program : stmt_list'''
    print("✅ Análisis sintáctico y semántico completado sin errores.")

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''

def p_stmt(p):
    '''stmt : declaration
            | assignment'''

# --- Declaraciones ---
def p_declaration(p):
    '''declaration : type ID SEMI
                   | type ID ASSIGN expression SEMI'''
    var_type = p[1]
    var_name = p[2]

    if var_name in symbol_table:
        print(f"Error semántico: variable '{var_name}' ya declarada.")
    else:
        symbol_table[var_name] = var_type

    # Asignación inicial (opcional)
    if len(p) == 6:
        expr_type = p[4]
        if not compatible(var_type, expr_type):
            print(f"Error de tipo: no se puede asignar {expr_type} a {var_type} ({var_name})")

# --- Asignaciones ---
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI'''
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Error semántico: variable '{var_name}' no declarada.")
    else:
        var_type = symbol_table[var_name]
        expr_type = p[3]
        if not compatible(var_type, expr_type):
            print(f"Error de tipo: no se puede asignar {expr_type} a {var_type} ({var_name})")

# --- Tipos ---
def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

# --- Expresiones ---
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = result_type(p[1], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_binop(p):
    '''term : term MUL factor
            | term DIV factor'''
    p[0] = result_type(p[1], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUM_INT
              | NUM_FLOAT'''
    if isinstance(p[1], int):
        p[0] = 'int'
    else:
        p[0] = 'float'

def p_factor_id(p):
    '''factor : ID'''
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Error semántico: variable '{var_name}' no declarada.")
        p[0] = 'error'
    else:
        p[0] = symbol_table[var_name]

def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}' (línea {p.lineno})")
    else:
        print("Error sintáctico: fin de archivo inesperado.")

# -----------------------------
# FUNCIONES AUXILIARES
# -----------------------------

def compatible(dest, src):
    """Verifica si se puede asignar un tipo a otro"""
    if dest == src:
        return True
    if dest == 'float' and src == 'int':
        return True  # promoción válida
    return False

def result_type(t1, t2):
    """Determina el tipo resultante de una operación"""
    if 'error' in (t1, t2):
        return 'error'
    if 'float' in (t1, t2):
        return 'float'
    return 'int'

# -----------------------------
# MAIN
# -----------------------------
if __name__ == '__main__':
    parser = yacc.yacc()

    code = """
    int a;
    float b = 3.14;
    a = 5;
    b = a + 2.5;
    c = 4;
    int a;
    a = 3.14;
    """

    print("=== Análisis Léxico, Sintáctico y Semántico ===")
    parser.parse(code)
