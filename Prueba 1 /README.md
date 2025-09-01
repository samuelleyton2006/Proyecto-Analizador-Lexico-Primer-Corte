Componentes principales
1. Conjuntos y diccionarios
	•	`PALABRAS_RESERVADAS`: conjunto con todas las palabras reservadas de Python que el analizador debe detectar específicamente.
	•	`OPERADORES_DOBLES` y `TOKENS_ESPECIALES`: definiciones para operadores de uno y dos caracteres, cada uno con su token nombre.
2. Funciones auxiliares para verificar caracteres
	•	`es_letra(c)`: devuelve `True` si `c` es una letra o guion bajo, para reconocer el inicio de identificadores.
	•	`es_digito(c)`: devuelve `True` si `c` es un dígito del 0 al 9.
3. Autómatas para cada tipo de token
Cada función `automata_` simula un autómata finito con estados y transiciones mediante variables `estado`, recorriendo caracteres de la línea a partir de un índice `inicio`:
	•	`automata_cadena(linea, inicio)`: Detecta cadenas que empiezan y terminan con comillas (simples o dobles), manejando escapes.
	•	Estado 0: espera comilla inicial.
	•	Estado 1: lee caracteres incluyendo escapes, hasta encontrar la comilla final o error.
	•	`automata_entero(linea, inicio)`: Detecta números enteros con signo opcional.
	•	Estado 0: espera signo o dígito inicial.
	•	Estado 1: atraviesa dígitos hasta que aparezca otro caracter o final de línea.
	•	`automata_identificador(linea, inicio)`: Detecta identificadores y palabras reservadas.
	•	Estado 0: espera letra o guion bajo inicial.
	•	Estado 1: lee letras y dígitos mientras pueda para formar el lexema.
•	`automata_operador_doble(linea, inicio)`: Busca coincidencia con operadores dobles en la posición actual.
	•	Simplemente verifica si alguno de los operadores dobles está presente en esa posición.
	•	`automata_operador_simple(linea, inicio)`: Detecta operadores o símbolos simples de un solo carácter.
4. Función principal `analizar_linea`
	•	Procesa una línea completa desde el índice 0 hacia adelante.
	•	Omite espacios.
	•	Ignora comentarios (`#` y lo que sigue).
	•	Intenta en orden cada autómata para detectar tokens.
	•	Primero prueba cadenas.
	•	Luego operadores dobles.
	•	Luego operadores simples.
	•	Luego enteros.
	•	Finalmente identificadores o palabras reservadas.
	•	Cuando un autómata acepta un token, este se imprime con el formato pedido y el índice de lectura avanza.
	•	Si ningún autómata reconoce, se imprime error léxico con ubicación precisa y termina el análisis de esa línea.
5. Función `analizar_archivo`
	•	Abre el archivo fuente.
	•	Lee línea a línea llamando a `analizar_linea`.
	•	Reporta tokens o errores línea por línea.
6. Parte ejecutable principal
	•	Permite ejecutar el analizador desde línea de comandos pasando como argumento el archivo Python a analizar.
Ventajas de este diseño
•	Claramente modular: cada autómata implementa la lógica para un token específico.
	•	Control total de las transiciones de estado mediante programación imperativa.
	•	Fácil de mantener, extender o modificar cada autómata por separado.
	•	Formato de salida específico compatible con evaluaciones académicas.
	•	Sin librerías externas, perfecto para entender la teoría de compiladores desde la base.
