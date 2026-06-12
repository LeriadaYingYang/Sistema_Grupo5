from director.control_academica.asistencia_alumnos import registrar_asistencia_alumnos
from director.control_academica.asistencia_profesores import registrar_asistencia_profesores
from director.control_academica.consultar_asistencia_alumnos import consultar_asistencia_alumnos
from director.control_academica.consultar_asistencia_profesores import consultar_asistencia_profesores
from director.control_academica.reporte_inasistencias import reporte_inasistencias
from director.utilidades import imprimir_titulo, imprimir_menu


def menu_control_academico():
    while True:
        imprimir_titulo("CONTROL ACADÉMICO")
        imprimir_menu([
            "Gestión de asistencias",
            "Volver"
        ])
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_asistencias()
        elif opcion == "2":
            print("\nVolviendo al menú director")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def menu_asistencias():
    while True:
        imprimir_titulo("GESTIÓN DE ASISTENCIAS")
        imprimir_menu([
            "Registrar asistencia de alumnos",
            "Registrar asistencia de profesores",
            "Consultar asistencia de alumnos",
            "Consultar asistencia de profesores",
            "Reporte de inasistencias",
            "Volver"
        ])
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_asistencia_alumnos()
        elif opcion == "2":
            registrar_asistencia_profesores()
        elif opcion == "3":
            consultar_asistencia_alumnos()
        elif opcion == "4":
            consultar_asistencia_profesores()
        elif opcion == "5":
            reporte_inasistencias()
        elif opcion == "6":
            print("\nVolviendo a control académico")
            break
        else:
            print("Opción inválida. Intente nuevamente.")