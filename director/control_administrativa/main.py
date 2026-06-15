from director.control_administrativa.cargos_oficiales import crear_cargo_oficial, ver_cargos_oficiales, modificar_cargo_oficial
from director.control_administrativa.descuentos import crear_descuento_convenio
from director.control_administrativa.asignar_descuentos import asignar_descuento_alumno
from director.control_administrativa.cargos_extras import menu_cargos_extras
from director.control_administrativa.resumen_pagos import menu_resumen_pagos
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa
from director.control_administrativa.cargos_oficiales import menu_cargos_oficiales
from director.control_administrativa.descuentos import menu_descuentos
from director.control_administrativa.asignar_descuentos import menu_asignar_descuentos


def menu_control_administrativo():
    while True:
        limpiar_pantalla()
        imprimir_titulo("5. GESTIÓN Y CONTROL ADMINISTRATIVO")
        
        opciones = [
            "Gestionar Cargos Oficiales (Matrículas, Pensiones)",
            "Gestionar Cargos Extras (Certificados)",
            "Gestionar Catálogo de Descuentos / Convenios",
            "Asignar Descuento a un Alumno",
            "Resumen de Pagos y Estado Financiero (Reporte)",
            "Volver al Menú del Director"
        ]
        
        imprimir_menu(opciones)
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            print("\nRedirigiendo a Cargos Oficiales...")
            menu_cargos_oficiales()
            pausa()
        elif opcion == "2":
            print("\nRedirigiendo a Cargos Extras...")
            menu_cargos_extras()
            pausa()
        elif opcion == "3":
            print("\nRedirigiendo a Catálogo de Descuentos...")
            menu_descuentos()
            pausa()
        elif opcion == "4":
            print("\nRedirigiendo a Asignación de Descuentos...")
            menu_asignar_descuentos()
            pausa()
        elif opcion == "5":
            print("\nRedirigiendo a Resumen de Pagos...")
            menu_resumen_pagos()
            pausa()
        elif opcion == "6":
            print("\nVolviendo al menú principal...")
            break
        else:
            print("\n Opción no válida. Por favor, intente de nuevo.")
            pausa()
