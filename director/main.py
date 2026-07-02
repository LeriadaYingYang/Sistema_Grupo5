from director.gestion_academica.main import menu_academico
from director.control_administrativa.main import menu_pagos
from director.utilidades import imprimir_titulo, imprimir_menu

def menu_director():
    while True:
        imprimir_titulo("MENÚ DIRECTOR")
        imprimir_menu([
            "Gestión académica",
            "Control académico",
            "Gestión docente",
            "Gestión estudiantil",
            "Gestion y Control administrativo",
            "Cerrar sesión"])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_academico()


        elif opcion == "5":
            menu_pagos()

        elif opcion == "6":
            print("\nCerrando sesión del director")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")