from gestion_academica.notas.crear_tablilla import crear_tablilla_notas
from gestion_academica.notas.registrar_modificar_notas import registrar_modificar_notas
from gestion_academica.notas.ver_notas import ver_notas_por_unidad
from gestion_academica.utilidades import imprimir_titulo, imprimir_menu

def menu_notas():  #muestra el menú principal de gestión de notas
    while True:
        imprimir_titulo("GESTIÓN DE NOTAS")
        imprimir_menu(["Crear Tablilla de Notas", "Registrar o Modificar Notas", "Ver Notas","Volver"])

        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #crea la tablilla de notas
            crear_tablilla_notas()
        elif opcion == "2":  #registra o modifica notas
            registrar_modificar_notas()
        elif opcion == "3":  #muestra las notas registradas
            ver_notas_por_unidad()
        elif opcion == "4":  #vuelve al menú del director
            print("\nVolviendo al menú director")
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida. Intente nuevamente.")