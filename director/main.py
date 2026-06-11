from director.profesores.main import menu_profesores
from director.alumnos.main import menu_alumnos
from director.academico.main import menu_academico
from director.notas.main import menu_notas
from director.asistencias.main import menu_asistencias
from director.pagos.main import menu_pagos
from director.utilidades import imprimir_titulo, imprimir_menu

def menu_director():  #muestra el menú principal del director y permite acceder a todos los módulos del sistema
    while True:
        imprimir_titulo("MENÚ DIRECTOR")
        imprimir_menu(["Gestión académica", "Gestión de profesores", "Gestión de alumnos",
                      "Gestión de notas","Gestión de asistencias", "Gestión de pagos", "Cerrar sesión"])

        opcion = input("Seleccione una opción: ")  #xsolicita la opción que desea ejecutar el director
        if opcion == "1":  #abre el módulo académico para gestionar carreras, plantillas, módulos y salones
            menu_academico()
        elif opcion == "2":  #abre el módulo para registrar, asignar y administrar profesores
            menu_profesores()
        elif opcion == "3":  #abre el módulo para registrar, asignar y administrar alumnos
            menu_alumnos()
        elif opcion == "4":  #abre el módulo de creación, registro y consulta de notas académicas
            menu_notas()
        elif opcion == "5":  #abre el módulo para configurar horarios y registrar asistencias
            menu_asistencias()
        elif opcion == "6":  #abre el módulo para administrar cargos, descuentos y pagos
            menu_pagos()
        elif opcion == "7":  #finaliza la sesión del director y regresa al menú principal del sistema
            print("\nCerrando sesión del director")
            break
        else:  #muestra mensaje cuando la opción ingresada no existe en el menú
            print("\nOpción inválida. Intente nuevamente.")