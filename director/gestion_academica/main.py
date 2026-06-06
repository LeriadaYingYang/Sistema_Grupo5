from director.gestion_academica.carreras import registrar_carrera, ver_carreras
from director.gestion_academica.salones import registrar_salon, ver_salones
from director.gestion_academica.plantilla import crear_plantilla, ver_plantillas
from director.gestion_academica.unidades import registrar_unidad, ver_unidades
from director.gestion_academica.modulos import registrar_modulo, ver_modulos
from director.utilidades import imprimir_titulo, imprimir_menu

def menu_academico():  #muestra el menú principal académico
    while True:
        imprimir_titulo("GESTIÓN ACADÉMICA")
        imprimir_menu(["Carreras", "Salones", "Plantilla Académica", "Unidades / Ciclos",
                       "Modulos","Volver"])

        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #abre el menú de carreras
            menu_carreras()
        elif opcion == "2":  #abre el menú de salones
            menu_salones()
        elif opcion == "3":  #abre el menú de plantillas académicas
            menu_plantillas()
        elif opcion == "4":  #abre el menú de unidades o ciclos
            menu_unidades()
        elif opcion == "5":  #abre el menú de módulos
            menu_modulos()
        elif opcion == "6":  #regresa al menú del director
            print("\nVolviendo al menú director")
            break
        else:  # muestra mensaje si la opción no existe
            print("Opción inválida.")

def menu_carreras():  #muestra el menú de carreras
    while True:
        imprimir_titulo("CARRERAS")
        imprimir_menu(["Registrar carrera", "Ver carrera", "Volver"])
        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #registra una nueva carrera
            registrar_carrera()
        elif opcion == "2":  #muestra las carreras registradas
            ver_carreras()
        elif opcion == "3":  #vuelve al menú académico
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")

def menu_salones():  #muestra el menú de salones
    while True:
        imprimir_titulo("SALONES")
        imprimir_menu(["Crear salon", "Ver salon", "Volver"])
        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #registra un nuevo salón
            registrar_salon()
        elif opcion == "2":  #muestra los salones registrados
            ver_salones()
        elif opcion == "3":  #vuelve al menú académico
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")

def menu_plantillas():  #muestra el menú de plantillas académicas
    while True:
        imprimir_titulo("PLANTILLA ACADÉMICA")
        imprimir_menu(["Crear plantilla", "Ver plantilla", "Volver"])
        opcion = input("Seleccione una opción: ")  # solicita una opción al usuario
        if opcion == "1":  #crea una nueva plantilla académica
            crear_plantilla()
        elif opcion == "2":  # muestra las plantillas registradas
            ver_plantillas()
        elif opcion == "3":  # vuelve al menú académico
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")

def menu_unidades():  #muestra el menú de unidades o ciclos
    while True:
        imprimir_titulo("UNIDADES / CICLOS")
        imprimir_menu(["Registrar unidades o Ciclo", "Ver unidades", "Volver"])

        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #registra una nueva unidad o ciclo
            registrar_unidad()
        elif opcion == "2":  #muestra las unidades registradas
            ver_unidades()
        elif opcion == "3":  #vuelve al menú académico
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")

def menu_modulos():  #muestra el menú de módulos
    while True:
        imprimir_titulo("MÓDULOS")
        imprimir_menu(["Crear modulo", "Ver modulo", "Volver"])
        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #registra un nuevo módulo
            registrar_modulo()
        elif opcion == "2":  #muestra los módulos registrados
            ver_modulos()
        elif opcion == "3":  #vuelve al menú académico
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")