from director.alumnos.crear_alumno import crear_alumno
from director.alumnos.asignar_alumno import asignar_alumno
from director.alumnos.ver_datos_alumnos import menu_ver_datos_alumnos
from director.alumnos.editar_alumno import editar_alumno
from director.utilidades import imprimir_titulo

def menu_alumnos():  #muestra el menú principal de gestión de alumnos
    while True:
        imprimir_titulo("GESTIÓN DE ALUMNOS")
        print("""
1. Crear alumno
2. Asignar alumno a carrera y salón
3. Ver datos de alumnos
4. Editar alumno
5. Volver al menú de director
""")
        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #abre el registro de alumno
            crear_alumno()
        elif opcion == "2":  #abre la asignación del alumno a carrera y salón
            asignar_alumno()
        elif opcion == "3":  #abre el menú para ver datos de alumnos
            menu_ver_datos_alumnos()
        elif opcion == "4":  #abre la edición de datos del alumno
            editar_alumno()
        elif opcion == "5":  #vuelve al menú del director
            print("\nVolviendo al menú director.")
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")