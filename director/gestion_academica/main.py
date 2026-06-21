from director.gestion_academica.carreras import registrar_carrera, editar_carrera, buscar_carrera, ver_carreras, desactivar_carrera
from director.gestion_academica.plantillas import crear_plantilla, editar_plantilla, asignar_carrera_plantilla, ver_plantillas, desactivar_plantilla
from director.gestion_academica.salones import registrar_salon, editar_salon, asignar_plantilla_salon, ver_salones, cerrar_salon
from director.gestion_academica.unidades import registrar_unidad, editar_unidad, asignar_unidad_salon, ver_unidades, desactivar_unidad
from director.gestion_academica.modulos import registrar_modulo, editar_modulo, asignar_modulo_unidad, ver_modulos, desactivar_modulo
from director.utilidades import imprimir_titulo, imprimir_menu


def menu_academico():
    while True:
        imprimir_titulo("GESTIÓN ACADÉMICA")
        imprimir_menu([
            "Gestionar Carreras",
            "Gestionar Plantillas Académicas",
            "Gestionar Salones",
            "Gestionar Unidades / Ciclos",
            "Gestionar Módulos",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_carreras()
        elif opcion == "2":
            menu_plantillas()
        elif opcion == "3":
            menu_salones()
        elif opcion == "4":
            menu_unidades()
        elif opcion == "5":
            menu_modulos()
        elif opcion == "6":
            print("\nVolviendo al menú director")
            break
        else:
            print("Opción inválida.")


def menu_carreras():
    while True:
        imprimir_titulo("GESTIONAR CARRERAS")
        imprimir_menu([
            "Registrar carrera",
            "Editar carrera",
            "Buscar carrera",
            "Ver carreras",
            "Desactivar carrera",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_carrera()
        elif opcion == "2":
            editar_carrera()
        elif opcion == "3":
            buscar_carrera()
        elif opcion == "4":
            ver_carreras()
        elif opcion == "5":
            desactivar_carrera()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


def menu_plantillas():
    while True:
        imprimir_titulo("GESTIONAR PLANTILLAS ACADÉMICAS")
        imprimir_menu([
            "Crear plantilla",
            "Editar plantilla",
            "Asignar carrera a plantilla",
            "Ver plantillas",
            "Desactivar plantilla",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_plantilla()
        elif opcion == "2":
            editar_plantilla()
        elif opcion == "3":
            asignar_carrera_plantilla()
        elif opcion == "4":
            ver_plantillas()
        elif opcion == "5":
            desactivar_plantilla()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


def menu_salones():
    while True:
        imprimir_titulo("GESTIONAR SALONES")
        imprimir_menu([
            "Crear salón",
            "Editar salón",
            "Asignar plantilla al salón",
            "Ver salones",
            "Cerrar salón",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_salon()
        elif opcion == "2":
            editar_salon()
        elif opcion == "3":
            asignar_plantilla_salon()
        elif opcion == "4":
            ver_salones()
        elif opcion == "5":
            cerrar_salon()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


def menu_unidades():
    while True:
        imprimir_titulo("GESTIONAR UNIDADES / CICLOS")
        imprimir_menu([
            "Crear unidad",
            "Editar unidad",
            "Asignar unidad a salón",
            "Ver unidades",
            "Desactivar unidad",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_unidad()
        elif opcion == "2":
            editar_unidad()
        elif opcion == "3":
            asignar_unidad_salon()
        elif opcion == "4":
            ver_unidades()
        elif opcion == "5":
            desactivar_unidad()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


def menu_modulos():
    while True:
        imprimir_titulo("GESTIONAR MÓDULOS")
        imprimir_menu([
            "Crear módulo",
            "Editar módulo",
            "Asignar módulo a unidad",
            "Ver módulos",
            "Desactivar módulo",
            "Volver"
        ])

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_modulo()
        elif opcion == "2":
            editar_modulo()
        elif opcion == "3":
            asignar_modulo_unidad()
        elif opcion == "4":
            ver_modulos()
        elif opcion == "5":
            desactivar_modulo()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")