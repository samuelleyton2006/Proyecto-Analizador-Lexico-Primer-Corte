1. Estructura modular:
	•	Cada tipo de token tiene su propio autómata finito determinista como clase.
	•	El método `.match()` procesa estado por estado, solo usando condicionales y bucles.
2. Analizador principal:
	•	Se crea la lista de autómatas ordenados por prioridad.
	•	Para cada posición de la línea, se consulta cada autómata.
	•	El primero que acepta, avanza el índice y muestra el token.
	•	Si ninguno acepta, se muestra error léxico.
3. Manejo de comentarios y espacios:
	•	Si encuentra espacio, avanza.
	•	Si encuentra `#`, ignora el resto de la línea.
4. Salida:
	•	El resultado incluye tipo de token, lexema, línea y columna, igual que el otro programa.
¿Cómo lo diseñé?
	•	Separé la lógica de cada tipo de token en clases propias, simulando la teoría de autómatas finitos.
	•	Priorizo autómatas: primero cadenas, luego operadores dobles, operadores simples, números y por último identificadores/reservadas.
	•	Cada `.match()` maneja estados con variables locales, sin variables globales.
	•	El proceso es lineal y determinista: no hay ambigüedad, cada autómata acepta o rechaza la secuencia según la definición clásica de AFD.
	•	El analizador principal solo gestiona el ciclo y la llamada por orden.
