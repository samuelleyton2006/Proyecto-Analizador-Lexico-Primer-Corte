import re
import sys

# Listado de palabras reservadas de Python (case sensitive)
PALABRAS_RESERVADAS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
    'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    'print',  # aunque print es función, se pide como reservada
}

# Operadores y símbolos especiales con su token asociado (tk_nombre)
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
    '<=': 'tk_menor_igual',
    '>=': 'tk_mayor_igual',
    '==': 'tk_igual_igual',
    '!=': 'tk_distinto',
    '->': 'tk_flecha',
    '#': 'tk_comentario',
}

# Patrón tokens regulares, listados en orden para respetar subcadena más larga
TOKEN_REGEX = [
    ('tk_flecha', r'->'),
    ('tk_menor_igual', r'<='),
    ('tk_mayor_igual', r'>='),
    ('tk_igual_igual', r'=='),
    ('tk_distinto', r'!='),
    ('tk_dos_puntos', r':'),
    ('tk_coma', r','),
    ('tk_punto', r'\.'),
    ('tk_asig', r'='),
    ('tk_suma', r'\+'),
    ('tk_menos', r'-'),
    ('tk_mult', r'\*'),
    ('tk_div', r'/'),
    ('tk_mod', r'%'),
    ('tk_par_izq', r'\('),
    ('tk_par_der', r'\)'),
    ('tk_llave_izq', r'\{'),
    ('tk_llave_der', r'\}'),
    ('tk_corchete_izq', r'\['),
    ('tk_corchete_der', r'\]'),
    ('tk_menor', r'<'),
    ('tk_mayor', r'>'),
]

# Expresiones regulares para tokens específicos
RE_IDENTIFICADOR = r'[A-Za-z_][A-Za-z0-9_]*'
RE_ENTERO = r'[+-]?\d+'
RE_CADENA = r'(\"([^\\\"]|\\.)*\"|\'([^\\\']|\\.)*\')'

# Función para eliminar comentarios (ignorarlos)
def eliminar_comentarios(linea):
    pos = linea.find('#')
    if pos != -1:
        return linea[:pos]
    return linea

def analizar_lexico(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f'No se encontró el archivo: {ruta_archivo}')
        return

    linea_num = 0
    for linea in lineas:
        linea_num += 1
        columna = 1
        texto = eliminar_comentarios(linea.rstrip('\n').rstrip('\r'))

        while texto:
            # Eliminar espacios al inicio
            if texto[0].isspace():
                texto = texto[1:]
                columna += 1
                continue

            # Detectar cadena literal
            m = re.match(RE_CADENA, texto)
            if m:
                lexema = m.group(0)
                print(f'<tk_cadena,{lexema},{linea_num},{columna}>')
                # avanzar texto y columna
                longitud = len(lexema)
                texto = texto[longitud:]
                columna += longitud
                continue

            # Detectar entero
            m = re.match(RE_ENTERO, texto)
            if m:
                lexema = m.group(0)
                # Para signo + o - solo se acepta si seguido de dígitos
                # Ya contemplado en la regex
                print(f'<tk_entero,{lexema},{linea_num},{columna}>')
                longitud = len(lexema)
                texto = texto[longitud:]
                columna += longitud
                continue

            # Detectar palabras reservadas y identificadores
            m = re.match(RE_IDENTIFICADOR, texto)
            if m:
                lexema = m.group(0)
                if lexema in PALABRAS_RESERVADAS:
                    # Palabra reservada debe imprimirse solo como token y posición
                    print(f'<{lexema},{linea_num},{columna}>')
                else:
                    print(f'<id,{lexema},{linea_num},{columna}>')
                longitud = len(lexema)
                texto = texto[longitud:]
                columna += longitud
                continue

            # Detectar operadores y símbolos especiales, respetando subcadena más larga
            emparejado = False
            for tok_nombre, tok_patron in TOKEN_REGEX:
                m = re.match(tok_patron, texto)
                if m:
                    lexema = m.group(0)
                    print(f'<{tok_nombre},{linea_num},{columna}>')
                    longitud = len(lexema)
                    texto = texto[longitud:]
                    columna += longitud
                    emparejado = True
                    break
            if emparejado:
                continue

            # Si llega aquí, no pudo reconocer token -> error léxico
            print(f'>>> Error léxico(linea:{linea_num},posicion:{columna})')
            return

# Código principal para ejecución directa
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analizador_lexico.py archivo_fuente.py")
        sys.exit(1)
    archivo_entrada = sys.argv[1]
    analizar_lexico(archivo_entrada)
