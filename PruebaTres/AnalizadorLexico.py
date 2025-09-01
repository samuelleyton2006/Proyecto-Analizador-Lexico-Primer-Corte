# --- Definiciones de tokens ---
PALABRAS_RESERVADAS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
    'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield', 'print'
}

OPERADORES_DOBLES = {
    '->': 'tk_flecha', '<=': 'tk_menor_igual', '>=': 'tk_mayor_igual',
    '==': 'tk_igual_igual', '!=': 'tk_distinto'
}

OPERADORES_SIMPLES = {
    ':': 'tk_dos_puntos', ',': 'tk_coma', '.': 'tk_punto', '=': 'tk_asig', '+': 'tk_suma',
    '-': 'tk_menos', '*': 'tk_mult', '/': 'tk_div', '%': 'tk_mod', '(': 'tk_par_izq',
    ')': 'tk_par_der', '{': 'tk_llave_izq', '}': 'tk_llave_der', '[': 'tk_corchete_izq',
    ']': 'tk_corchete_der', '<': 'tk_menor', '>': 'tk_mayor'
}

# --- Automatizadores por token ---
class AutomataCadena:
    def match(self, linea, pos):
        if linea[pos] not in ['"',"'"]: return None
        comilla = linea[pos]
        lexema, i = comilla, pos+1
        while i < len(linea):
            if linea[i] == '\\': # escape
                lexema += linea[i]
                if i+1 < len(linea):
                    lexema += linea[i+1]
                    i += 2; continue
                else: break
            if linea[i] == comilla:
                lexema += comilla
                return ('tk_cadena', lexema, i+1-pos)
            lexema += linea[i]
            i += 1
        return None # no cerrada

class AutomataEntero:
    def match(self, linea, pos):
        estado, lexema, i = 0, '', pos
        while i < len(linea):
            if estado == 0:
                if linea[i] in '+-':
                    lexema += linea[i]; i += 1; estado = 0
                    continue
                elif linea[i].isdigit():
                    lexema += linea[i]; i += 1; estado = 1
                else: break
            elif estado == 1:
                if linea[i].isdigit():
                    lexema += linea[i]; i += 1
                else: break
        if estado == 1 and lexema[-1].isdigit():
            return ('tk_entero', lexema, i-pos)
        return None

class AutomataIdentificador:
    def match(self, linea, pos):
        if not (linea[pos].isalpha() or linea[pos] == '_'): return None
        lexema, i = '', pos
        while i < len(linea) and (linea[i].isalnum() or linea[i] == '_'):
            lexema += linea[i]; i += 1
        if lexema in PALABRAS_RESERVADAS:
            return (lexema, lexema, i-pos) # palabra reservada
        else:
            return ('id', lexema, i-pos) # identificador

class AutomataOpDoble:
    def match(self, linea, pos):
        for op, nombre in OPERADORES_DOBLES.items():
            if linea.startswith(op, pos):
                return (nombre, op, len(op))
        return None

class AutomataOpSimple:
    def match(self, linea, pos):
        c = linea[pos]
        if c in OPERADORES_SIMPLES:
            return (OPERADORES_SIMPLES[c], c, 1)
        return None

# --- Analizador principal ---
class AnalizadorLexico:
    def __init__(self):
        self.automatas = [
            AutomataCadena(), AutomataOpDoble(), AutomataOpSimple(),
            AutomataEntero(), AutomataIdentificador()
        ]
    def analizar_linea(self, linea, num_linea):
        i = 0
        while i < len(linea):
            if linea[i].isspace(): i += 1; continue
            if linea[i] == '#': break
            for aut in self.automatas:
                res = aut.match(linea, i)
                if res:
                    tipo, lexema, longi = res
                    print(f'<{tipo},{lexema},{num_linea},{i+1}>')
                    i += longi; break
            else:
                print(f'>>> Error léxico(linea:{num_linea},posicion:{i+1})')
                return

    def analizar(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
        except FileNotFoundError:
            print(f'Archivo no encontrado: {filename}')
            return
        for n, l in enumerate(lineas, 1):
            self.analizar_linea(l.rstrip('\n'), n)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2: print('Uso: python analizador_clases.py archivo.py')
    else: AnalizadorLexico().analizar(sys.argv[1])
