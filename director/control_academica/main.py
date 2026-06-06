from director.control_academica.configurar_horarios import configurar_horarios
from director.control_academica.asistencia_alumnos import registrar_asistencia_alumnos
from director.control_academica.asistencia_profesores import registrar_asistencia_profesores
from director.control_academica.ver_asistencia_alumnos import menu_ver_asistencia_alumnos
from director.control_academica.horas_profesores import ver_horas_profesores
from director.control_academica.crear_tablilla import crear_tablilla_notas
from director.control_academica.registrar_modificar_notas import registrar_modificar_notas
from director.control_academica.ver_notas import ver_notas_por_unidad
from director.utilidades import imprimir_titulo, imprimir_menu


def menu_control_academico():
    while True:
        imprimir_titulo("CONTROL ACADÉMICO")
        imprimir_menu([
            "Gestión de notas",
            "Gestión de asistencias",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_notas()
        elif opcion == "2":
            menu_asistencias()
        elif opcion == "3":
            print("\nVolviendo al menú director")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_notas():
    while True:
        imprimir_titulo("GESTIÓN DE NOTAS")
        imprimir_menu([
            "Crear Tablilla de Notas",
            "Registrar o Modificar Notas",
            "Ver Notas",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_tablilla_notas()
        elif opcion == "2":
            registrar_modificar_notas()
        elif opcion == "3":
            ver_notas_por_unidad()
        elif opcion == "4":
            print("\nVolviendo a control académico")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_asistencias():
    while True:
        imprimir_titulo("GESTIÓN DE ASISTENCIAS")
        imprimir_menu([
            "Configurar Horarios",
            "Registrar Asistencia de Alumnos",
            "Registrar Asistencia de Profesores",
            "Ver Asistencia de Alumnos",
            "Ver Horas Trabajadas de Profesores",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            configurar_horarios()
        elif opcion == "2":
            registrar_asistencia_alumnos()
        elif opcion == "3":
            registrar_asistencia_profesores()
        elif opcion == "4":
            menu_ver_asistencia_alumnos()
        elif opcion == "5":
            ver_horas_profesores()
        elif opcion == "6":
            print("\nVolviendo a control académico")
            break
        else:
            print("Opción inválida. Intente nuevamente.")