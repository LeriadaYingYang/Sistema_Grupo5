from director.profesores.main import menu_profesores
from director.alumnos.main import menu_alumnos
from director.academico.main import menu_academico
from director.notas.main import menu_notas
from director.asistencias.main import menu_asistencias
from director.pagos.main import menu_pagos

def menu_director():
    while True:
        print("""
==================================================
                 MENÚ DIRECTOR
==================================================

1. Gestión académica
2. Gestión de profesores
3. Gestión de alumnos
4. Gestión de notas
5. Gestión de asistencias
6. Gestión de pagos
7. Cerrar sesión
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_academico()

        elif opcion == "2":
            menu_profesores()

        elif opcion == "3":
            menu_alumnos()

        elif opcion == "4":
            menu_notas()

        elif opcion == "5":
            menu_asistencias()

        elif opcion == "6":
            menu_pagos()

        elif opcion == "7":
            print("\nCerrando sesión del director")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")