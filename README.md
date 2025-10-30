JEREMY SURIEL 1-20-2049

# 🧠 Analizador Léxico, Sintáctico y Semántico (Mini Compilador)

Este proyecto implementa un **mini compilador** desarrollado en **Python** utilizando la librería **PLY (Python Lex-Yacc)**.
El sistema analiza un archivo fuente en un lenguaje simple de tipo C, realizando las tres fases fundamentales del proceso de compilación:

* **Análisis léxico**
* **Análisis sintáctico (parsing)**
* **Análisis semántico (tipos y declaraciones)**

---

## 📚 Descripción General

El programa lee el contenido de un archivo de texto (`.txt`) que contiene un pequeño fragmento de código fuente y realiza las siguientes tareas:

1. **Analizador léxico:** identifica los tokens (palabras clave, identificadores, números, operadores, etc.).
2. **Analizador sintáctico:** valida la estructura gramatical del programa según las reglas del lenguaje.
3. **Analizador semántico:** verifica la correcta declaración de variables, compatibilidad de tipos y errores de asignación.

El proyecto tiene fines educativos y permite observar cómo interactúan las fases de un compilador real, mostrando:

* Los **tokens** reconocidos.
* Los **errores semánticos** detectados.
* La **tabla de símbolos** final.

---

## 🧩 Lenguaje Soportado

El lenguaje analizado es una versión reducida similar a C, con soporte para:

### Declaraciones

```c
int a;
float b = 3.14;
```

### Asignaciones

```c
a = 5;
b = a + 2.5;
```

### Expresiones

* Suma, resta, multiplicación y división
* Uso de paréntesis
* Variables y números (enteros y flotantes)

### Comentarios

```c
// Esto es un comentario
```

---

## ⚙️ Características Semánticas

El analizador realiza los siguientes **chequeos semánticos**:

| Tipo de Error                | Descripción                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| 🔍 Variable no declarada     | Uso de una variable que no fue declarada previamente         |
| ⚠️ Redeclaración             | Intentar declarar una variable con un nombre ya existente    |
| 🚫 Incompatibilidad de tipos | Asignar un valor `float` a una variable `int` (no permitido) |
| ✅ Promoción automática       | Asignar un `int` a un `float` es permitido                   |

---

## 🧰 Requisitos

Asegúrate de tener instalado **Python 3.x** y **PLY**:

```bash
pip install ply
```

---

## 🚀 Ejecución

1. Crea un archivo fuente, por ejemplo **`programa.txt`**, con el siguiente contenido:

```c
// Ejemplo de prueba
int a;
float b = 3.14;
a = 5;
b = a + 2.5;
c = 4;        // variable no declarada
int a;        // redeclaración
a = 3.14;     // error: float -> int (no permitido)
```

2. Ejecuta el analizador desde la terminal:

```bash
python compiler.py programa.txt
```

3. El programa mostrará:

* El código de entrada
* Los **tokens** reconocidos
* Los **errores semánticos** detectados
* La **tabla de símbolos** generada

---

## 🧾 Ejemplo de Salida

```
=== ENTRADA ===
// Ejemplo de prueba
int a;
float b = 3.14;
a = 5;
b = a + 2.5;
c = 4;        // variable no declarada
int a;        // redeclaración
a = 3.14;     // error: float -> int (no permitido)
=============

Tokens (análisis léxico):
  Línea 2, col 1: INT_KW -> int
  Línea 2, col 5: ID -> a
  Línea 2, col 6: SEMI -> ;
  ...
  
Errores semánticos/de tipo:
  Línea 14: Variable no declarada 'c'
  Línea 15: Redeclaración de la variable 'a' (declarada previamente en la línea 10)
  Línea 16: Error de tipo: no se puede asignar una expresión de tipo float a la variable 'a' de tipo int

Tabla de símbolos:
  a : int   (declarada en la línea 10)
  b : float (declarada en la línea 11)
```

---

## 🧠 Estructura del Proyecto

```
AnalizadorSemanticoCompilador/
│
├── compiler.py          # Código fuente principal
├── programa.txt         # Ejemplo de programa de entrada
└── README.md            # Este documento
```

---

## 🧩 Componentes Principales del Código

* **Sección Léxica:** definición de tokens y expresiones regulares (`t_ID`, `t_NUM_INT`, etc.)
* **Sección Sintáctica:** gramática del lenguaje (`stmt`, `decl`, `expression`, etc.)
* **Sección Semántica:** verificación de tipos y control de la tabla de símbolos
* **Salida:** reporte legible con errores semánticos y resumen de variables declaradas

---

## 🎓 Propósito Académico

Este proyecto forma parte de la **asignatura de Compiladores**, y tiene como objetivo comprender y aplicar los conceptos de:

* Análisis léxico
* Análisis sintáctico
* Análisis semántico
* Construcción de un compilador básico

---

## ✍️ Autor

**Nombre:** Jeremy Suriel
**Matricula:** 1-20-2049
**Materia:** Compiladores
**Universidad:** UTESA
**Periodo:** Septiembre – Diciembre 2025

---
