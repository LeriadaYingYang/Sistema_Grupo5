import os

ANCHO_TITULO = 40

def imprimir_titulo(texto):  # muestra un título centrado con marcos
    print("-" * ANCHO_TITULO)
    print(texto.center(ANCHO_TITULO))
    print("-" * ANCHO_TITULO)

def imprimir_menu(opciones):  # muestra una lista de opciones numeradas
    for numero, opcion in enumerate(opciones, start=1):
        print(f"{numero}. {opcion}")

def pausa():  # espera que el usuario presione enter
    input("\nPresione Enter para continuar")

def limpiar_pantalla():  # limpia la pantalla de la consola
    os.system("cls" if os.name == "nt" else "clear")

def pedir_entero(mensaje):  # solicita un número entero al usuario y lo retorna, o None si es inválido
    try:
        return int(input(mensaje))
    except ValueError:
        print("Error: debe ingresar un número entero.")
        return None

def validar_no_vacio(valor, nombre_campo):  # valida que un campo no esté vacío
    if not valor.strip():
        print(f"Error: el campo '{nombre_campo}' no puede estar vacío.")
        return False
    return True
