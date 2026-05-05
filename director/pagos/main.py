from director.pagos.cargos_oficiales import crear_cargo_oficial, ver_cargos_oficiales, modificar_cargo_oficial
from director.pagos.descuentos import crear_descuento_convenio
from director.pagos.asignar_descuentos import asignar_descuento_alumno
from director.pagos.cargos_extras import menu_cargos_extras
from director.pagos.resumen_pagos import menu_resumen_pagos


def menu_pagos():
    while True:
        print("""
====================================
      GESTIÓN DE PAGOS - DIRECTOR
====================================

1. Crear cargo oficial por plantilla y carrera
2. Ver cargos oficiales creados
3. Modificar cargo oficial
4. Crear descuento o convenio
5. Asignar descuento/convenio a alumno
6. Crear cargo extra general
7. Ver resumen de pagos y deudas
8. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

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