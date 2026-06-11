import os # Limpia la pantalla de la consola

def imprimir_titulo(texto):  # Muestra un título centrado con marcos
    ancho = 40
    print("-" * ancho)
    print(texto.center(ancho))
    print("-" * ancho)

def imprimir_menu(opciones):  # Muestra una lista de opciones numeradas
    for numero, opcion in enumerate(opciones, start=1):
        print(f"{numero}. {opcion}")

def pausa():  # Espera que el usuario presione enter
    input("\nPresione Enter para continuar")

def limpiar_pantalla():# Limpia la pantalla de la consola
    os.system("cls" if os.name == "nt" else "clear")