from secretaria.matriculas.consultar_matricula import menu_consultar_matricula
from secretaria.matriculas.registrar_matricula import menu_registrar_matricula
from secretaria.matriculas.renovar_matricula import menu_renovar_matricula
from secretaria.matriculas.retirar_matricula import menu_retirar_matricula
from secretaria.utilidades import imprimir_titulo,imprimir_menu

def menu_matriculas(): #Muestra el menú principal de matrículas
    while True:
        imprimir_titulo("=== GESTIÓN DE MATRÍCULAS ===")
        imprimir_menu(["Registrar Matrícula","Consultar Matrícula","Renovar Matrícula",
                    "Retirar Matrícula","Volver"])

        opcion = input("Seleccionar una opción: ")
        if opcion == "1": #Abre el módulo registrar matrícula
            menu_registrar_matricula()
        elif opcion == "2": #Abre el módulo consultar matrícula
            menu_consultar_matricula()
        elif opcion == "3": #Abre el módulo renovar matrícula
            menu_renovar_matricula()
        elif opcion == "4": #Abre el módulo retirar matrícula
            menu_retirar_matricula()
        elif opcion == "5": #Vuelve al menú secretaría
            print("\nVolviendo al menú secretaría...")
            break
        else: #Muestra mensaje de error
            print("Opción inválida.")