from director.notas.crear_tablilla import crear_tablilla_notas
from director.notas.registrar_modificar_notas import registrar_modificar_notas
from director.notas.ver_notas import ver_notas_por_unidad
from director.utilidades import imprimir_titulo

def menu_notas():  #muestra el menú principal de gestión de notas
    while True:
        imprimir_titulo("GESTIÓN DE NOTAS")

        print("""
1. Crear tablilla de notas
2. Registrar o modificar notas
3. Ver notas
4. Volver al menú director
""")

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