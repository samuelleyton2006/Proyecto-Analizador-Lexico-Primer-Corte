Explicación de cómo se hizo y cómo funciona
Diseño
	•	Muy directo: Cada tipo de token tiene su propia función autónoma que simula un autómata finito por estados usando bucles y condicionales.
	•	Sin clases ni estructuras sofisticadas: Todo son funciones y diccionarios.
	•	Secuencia simple: El analizador recorre cada línea y en cada posición va probando los autómatas en orden de prioridad (cadenas > operadores dobles > operadores simples > enteros > identificadores > error).
Funcionamiento
	1.	Lectura de líneas de código: El programa abre el archivo y lee cada línea.
	2.	Por cada línea: Recorre los caracteres desde el principio, ignorando espacios.
	3.	Manejo de comentarios: Detiene el análisis de la línea cuando encuentra `#`.
	4.	Prueba de tokens:
	•	Prueba si hay una cadena con `automata_cadena`.
	•	Prueba un operador doble.
	•	Prueba un operador simple.
	•	Prueba un entero.
	•	Prueba un identificador o palabra reservada.
	5.	Registro de tokens:
	•	Cuando detecta un token, lo imprime en formato `<tipo,lexema,linea,columna>`.
	•	Avanza la posición según la longitud del token encontrado.
	6.	Detección de error léxico: Si ningún automata reconoce el símbolo actual, imprime error léxico y termina el análisis de esa línea.
 Resultado
	•	Es un código sencillo, fácil de leer y entender, pero sigue la lógica de autómatas finitos deterministas para cada tipo de token.
	•	Ideal para entregar en semestres iniciales, pues no emplea clases ni estructuras complejas, sólo funciones, bucles y condicionales.
