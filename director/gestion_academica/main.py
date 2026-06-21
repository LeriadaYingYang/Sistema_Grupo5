from director.gestion_academica.carreras import registrar_carrera, editar_carrera, buscar_carrera, ver_carreras, desactivar_carrera, activar_carrera
from director.gestion_academica.plantillas import crear_plantilla, editar_plantilla, asignar_carrera_plantilla, ver_plantillas, desactivar_plantilla,activar_plantilla
from director.gestion_academica.salones import registrar_salon, editar_salon, asignar_plantilla_salon, ver_salones, desactivar_salon, activar_salon
from director.gestion_academica.unidades import registrar_unidad, editar_unidad, ver_unidades, desactivar_unidad, activar_unidad
from director.gestion_academica.modulos import registrar_modulo, editar_modulo, ver_modulos, desactivar_modulo
from director.utilidades import imprimir_titulo, imprimir_menu


def leer_opcion(maximo):  #valida que la opción ingresada sea numérica y esté dentro del rango
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))

            if 1 <= opcion <= maximo:
                return opcion

            print("Opción fuera de rango.")
        except ValueError:
            print("Debe ingresar un número válido.")

def menu_academico():  #muestra el menú principal académico
    while True:
        imprimir_titulo("GESTIÓN ACADÉMICA")
        imprimir_menu([
            "Gestionar Carreras",
            "Gestionar Plantillas Académicas",
            "Gestionar Salones",
            "Gestionar Módulos",
            "Gestionar Unidades",
            "Volver"])

        opcion = leer_opcion(6)
        if opcion == 1:
            menu_carreras()
        elif opcion == 2:
            menu_plantillas()
        elif opcion == 3:
            menu_salones()
        elif opcion == 4:
            menu_modulos()
        elif opcion == 5:
            menu_unidades()
        elif opcion == 6:
            print("\nVolviendo al menú director")
            break

def menu_carreras():  #muestra el menú de carreras
    while True:
        imprimir_titulo("GESTIONAR CARRERAS")
        imprimir_menu([
            "Registrar carrera",
            "Editar carrera",
            "Buscar carrera",
            "Ver carreras",
            "Ocultar carrera",
            "Activar carrera",
            "Volver"])

        opcion = leer_opcion(7)

        if opcion == 1:
            registrar_carrera()
        elif opcion == 2:
            editar_carrera()
        elif opcion == 3:
            buscar_carrera()
        elif opcion == 4:
            ver_carreras()
        elif opcion == 5:
            desactivar_carrera()
        elif opcion == 6:
            activar_carrera()
        elif opcion == 7:
            break

def menu_plantillas():  #muestra el menú de plantillas académicas
    while True:
        imprimir_titulo("GESTIONAR PLANTILLAS ACADÉMICAS")
        imprimir_menu([
            "Crear plantilla",
            "Editar plantilla",
            "Asignar carrera a plantilla",
            "Ver plantillas",
            "Desactivar plantilla",
            "Activar plantilla",
            "Volver"])

        opcion = leer_opcion(7)

        if opcion == 1:
            crear_plantilla()
        elif opcion == 2:
            editar_plantilla()
        elif opcion == 3:
            asignar_carrera_plantilla()
        elif opcion == 4:
            ver_plantillas()
        elif opcion == 5:
            desactivar_plantilla()
        elif opcion == 6:
            activar_plantilla()
        elif opcion == 7:
            break

def menu_salones():  #muestra el menú de salones
    while True:
        imprimir_titulo("GESTIONAR SALONES")
        imprimir_menu([
            "Crear salón",
            "Editar salón",
            "Asignar plantilla al salón",
            "Ver salones",
            "Desactivar salón",
            "Activar salón",
            "Volver"])
        opcion = leer_opcion(7)
        if opcion == 1:
            registrar_salon()
        elif opcion == 2:
            editar_salon()
        elif opcion == 3:
            asignar_plantilla_salon()
        elif opcion == 4:
            ver_salones()
        elif opcion == 5:
            desactivar_salon()
        elif opcion == 6:
            activar_salon()
        elif opcion == 7:
            break

def menu_unidades():  #muestra el menú de unidades
    while True:
        imprimir_titulo("GESTIONAR UNIDADES")
        imprimir_menu([
            "Crear unidad",
            "Editar unidad",
            "Ver unidades",
            "Desactivar unidad",
            "Activar unidad",
            "Volver"])

        opcion = leer_opcion(6)

        if opcion == 1:
            registrar_unidad()
        elif opcion == 2:
            editar_unidad()
        elif opcion == 3:
            ver_unidades()
        elif opcion == 4:
            desactivar_unidad()
        elif opcion == 5:
            activar_unidad()
        elif opcion == 6:
            break

def menu_modulos():  #muestra el menú de módulos
    while True:
        imprimir_titulo("GESTIONAR MÓDULOS")
        imprimir_menu([
            "Crear módulo",
            "Editar módulo",
            "Ver módulos",
            "Desactivar módulo",
            "Volver"])

        opcion = leer_opcion(5)

        if opcion == 1:
            registrar_modulo()
        elif opcion == 2:
            editar_modulo()
        elif opcion == 3:
            ver_modulos()
        elif opcion == 4:
            desactivar_modulo()
        elif opcion == 5:
            break