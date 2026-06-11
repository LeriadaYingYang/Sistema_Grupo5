from director.profesores.crear_profesor import crear_profesor
from director.profesores.asignar_profesor import asignar_profesor
from director.profesores.ver_datos_profesores import menu_ver_datos_profesores
from director.profesores.editar_profesor import editar_profesor
from director.utilidades import imprimir_titulo, imprimir_menu

def menu_profesores():  #muestra el menú principal para administrar profesores
    while True:
        imprimir_titulo("GESTIÓN DE PROFESORES")
        imprimir_menu(["Crear Profesor", "Asignar Profesor a Salon", "Ver datos de Profesores",
                       "Editar Datos de Profesor", "Volver"])

        opcion = input("Seleccione una opción: ")  #solicita la opción que desea ejecutar el usuario
        if opcion == "1":  #abre el registro para crear un nuevo profesor
            crear_profesor()
        elif opcion == "2":  #permite asignar un profesor registrado a un salón existente
            asignar_profesor()
        elif opcion == "3":  #abre el submenú para consultar información de profesores
            menu_ver_datos_profesores()
        elif opcion == "4":  #permite buscar y modificar los datos personales de un profesor
            editar_profesor()
        elif opcion == "5": #regresa al menú principal del director
            print("\nVolviendo al menú director")
            break
        else:  #muestra mensaje cuando la opción ingresada no existe
            print("Opción inválida.")