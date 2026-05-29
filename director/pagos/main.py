from director.pagos.cargos_oficiales import crear_cargo_oficial, ver_cargos_oficiales, modificar_cargo_oficial
from director.pagos.descuentos import crear_descuento_convenio
from director.pagos.asignar_descuentos import asignar_descuento_alumno
from director.pagos.cargos_extras import menu_cargos_extras
from director.pagos.resumen_pagos import menu_resumen_pagos
from director.utilidades import imprimir_titulo


def menu_pagos():  #muestra el menú principal de gestión de pagos
    while True:
        imprimir_titulo("GESTIÓN DE PAGOS - DIRECTOR")

        print("""
1. Crear cargo oficial por plantilla y carrera
2. Ver cargos oficiales creados
3. Modificar cargo oficial
4. Crear descuento o convenio
5. Asignar descuento/convenio a alumno
6. Crear cargo extra general
7. Ver resumen de pagos y deudas
8. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #crea un cargo oficial
            crear_cargo_oficial()
        elif opcion == "2":  #muestra los cargos oficiales creados
            ver_cargos_oficiales()
        elif opcion == "3":  #modifica un cargo oficial
            modificar_cargo_oficial()
        elif opcion == "4":  #crea un descuento o convenio
            crear_descuento_convenio()
        elif opcion == "5":  #asigna un descuento o convenio a un alumno
            asignar_descuento_alumno()
        elif opcion == "6":  #abre el menú de cargos extras
            menu_cargos_extras()
        elif opcion == "7":  #abre el resumen de pagos y deudas
            menu_resumen_pagos()
        elif opcion == "8":  #vuelve al menú del director
            print("\nVolviendo al menú director")
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")