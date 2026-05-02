from director.profesores.crear_profesor import crear_profesor
from director.profesores.asignar_profesor import asignar_profesor


def menu_profesores():
    while True:
        print("""
====================================
        GESTIÓN DE PROFESORES
====================================

1. Crear profesor
2. Asignar profesor a curso
3. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_profesor()

        elif opcion == "2":
            asignar_profesor()

        elif opcion == "3":
            print("\nVolviendo al menú director...")
            break

        else:
            print("Opción inválida.")