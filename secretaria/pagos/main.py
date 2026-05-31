from secretaria.pagos.cargos_oficiales import crear_cargo_oficial, ver_cargos_oficiales, modificar_cargo_oficial
from secretaria.pagos.descuentos import crear_descuento_convenio
from secretaria.pagos.asignar_descuentos import asignar_descuento_alumno
from secretaria.pagos.cargos_extra import menu_cargos_extras
from secretaria.pagos.resumen_pagos import menu_resumen_pagos
from secretaria.utilidades import imprimir_titulo, imprimir_menu

#===========================================
# Archivo: main.py -> pagos
# Participante: Fabrizio Ortega (secretaría)
#===========================================


def menu_pagos():  #Muestra el menú principal de gestión de pagos
    while True:
        imprimir_titulo("=== GESTIÓN DE PAGOS - SECRETARÍA ===")
        imprimir_menu(["Crear Cargo Oficial Por Plantilla Y Carrera", "Ver Cargos Oficiales Creados",
                    "Modificar Cargo Oficial", "Crear Descuento O Convenio", "Asignar Descuento/Convenio A Alumno",
                    "Crear Cargo Extra General", "Ver Resumen De Pagos Y Deudas", "Volver"])
        imprimir_menu([])

        opcion = input("Seleccionar una opción: ")  #Solicita una opción al usuario
        if opcion == "1":  #Crea un cargo oficial
            crear_cargo_oficial()
        elif opcion == "2":  #Muestra los cargos oficiales creados
            ver_cargos_oficiales()
        elif opcion == "3":  #Modifica un cargo oficial
            modificar_cargo_oficial()
        elif opcion == "4":  #Crea un descuento o convenio
            crear_descuento_convenio()
        elif opcion == "5":  #Asigna un descuento o convenio a un alumno
            asignar_descuento_alumno()
        elif opcion == "6":  #Abre el menú de cargos extras
            menu_cargos_extras()
        elif opcion == "7":  #Abre el resumen de pagos y deudas
            menu_resumen_pagos()
        elif opcion == "8":  #Vuelve al menú de secretaría
            print("\nVolviendo al menú de secretaría...")
            break
        else:  #Muestra mensaje si la opción no existe
            print("Opción inválida.")