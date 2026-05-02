from director.alumnos.crear_alumno import crear_alumno
from director.alumnos.asignar_alumno import asignar_alumno


def menu_alumnos():
    while True:
        print("""
====================================
        GESTIÓN DE ALUMNOS
====================================

1. Crear alumno
2. Asignar alumno a carrera y salón
3. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_alumno()

        elif opcion == "2":
            asignar_alumno()

        elif opcion == "3":
            print("\nVolviendo al menú director...")
            break

        else:
            print("Opción inválida.")