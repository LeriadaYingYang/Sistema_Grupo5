from director.control_academica.gestion_horarios.configurar_horarios import configurar_horarios
from director.control_academica.gestion_horarios.modificar_horarios import modificar_horarios
from director.control_academica.gestion_horarios.consultar_horarios import consultar_horarios
from director.control_academica.gestion_horarios.asignar_horarios import asignar_horarios_profesores
from director.control_academica.gestion_horarios.ver_carga_horaria import ver_carga_horaria_docente
from director.control_academica.gestion_asistencia.asistencia_alumnos import registrar_asistencia_alumnos
from director.control_academica.gestion_asistencia.asistencia_profesores import registrar_asistencia_profesores
from director.control_academica.gestion_asistencia.consultar_asistencia_alumnos import consultar_asistencia_alumnos
from director.control_academica.gestion_asistencia.consultar_asistencia_profesores import consultar_asistencia_profesores
from director.control_academica.gestion_asistencia.reporte_inasistencias import reporte_inasistencias
from director.control_academica.seguimiento_academico.ver_notas_modulo import ver_notas_modulo
from director.control_academica.seguimiento_academico.ver_notas_unidad import ver_notas_unidad
from director.control_academica.seguimiento_academico.consultar_rendimiento import consultar_rendimiento_academico
from director.control_academica.seguimiento_academico.alumnos_bajos import alumnos_bajo_rendimiento
from director.control_academica.seguimiento_academico.reporte_general import reporte_academico_general
from director.control_academica.control_docente.ver_horas import ver_horas_trabajadas
from director.control_academica.control_docente.control_carga_horaria import control_carga_horaria
from director.control_academica.control_docente.reporte_asistencia import reporte_asistencia_docente
from director.control_academica.control_docente.faltas import profesores_con_faltas
from director.control_academica.control_docente.resumen import resumen_desempeno_docente
from director.utilidades import imprimir_titulo,imprimir_menu,pausa,limpiar_pantalla


def menu_control_academico():

    while True:
        limpiar_pantalla()
        imprimir_titulo("CONTROL ACADÉMICO")
        imprimir_menu([
            "Gestión de Horarios",
            "Gestión de Asistencias",
            "Seguimiento Académico",
            "Control de Docente",
            "Volver"
        ])
        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            menu_gestion_horarios()
        elif opcion == "2":
            menu_gestion_asistencias()
        elif opcion == "3":
            menu_seguimiento_academico()
        elif opcion == "4":
            menu_control_docente()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")
            pausa()


def menu_gestion_horarios():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE HORARIOS")
        imprimir_menu([
            "Configurar horarios",
            "Modificar horarios",
            "Consultar horarios",
            "Asignar horarios a profesores",
            "Ver carga horaria docente",
            "Volver"
        ])
        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            configurar_horarios()
        elif opcion == "2":
            modificar_horarios()
        elif opcion == "3":
            consultar_horarios()
        elif opcion == "4":
            asignar_horarios_profesores()
        elif opcion == "5":
            ver_carga_horaria_docente()
        elif opcion == "6":
            break
        pausa()

def menu_gestion_asistencias():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE ASISTENCIAS")
        imprimir_menu([
            "Registrar asistencia de alumnos",
            "Registrar asistencia de profesores",
            "Consultar asistencia de alumnos",
            "Consultar asistencia de profesores",
            "Reporte de inasistencias",
            "Volver"
        ])
        opcion = input("\nSeleccione una opción: ")
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
            break
        pausa()


def menu_seguimiento_academico():
    while True:
        limpiar_pantalla()
        imprimir_titulo("SEGUIMIENTO ACADÉMICO")
        imprimir_menu([
            "Ver notas por módulo",
            "Ver notas por unidad",
            "Consultar rendimiento académico",
            "Alumnos con bajo rendimiento",
            "Reporte académico general",
            "Volver"
        ])
        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            ver_notas_modulo()
        elif opcion == "2":
            ver_notas_unidad()
        elif opcion == "3":
            consultar_rendimiento_academico()
        elif opcion == "4":
            alumnos_bajo_rendimiento()
        elif opcion == "5":
            reporte_academico_general()
        elif opcion == "6":
            break
        pausa()


def menu_control_docente():
    while True:
        limpiar_pantalla()
        imprimir_titulo("CONTROL DOCENTE")
        imprimir_menu([
            "Ver horas trabajadas",
            "Control de carga horaria",
            "Reporte de asistencia docente",
            "Profesores con faltas",
            "Resumen de desempeño docente",
            "Volver"
        ])
        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":
            ver_horas_trabajadas()
        elif opcion == "2":
            control_carga_horaria()
        elif opcion == "3":
            reporte_asistencia_docente()
        elif opcion == "4":
            profesores_con_faltas()
        elif opcion == "5":
            resumen_desempeno_docente()
        elif opcion == "6":
            break
        pausa()