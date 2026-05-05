from director.alumnos.crear_alumno import crear_alumno
from director.alumnos.asignar_alumno import asignar_alumno
from director.alumnos.ver_datos_alumnos import menu_ver_datos_alumnos
from director.alumnos.editar_alumno import editar_alumno

def menu_alumnos():
    while True:
        print("""
====================================
        GESTIÓN DE ALUMNOS
====================================

1. Crear alumno
2. Asignar alumno a carrera y salón
3. Ver datos de alumnos
4. Editar alumno
5. Volver al menu de director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_alumno()

        elif opcion == "2":
            asignar_alumno()

        elif opcion == "3":
            menu_ver_datos_alumnos()

        elif opcion == "4":
            editar_alumno()

        elif opcion == "5":
            print("\nVolviendo al menú director.")
            break
        else:
            print("Opción inválida.")