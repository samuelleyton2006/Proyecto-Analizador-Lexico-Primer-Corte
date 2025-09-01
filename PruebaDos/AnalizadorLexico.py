PALABRAS_RESERVADAS = [
    "False", "None", "True", "and", "as", "assert", "break", "class", "continue", "def",
    "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import",
    "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield", "print"
]

OPERADORES_DOBLES = {
    '->': "tk_flecha", '<=': "tk_menor_igual", '>=': "tk_mayor_igual",
    '==': "tk_igual_igual", '!=': "tk_distinto"
}
OPERADORES_SIMPLES = {
    ':': "tk_dos_puntos", ',': "tk_coma", '.': "tk_punto", '=': "tk_asig", '+': "tk_suma",
    '-': "tk_menos", '*': "tk_mult", '/': "tk_div", '%': "tk_mod", '(': "tk_par_izq",
    ')': "tk_par_der", '{': "tk_llave_izq", '}': "tk_llave_der", '[': "tk_corchete_izq",
    ']': "tk_corchete_der", '<': "tk_menor", '>': "tk_mayor"
}

def es_letra(c):
    return c.isalpha() or c == '_'

def es_digito(c):
    return c.isdigit()

def automata_cadena(linea, pos):
    if linea[pos] == '"' or linea[pos] == "'":
        comilla = linea[pos]
        lexema = comilla
        i = pos + 1
        while i < len(linea):
            if linea[i] == '\\' and i + 1 < len(linea):
                lexema += linea[i] + linea[i+1]
                i += 2
            elif linea[i] == comilla:
                lexema += comilla
                return lexema, i - pos + 1
            else:
                lexema += linea[i]
                i += 1
    return None, 0

def automata_entero(linea, pos):
    i = pos
    lexema = ''
    if linea[i] == '+' or linea[i] == '-':
        lexema += linea[i]
        i += 1
        if i >= len(linea) or not es_digito(linea[i]):
            return None, 0
    if i < len(linea) and es_digito(linea[i]):
        while i < len(linea) and es_digito(linea[i]):
            lexema += linea[i]
            i += 1
        return lexema, i - pos
    return None, 0

def automata_identificador(linea, pos):
    i = pos
    lexema = ''
    if es_letra(linea[i]):
        while i < len(linea) and (es_letra(linea[i]) or es_digito(linea[i])):
            lexema += linea[i]
            i += 1
        return lexema, i - pos
    return None, 0

def automata_op_doble(linea, pos):
    for op in OPERADORES_DOBLES:
        if linea.startswith(op, pos):
            return op, len(op)
    return None, 0

def automata_op_simple(linea, pos):
    c = linea[pos]
    if c in OPERADORES_SIMPLES:
        return c, 1
    return None, 0

def analizar_linea(linea, nlinea):
    i = 0
    while i < len(linea):
        if linea[i].isspace():
            i += 1
            continue
        if linea[i] == '#':
            break
        token, lon = automata_cadena(linea, i)
        if lon:
            print(f'<tk_cadena,{token},{nlinea},{i+1}>')
            i += lon
            continue
        op, lon = automata_op_doble(linea, i)
        if lon:
            print(f'<{OPERADORES_DOBLES[op]},{nlinea},{i+1}>')
            i += lon
            continue
        op, lon = automata_op_simple(linea, i)
        if lon:
            print(f'<{OPERADORES_SIMPLES[op]},{nlinea},{i+1}>')
            i += lon
            continue
        num, lon = automata_entero(linea, i)
        if lon:
            print(f'<tk_entero,{num},{nlinea},{i+1}>')
            i += lon
            continue
        idn, lon = automata_identificador(linea, i)
        if lon:
            if idn in PALABRAS_RESERVADAS:
                print(f'<{idn},{nlinea},{i+1}>')
            else:
                print(f'<id,{idn},{nlinea},{i+1}>')
            i += lon
            continue
        # Si nada coincide, error léxico
        print(f'>>> Error léxico(linea:{nlinea},posicion:{i+1})')
        break

def analizar_archivo(nombre):
    try:
        f = open(nombre, 'r', encoding='utf-8')
        lineas = f.readlines()
        f.close()
    except:
        print('Error al abrir archivo')
        return
    for n, linea in enumerate(lineas, 1):
        analizar_linea(linea.rstrip('\n'), n)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Uso: python analizador_simple.py archivo.py')
    else:
        analizar_archivo(sys.argv[1])
