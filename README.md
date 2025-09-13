# Laboratorio 7 - Simplificación de Gramáticas Libres de Contexto

**Curso:** Teoría de la Computación  
**Universidad:** Universidad del Valle de Guatemala  
**Autores:** Joel Antonio Jaquez López (23369) y Juan Francisco Martínez (23617)  
**Fecha:** 2025

## Descripción del Laboratorio

Este laboratorio implementa un algoritmo completo para la eliminación de producciones-ε en gramáticas libres de contexto (CFGs). El programa carga gramáticas desde archivos de texto, valida su formato usando expresiones regulares, y aplica el algoritmo teórico de eliminación de producciones épsilon con generación de combinaciones 2^n.

## Características Principales

- **Validación robusta con regex** - Reutiliza conceptos del Proyecto 1
- **Algoritmo iterativo de punto fijo** - Para encontrar símbolos anulables
- **Generación sistemática 2^n** - Todas las combinaciones posibles
- **Manejo completo de errores** - Detección y reporte de formatos inválidos
- **Salida detallada paso a paso** - Trazabilidad completa del proceso

## Estructura del Código

### Clases Principales

- **`Produccion`** - Representa una regla individual de la gramática
- **`Gramatica`** - Contenedor principal con clasificación automática de símbolos

### Funciones Clave

- **`encontrar_simbolos_anulables()`** - Algoritmo iterativo para identificar símbolos anulables
- **`generar_nuevas_producciones()`** - Implementación del algoritmo 2^n 
- **`eliminar_producciones_epsilon()`** - Coordinador principal del proceso

## Requisitos del Sistema

- Python 3.7+
- Librerías estándar: `sys`, `re`, `itertools`

## Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Cisco890/LabsTeoria.git
cd Ejercicio2/
```

### 2. Preparar archivos de gramática
- gramatica1.txt
- gramatica2.txt

### 3. Ejecutar el programa
```bash
python SimplificacionGramatica.py gramatica1.txt
python SimplificacionGramatica.py gramatica2.txt
```

## Formato de Archivos de Entrada

### Convenciones
- **Mayúsculas** = No-terminales (A, B, C, S)
- **Minúsculas y dígitos** = Terminales (a, b, 0, 1)
- **Flecha** = `→` o `->` 
- **Alternativas** = Separadas por `|`
- **Épsilon** = `ε`

### Ejemplo de formato válido
```
S → aAa | bBb | ε
A → C | a
B → C | b
C → CDE | ε
D → A | B | ab
```

## Algoritmo Implementado

### Paso 1: Encontrar Símbolos Anulables
Algoritmo iterativo que identifica todos los símbolos que pueden derivar en ε:
- **Regla directa:** A → ε implica que A es anulable
- **Regla indirecta:** A → BC donde B y C son anulables implica que A es anulable

### Paso 2: Generar Nuevas Producciones
Para cada producción con n símbolos anulables:
- Genera 2^n combinaciones eliminando subconjuntos de símbolos anulables
- Rechaza combinaciones que resulten en producciones vacías
- Elimina duplicados automáticamente

### Paso 3: Construir Gramática Final
- Elimina todas las producciones-ε originales
- Integra las nuevas producciones generadas
- Preserva el símbolo inicial y la equivalencia del lenguaje

## Ejemplos de Ejecución

### Ejecución Normal
```bash
$ python SimplificacionGramatica.py gramatica1.txt

=== RESULTADO ===
Gramática Original:
  S → 0A0 | 1B1 | ε
  A → C
  B → S | A
  C → S | ε

Gramática sin producciones-ε:
  A → C
  B → S | A
  C → S  
  S → 00 | 0A0 | 1B1 | 11
```

### Validación de Errores
```bash
$ python SimplificacionGramatica.py gramatica1.txt

Gramática Original:
  s → 0A0 | 1B1 | ε
  A → C
  B → S | A
  C → S | ε

Error en linea 1: Formato invalido
Deteniendo ejecucion debido a formato invalido.
```

## Validación de Formato

El programa implementa validación estricta usando expresiones regulares:

```python
patron = r'^[A-Z]\s*(→|->)\s*(([A-Za-z0-9ε]|\s)*(\s*\|\s*([A-Za-z0-9ε]|\s)*)*)\s*$'
```

### Errores Detectados
- Líneas que no inician con mayúscula
- Ausencia de flecha de producción  
- Símbolos inválidos o caracteres especiales
- Formato incorrecto de alternativas

## Archivos del Proyecto

```
laboratorio7-cfg/
├── SimplificacionGramatica.py  # Programa principal
├── gramatica1.txt              # Gramática de prueba 1
├── gramatica2.txt              # Gramática de prueba 2
├── README.md                   # Este archivo
```

# Enlace al video de YouTube
- https://youtu.be/DhZbD-WDtdM
