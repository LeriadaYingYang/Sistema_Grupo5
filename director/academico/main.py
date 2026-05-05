from director.academico.carreras import registrar_carrera, ver_carreras
from director.academico.salones import registrar_salon, ver_salones
from director.academico.plantilla import crear_plantilla, ver_plantillas
from director.academico.unidades import registrar_unidad, ver_unidades
from director.academico.modulos import registrar_modulo, ver_modulos

def menu_academico():
    while True:
        print("""
====================================
        GESTIÓN ACADÉMICA
====================================

1. Carreras
2. Salones
3. Plantilla académica
4. Unidades / ciclos
5. Módulos
6. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_carreras()

        elif opcion == "2":
            menu_salones()

        elif opcion == "3":
            menu_plantillas()

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
        print("""
====================================
            CARRERAS
====================================

1. Registrar carrera
2. Ver carreras
3. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_carrera()

        elif opcion == "2":
            ver_carreras()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

def menu_salones():
    while True:
        print("""
====================================
            SALONES
====================================

1. Registrar salón
2. Ver salones
3. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_salon()

        elif opcion == "2":
            ver_salones()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

def menu_plantillas():
    while True:
        print("""
====================================
        PLANTILLA ACADÉMICA
====================================

1. Crear plantilla
2. Ver plantillas
3. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_plantilla()

        elif opcion == "2":
            ver_plantillas()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

def menu_unidades():
    while True:
        print("""
====================================
        UNIDADES / CICLOS
====================================

1. Registrar unidad o ciclo
2. Ver unidades
3. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_unidad()

        elif opcion == "2":
            ver_unidades()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

def menu_modulos():
    while True:
        print("""
====================================
            MÓDULOS
====================================

1. Registrar módulo
2. Ver módulos
3. Volver
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_modulo()

        elif opcion == "2":
            ver_modulos()

        elif opcion == "3":
            break

        else:
            print("Opción inválida.")

