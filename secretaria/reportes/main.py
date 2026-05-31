from secretaria.reportes.reporte_alumnos import menu_reporte_alumnos
from secretaria.reportes.reporte_matriculas import menu_reporte_matriculas
from secretaria.reportes.reporte_pagos import menu_reporte_pagos
from secretaria.reportes.reporte_profesores import menu_reporte_profesores
from secretaria.utilidades import imprimir_titulo,imprimir_menu

#===========================================
# Archivo: main.py -> reportes
# Participante: Fabrizio Ortega (secretaría)
#===========================================

def menu_reportes(): #Muestra el menú principal de reportes
    while True:
        imprimir_titulo("=== GESTIÓN DE REPORTES ===")
        imprimir_menu(["Reporte de Alumnos","Reporte de Matrículas","Reporte de Pagos",
                    "Reporte de Profesores","Volver"])

        opcion = input("Seleccionar una opción: ")
        if opcion == "1": #Abre el módulo reporte de alumnos
            menu_reporte_alumnos()
        elif opcion == "2": #Abre el módulo reporte de matrículas
            menu_reporte_matriculas()
        elif opcion == "3": #Abre el módulo reporte de pagos
            menu_reporte_pagos()
        elif opcion == "4": #Abre el módulo reporte de profesores
            menu_reporte_profesores()
        elif opcion == "5": #Vuelve al menú secretaría
            print("\nVolviendo al menú secretaría...")
            break
        else: #Muestra mensaje de error
            print("Opción inválida.")