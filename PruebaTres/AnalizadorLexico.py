# --- Definiciones de tokens ---
PALABRAS_RESERVADAS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
    'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield', 'print','object','str','int','float','bool','list','dict','set','tuple'
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
def es_letra(cadena: str)-> bool: # Esto dectecta letras ASCII
    if len(cadena)==0:
        return False
    return ('a' <= cadena <= 'z') or ('A' <= cadena <= 'Z')

def es_digito(cadena: str)-> bool: # Esto detecta numeros
    if len(cadena)==0:
        return False
    return '0' <= cadena <= '9'

def es_alfnum(cadena: str)-> bool:
    return es_letra(cadena) or es_digito(cadena)

def es_blanco(cadena: str)-> bool:
    return cadena in [' ', '\t', '\n', '\r', '\v', '\f']


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
                elif es_digito(linea[i]):
                    lexema += linea[i]; i += 1; estado = 1
                else: break
            elif estado == 1:
                if es_digito(linea[i]):
                    lexema += linea[i]; i += 1
                else: break
        if estado == 1 and es_digito(lexema[-1]):
            return ('tk_entero', lexema, i-pos)
        return None

class AutomataIdentificador:
    def match(self, linea, pos):
        if not (es_letra(linea[pos]) or linea[pos] == '_'): return None
        lexema, i = '', pos
        while i < len(linea) and (es_alfnum(linea[i]) or linea[i] == '_'):
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

class AnalizadorLexico:
    def __init__(self,salida="tokens.txt"):
        self.automatas = [
            AutomataCadena(), AutomataOpDoble(), AutomataOpSimple(),
            AutomataEntero(), AutomataIdentificador()
        ]
        self.salida=salida
        with open   (self.salida,'w',encoding='utf-8') as f:
            f.write("")
    
    def escribir(self,token):
        with open(self.salida,'a',encoding='utf-8') as f:
            f.write(token+'\n')
    def analizar_linea(self, linea, num_linea):
        i = 0
        while i < len(linea):
            if es_blanco(linea[i]): i += 1; continue
            if linea[i] == '#': break
            for aut in self.automatas:
                res = aut.match(linea, i)
                if res:
                    tipo, lexema, longi = res
                    token=f'<{tipo},{lexema},{num_linea},{i+1}>'
                    self.escribir(token)
                    i += longi; break
            else:
                print(f'>//>//> error lexico(linea:{num_linea},posicion:{i+1})')
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
    if len(sys.argv) != 2:

        print('Agregar un archivo para analizar')
    else: 
        AnalizadorLexico().analizar(sys.argv[1])
