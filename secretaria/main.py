from secretaria.alumnos.main import menu_alumnos
from secretaria.profesores.main import menu_profesores
from secretaria.pagos.main import menu_pagos
from secretaria.reportes.main import menu_reportes
from secretaria.matriculas.main import menu_matriculas
from secretaria.documentos.main import menu_documentos
from director.utilidades import imprimir_titulo, imprimir_menu

def menu_secretaria():  #Muestra el menú principal de secretaría
    while True:
        imprimir_titulo("=== MENÚ SECRETARÍA ===")
        imprimir_menu(["Gestión de Alumnos", "Gestión de Profesores", "Gestión de Documentos",
                    "Gestión de Matrículas","Gestión de Pagos", "Gestión de Reportes", "Cerrar sesión"])

        opcion = input("Seleccionar una opción: ")  #Solicita la opción que desea ejecutar el director
        if opcion == "1":  #Abre el módulo para registrar, asignar y administrar alumnos
            menu_alumnos()
        elif opcion == "2":  #Abre el módulo para registrar, asignar y administrar docentes
            menu_profesores()
        elif opcion == "3":  #Abre el módulo para gestionar documentos académicos
            menu_documentos()
        elif opcion == "4":  #Abre el módulo para gestionar matrículas
            menu_matriculas()
        elif opcion == "5":  #Abre el módulo para gestionar pagos
            menu_pagos()
        elif opcion == "6":  #Abre el módulo para generar reportes académicos y administrativos
            menu_reportes()
        elif opcion == "7":  #Finaliza la sesión del director y regresa al menú principal del sistema
            print("\nCerrando sesión de secretaría...")
            break
        else:  #Muestra mensaje cuando la opción ingresada no existe en el menú
            print("\nOpción inválida. Intente nuevamente.")