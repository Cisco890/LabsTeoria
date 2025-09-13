#################################################################################################################
# Joel Antonio Jaquez López - 23369  y Juan Francisco Martínez - 23617                                           #
# Laboratorio 7 - Simplificación de Gramáticas                                                                  #
#################################################################################################################

import sys
import re
from itertools import combinations

class Produccion:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda # (No terminal)
        self.derecha = derecha # Lista de simbolos

    def __str__(self):
        derecha_str = ' '.join(self.derecha) if self.derecha else 'ε'
        return f"{self.izquierda} -> {derecha_str}"
    
    def __repr__(self):
        return self.__str__()

# Representa una gramatica libre de contexto
class Gramatica:
    def __init__(self):
        self.producciones = [] # Lista de producciones
        self.no_terminales = set() # Conjunto de no terminales
        self.terminales = set() # Conjunto de terminales
        self.simbolo_inicial = None # Simbolo inicial

    # Agrega una produccion a la gramatica
    def agregar_produccion(self, produccion):
        self.producciones.append(produccion)
        self.no_terminales.add(produccion.izquierda)

        # Si es la primera produccion, el lado izquierdo es el simbolo inicial
        if self.simbolo_inicial is None:
            self.simbolo_inicial = produccion.izquierda

        # Ahora clasificamos los simbolos del lado derecho
        for simbolo in produccion.derecha:
            if simbolo != 'ε':
                if simbolo.isupper():
                    self.no_terminales.add(simbolo)
                elif simbolo.islower() or simbolo.isdigit():
                    self.terminales.add(simbolo)
    
    # Funcion que muestra la gramatica organizada
    def mostrar(self, titulo="Gramatica"):
        print(f"\n===== {titulo} ======")
        print(f"Simbolo inicial: {self.simbolo_inicial}")
        print(f"No terminales: {sorted(self.no_terminales)}")
        print(f"Terminales: {sorted(self.terminales)}")
        print("Producciones:")

        # Agrupamos las producciones por no terminal
        producciones_agrupadas = {}
        for prod in self.producciones:
            if prod.izquierda not in producciones_agrupadas:
                producciones_agrupadas[prod.izquierda] = []
            producciones_agrupadas[prod.izquierda].append(prod.derecha)
        
        for no_terminal in sorted(producciones_agrupadas.keys()):
            derechas = producciones_agrupadas[no_terminal]
            derechas_str = []
            for derecha in derechas:
                if derecha == ['ε'] or derecha == []:
                    derechas_str.append('ε')
                else:
                    derechas_str.append(''.join(derecha))
            print(f"  {no_terminal} -> {' | '.join(derechas_str)}")

    # Funcion que valida una linea de produccion usando regex
    @staticmethod 
    def validar_formato_produccion(linea):
        linea = linea.strip()
        patron = r'^[A-Z]\s*(→|->)\s*(([A-Za-z0-9ε]|\s)*(\s*\|\s*([A-Za-z0-9ε]|\s)*)*)\s*$'

        if not re.match(patron, linea):
            return False, f"Formato invalido"
        
        if '→' not in linea and '->' not in linea:
            return False, f"Falta el simbolo de produccion '→' o '->'"
        
        return True, "Formato valido"

    # Convierte una linea de texto en una produccion
    @staticmethod
    def parsear_produccion(linea):
        linea = linea.strip()

        if '→' in linea:
            izquierda, derecha = linea.split('→', 1)
        else:
            izquierda, derecha = linea.split('->', 1)
        
        izquierda = izquierda.strip()
        derecha = derecha.strip()

        # Separar por |
        alternativas = [alt.strip() for alt in derecha.split('|')]

        producciones = []
        for alternativa in alternativas:
            if alternativa == 'ε' or alternativa == '':
                # Produccion epsilon
                prod = Produccion(izquierda, ['ε'])
            else:
                # Convertir string a lista de simbolos
                simbolos = list(alternativa.replace(' ', ''))
                prod = Produccion(izquierda, simbolos)
            producciones.append(prod)
        
        return producciones
    
    @staticmethod
    def cargar_gramatica_desde_archivo(nombre_archivo):
        gramatica = Gramatica()
        try:
            print(f"\n===== Cargando gramatica desde '{nombre_archivo}' ======")
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                for numero_linea, linea in enumerate(archivo, start=1):
                    linea = linea.strip()

                    if not linea:
                        continue

                    print(f"Linea {numero_linea}: '{linea}'")
                    
                    es_valido, mensaje = Gramatica.validar_formato_produccion(linea)
                    if not es_valido:
                        print(f"Error en linea {numero_linea}: {mensaje}")
                        print(f"Deteniendo ejecucion debido a formato invalido.")
                        sys.exit(1)
                    
                    producciones = Gramatica.parsear_produccion(linea)
                    for prod in producciones:
                        gramatica.agregar_produccion(prod)
                    
            print(f"Gramatica cargada exitosamente.")
            return gramatica
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no se encontro.")
            sys.exit(1)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            sys.exit(1)
    
# Funcion para encontrar todos los simbolos que pueden derivar en epsilon
def encontrar_simbolos_anulables(gramatica):
    print("\n===== Paso 1: Enontrar simbolos anulables ======")

    anulables = set()
    cambio = True
    iteracion = 0

    while cambio:
        iteracion += 1
        print(f"\nIteracion {iteracion}:")

        cambio = False
        nuevos_anulables = set()

        for prod in gramatica.producciones:
            if prod.derecha == ['ε']:
                if prod.izquierda not in anulables:
                    nuevos_anulables.add(prod.izquierda)
                    cambio = True
                    print(f"  - {prod.izquierda} es anulable por produccion {prod}")
            
            elif all(simbolo in anulables for simbolo in prod.derecha if simbolo != 'ε'):
                if prod.izquierda not in anulables:
                    nuevos_anulables.add(prod.izquierda)
                    cambio = True
                    simbolos_str = ''.join(prod.derecha)
                    print(f"  - {prod.izquierda} es anulable porque todos los simbolos en {simbolos_str} son anulables")
        anulables.update(nuevos_anulables)

        if nuevos_anulables:
            print(f"  Nuevos simbolos anulables encontrados en esta iteracion: {sorted(nuevos_anulables)}")
            
        print(f"  Anulables totales hasta ahora: {sorted(anulables)}")

    print(f"\nSimbolos anulables finales: {sorted(anulables)}")
    return anulables
    
# Funcion que genera las nuevas producciones sin epsilon
def generar_nuevas_producciones(gramatica, anulables):
    print("\n===== Paso 2: Generar nuevas producciones sin epsilon ======")

    nuevas_producciones = []

    for i, prod in enumerate(gramatica.producciones):
        print(f"\nProcesando produccion {i+1}: {prod}")

        if prod.derecha == ['ε']:
            print(f"Eliminando produccion-ε: {prod}")
            continue

        posiciones_anulables = []
        for j, simbolo in enumerate(prod.derecha):
            if simbolo in anulables:
                posiciones_anulables.append(j)
            
        if not posiciones_anulables:
            nuevas_producciones.append(prod)
            print(f"  No hay simbolos anulables en {prod.derecha}, manteniendo produccion: {prod}")
        else:
            print(f"  Simbolos anulables en posiciones {posiciones_anulables}")

            # Generar todas las combinaciones posibles (2^n)
            n = len(posiciones_anulables)
            print(f" Generando {2**n} combinaciones:")

            producciones_generadas = set()

            for r in range(n + 1):
                for combo in combinations(posiciones_anulables, r):

                    nueva_derecha = []
                    for j, simbolo in enumerate(prod.derecha):
                        if j not in combo:
                            nueva_derecha.append(simbolo)
                        
                    if nueva_derecha:
                        nueva_prod_tupla = (prod.izquierda, tuple(nueva_derecha))
                        producciones_generadas.add(nueva_prod_tupla)
                        combo_str = f"eliminado pos {list(combo)}" if combo else "original"
                        print(f"    {prod.izquierda} → {''.join(nueva_derecha)} ({combo_str})")

            for izq, der in producciones_generadas:
                nueva_prod = Produccion(izq, list(der))
                nuevas_producciones.append(nueva_prod)

    print(f"\nTotal nuevas producciones generadas: {len(nuevas_producciones)}")
    return nuevas_producciones
    
# Algoritmo para eliminar producciones epsilon
def eliminar_producciones_epsilon(gramatica):
    print("========================")
    print("Eliminacion de producciones ε")
    print("========================")

    gramatica.mostrar("Gramatica Original")

    # Paso 1: Encontrar simbolos anulables
    anulables = encontrar_simbolos_anulables(gramatica)

    # Paso 2: Generar nuevas producciones sin epsilon
    nuevas_producciones = generar_nuevas_producciones(gramatica, anulables)

    # Paso 3: Construir nueva gramatica sin producciones ε
    nueva_gramatica = Gramatica()
    nueva_gramatica.simbolo_inicial = gramatica.simbolo_inicial

    for prod in nuevas_producciones:
        nueva_gramatica.agregar_produccion(prod)
        
    return nueva_gramatica
    
# Funcion principal para manejar la ejecucion del programa
def main():
    print("=================================================================")
    print("Laboratorio 7 - Simplificacion de Gramaticas Libres de Contexto")
    print("=================================================================")

    if len(sys.argv) != 2:
        print("Uso: python SimplificacionGramatica.py <archivo_gramatica>")
        print("Ejemplo: python SimplificacionGramatica.py gramatica.txt")
        sys.exit(1)
    nombre_archivo = sys.argv[1]

    try:
        # Cargar la gramatica desde el archivo
        gramatica_original = Gramatica.cargar_gramatica_desde_archivo(nombre_archivo)

        # Mostrar la gramatica cargada
        gramatica_original.mostrar("Gramatica Cargada")

        # Eliminar producciones epsilon
        gramatica_sin_epsilon = eliminar_producciones_epsilon(gramatica_original)
        gramatica_sin_epsilon.mostrar("Gramatica sin producciones ε")

        print(f"Producciones originales: {len(gramatica_original.producciones)}")
        print(f"Producciones finales: {len(gramatica_sin_epsilon.producciones)}")
        
    except KeyboardInterrupt:
        print("\nEjecucion interrumpida por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
                                

