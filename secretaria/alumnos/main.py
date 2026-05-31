from secretaria.alumnos.crear_alumno import crear_alumno
from secretaria.alumnos.asignar_alumnos import asignar_alumno
from secretaria.alumnos.ver_datos_alumnos import menu_ver_datos_alumnos
from secretaria.alumnos.editar_alumno import editar_alumno
from secretaria.utilidades import imprimir_titulo, imprimir_menu

#===========================================
# Archivo: main.py -> alumnos
# Participante: Fabrizio Ortega (secretaría)
#===========================================

def menu_alumnos():  #muestra el menú principal de gestión de alumnos
    while True:
        imprimir_titulo("=== GESTIÓN DE ALUMNOS ===")
        imprimir_menu(["Crear Alumno", "Asignar Alumno a Carrera y Salón",
                    "Ver Datos de Alumno","Editar Alumno","Volver"])

        opcion = input("Seleccionar una opción: ")  #Solicita una opción al usuario
        if opcion == "1":  #Abre el registro de alumno
            crear_alumno()
        elif opcion == "2":  #Abre la asignación del alumno a carrera y salón
            asignar_alumno()
        elif opcion == "3":  #Abre el menú para ver datos de alumnos
            menu_ver_datos_alumnos()
        elif opcion == "4":  #Abre la edición de datos del alumno
            editar_alumno()
        elif opcion == "5":  #Vuelve al menú de secretaría
            print("\nVolviendo al menú de secretaría...")
            break
        else:  #Muestra mensaje si la opción no existe
            print("Opción inválida.")