from secretaria.profesores.crear_profesor import crear_profesor
from secretaria.profesores.asignar_profesor import asignar_profesor
from secretaria.profesores.ver_datos_profesores import menu_ver_datos_profesores
from secretaria.profesores.editar_profesor import editar_profesor
from secretaria.utilidades import imprimir_titulo, imprimir_menu

#===========================================
# Archivo: main.py -> profesores
# Participante: Fabrizio Ortega (secretaría)
#===========================================

def menu_profesores():  #Muestra el menú principal para administrar profesores
    while True:
        imprimir_titulo("=== GESTIÓN DE PROFESORES ===")
        imprimir_menu(["Crear Profesor", "Asignar Profesor a Salon", "Ver datos de Profesores",
                    "Editar Datos de Profesor", "Volver"])

        opcion = input("Seleccionar una opción: ")  #Solicita la opción que desea ejecutar el usuario
        if opcion == "1":  #Abre crear_profesor.py
            crear_profesor()
        elif opcion == "2":  #Abre asignar_profesor.py
            asignar_profesor()
        elif opcion == "3":  #Abre ver_datos_profesores.py
            menu_ver_datos_profesores()
        elif opcion == "4":  #Abre editar_profesor.py
            editar_profesor()
        elif opcion == "5": #Regresa al menú principal de secretaría
            print("\nVolviendo al menú de secretaría...")
            break
        else:  #Muestra mensaje cuando la opción ingresada no existe
            print("Opción inválida.")