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
        imprimir_menu(["Crear Cargo Oficial Por Plantilla Y Carrera", "Ver Cargos Oficiales Creados",
                      "Modificar Cargo Oficial", "Crear Descuento O Convenio", "Asignar Descuento/Convenio A Alumno",
                      "Crear Cargo Extra General", "Ver Resumen De Pagos Y Deudas", "Volver Al Menú Director"])
        imprimir_menu([])

        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #crea un cargo oficial
            crear_cargo_oficial()
        elif opcion == "2":
            menu_asignar_descuentos()
        elif opcion == "3":  #muestra los cargos oficiales creados
            ver_cargos_oficiales()
        elif opcion == "4":  #modifica un cargo oficial
            modificar_cargo_oficial()
        elif opcion == "5":  #crea un descuento o convenio
            crear_descuento_convenio()
        elif opcion == "6":  #asigna un descuento o convenio a un alumno
            asignar_descuento_alumno()
        elif opcion == "7":  #abre el menú de cargos extras
            menu_cargos_extras()
        elif opcion == "8":  #abre el resumen de pagos y deudas
            menu_resumen_pagos()
        elif opcion == "9":  #vuelve al menú del director
            print("\nVolviendo al menú director")
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")
