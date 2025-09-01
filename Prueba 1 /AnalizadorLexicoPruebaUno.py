
# Analizador léxico basado en autómatas finitos en Python

PALABRAS_RESERVADAS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in',
    'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
    'return', 'try', 'while', 'with', 'yield', 'print'
}

OPERADORES_DOBLES = {
    '->': 'tk_flecha',
    '<=': 'tk_menor_igual',
    '>=': 'tk_mayor_igual',
    '==': 'tk_igual_igual',
    '!=': 'tk_distinto'
}

TOKENS_ESPECIALES = {   
    ':': 'tk_dos_puntos',
    ',': 'tk_coma',
    '.': 'tk_punto',
    '=': 'tk_asig',
    '+': 'tk_suma',
    '-': 'tk_menos',
    '*': 'tk_mult',
    '/': 'tk_div',
    '%': 'tk_mod',
    '(': 'tk_par_izq',
    ')': 'tk_par_der',
    '{': 'tk_llave_izq',
    '}': 'tk_llave_der',
    '[': 'tk_corchete_izq',
    ']': 'tk_corchete_der',
    '<': 'tk_menor',
    '>': 'tk_mayor',
}

def es_letra(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

def es_digito(c):
    return '0' <= c <= '9'

def automata_cadena(linea, inicio):
    estado = 0
    lexema = ''
    i = inicio
    longitud = len(linea)
    comilla = ''
    
    while i < longitud:
        c = linea[i]
        if estado == 0:
            if c == '"' or c == "'":
                comilla = c
                lexema += c
                estado = 1
                i += 1
            else:
                break
        elif estado == 1:
            lexema += c
            if c == '\\':
                # escape, toma siguiente sin evaluarlo
                i += 1
                if i < longitud:
                    lexema += linea[i]
                else:
                    return None, 0  # error
            elif c == comilla:
                i += 1
                return lexema, i - inicio
            i += 1
    return None, 0  # error: cadena no cerrada

def automata_entero(linea, inicio):
    estado = 0
    lexema = ''
    i = inicio
    longitud = len(linea)
    
    while i < longitud:
        c = linea[i]
        if estado == 0:
            if c == '+' or c == '-':
                lexema += c
                estado = 1
                i += 1
            elif es_digito(c):
                lexema += c
                estado = 1
                i += 1
            else:
                break
        elif estado == 1:
            if es_digito(c):
                lexema += c
                i += 1
            else:
                break
    if estado == 1 and len(lexema) > 0 and (lexema[-1].isdigit()):
        return lexema, i - inicio
    else:
        return None, 0  # error o no reconocido

def automata_identificador(linea, inicio):
    estado = 0
    lexema = ''
    i = inicio
    longitud = len(linea)
    
    while i < longitud:
        c = linea[i]
        if estado == 0:
            if es_letra(c):
                lexema += c
                estado = 1
                i += 1
            else:
                break
        elif estado == 1:
            if es_letra(c) or es_digito(c):
                lexema += c
                i += 1
            else:
                break
    if estado == 1:
        return lexema, i - inicio
    return None, 0

def automata_operador_doble(linea, inicio):
    for op, nombre in OPERADORES_DOBLES.items():
        if linea.startswith(op, inicio):
            return op, len(op), nombre
    return None, 0, None

def automata_operador_simple(linea, inicio):
    c = linea[inicio]
    if c in TOKENS_ESPECIALES:
        return c, 1, TOKENS_ESPECIALES[c]
    return None, 0, None

def analizar_linea(linea, linea_num):
    i = 0
    longitud = len(linea)
    while i < longitud:
        c = linea[i]

        if c.isspace():
            i += 1
            continue

        if c == '#':  # comentario, ignora resto línea
            break

        # Probar cadena
        lex, lon = automata_cadena(linea, i)
        if lex:
            print(f'<tk_cadena,{lex},{linea_num},{i+1}>')
            i += lon
            continue

        # Probar operador doble
        lex, lon, tok_name = automata_operador_doble(linea, i)
        if lex:
            print(f'<{tok_name},{linea_num},{i+1}>')
            i += lon
            continue

        # Probar operador simple
        lex, lon, tok_name = automata_operador_simple(linea, i)
        if lex:
            print(f'<{tok_name},{linea_num},{i+1}>')
            i += lon
            continue

        # Probar entero
        lex, lon = automata_entero(linea, i)
        if lex:
            print(f'<tk_entero,{lex},{linea_num},{i+1}>')
            i += lon
            continue

        # Probar identificador o palabra reservada
        lex, lon = automata_identificador(linea, i)
        if lex:
            if lex in PALABRAS_RESERVADAS:
                print(f'<{lex},{linea_num},{i+1}>')
            else:
                print(f'<id,{lex},{linea_num},{i+1}>')
            i += lon
            continue

        # Si no reconoce nada``
        print(f'>>> Error léxico(linea:{linea_num},posicion:{i+1})')
        break

def analizar_archivo(nombre):
    try:
        with open(nombre, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f'Archivo no encontrado: {nombre}')
        return

    for n, linea in enumerate(lineas, start=1):
        analizar_linea(linea.rstrip('\n'), n)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python aut_lexico.py archivo.py")
    else:
        analizar_archivo(sys.argv[1])
