from director.gestion_docente.main import menu_profesores
from director.gestion_estudiante.main import menu_alumnos
from director.gestion_academica.main import menu_academico
from director.control_academica.main import menu_control_academico
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
            "Control administrativo",
            "Cerrar sesión"])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_academico()

        elif opcion == "2":
            menu_control_academico()

        elif opcion == "3":
            menu_profesores()

        elif opcion == "4":
            menu_alumnos()

        elif opcion == "5":
            menu_pagos()

        elif opcion == "6":
            print("\nCerrando sesión del director")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")