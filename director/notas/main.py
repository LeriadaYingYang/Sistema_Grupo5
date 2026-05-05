from director.notas.crear_tablilla import crear_tablilla_notas
from director.notas.registrar_modificar_notas import registrar_modificar_notas
from director.notas.ver_notas import ver_notas_por_unidad


def menu_notas():
    while True:
        print("""
====================================
          GESTIÓN DE NOTAS
====================================

1. Crear tablilla de notas
2. Registrar o modificar notas
3. Ver notas
4. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_tablilla_notas()

        elif opcion == "2":
            registrar_modificar_notas()

        elif opcion == "3":
            ver_notas_por_unidad()

        elif opcion == "4":
            print("\nVolviendo al menú director")
            break

        else:
            print("Opción inválida. Intente nuevamente.")