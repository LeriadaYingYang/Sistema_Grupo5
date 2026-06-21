from director.control_administrativa.asignar_descuentos import menu_asignar_descuentos
from director.control_administrativa.cargos_oficiales import crear_cargo_oficial, ver_cargos_oficiales, modificar_cargo_oficial
from director.control_administrativa.descuentos import crear_descuento_convenio
from director.control_administrativa.asignar_descuentos import asignar_descuento_alumno
from director.control_administrativa.cargos_extras import menu_cargos_extras
from director.control_administrativa.resumen_pagos import menu_resumen_pagos
from director.utilidades import imprimir_titulo, imprimir_menu


def menu_pagos():  #muestra el menú principal de gestión de pagos
    while True:
        imprimir_titulo("GESTIÓN DE PAGOS - DIRECTOR")
        imprimir_menu([
            "Crear cargo oficial",
            "Ver cargos oficiales",
            "Modificar cargo oficial",
            "Crear descuento o convenio",
            "Asignar descuento/convenio a alumno",
            "Gestionar cargos extras",
            "Ver resumen de pagos y deudas",
            "Volver al menú director"])

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_cargo_oficial()
        elif opcion == "2":
            ver_cargos_oficiales()
        elif opcion == "3":
            modificar_cargo_oficial()
        elif opcion == "4":
            crear_descuento_convenio()
        elif opcion == "5":
            asignar_descuento_alumno()
        elif opcion == "6":
            menu_cargos_extras()
        elif opcion == "7":
            menu_resumen_pagos()
        elif opcion == "8":
            print("\nVolviendo al menú director")
            break
        else:
            print("Opción inválida.")
