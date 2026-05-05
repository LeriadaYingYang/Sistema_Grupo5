from director.profesores.crear_profesor import crear_profesor
from director.profesores.asignar_profesor import asignar_profesor
from director.profesores.ver_datos_profesores import menu_ver_datos_profesores
from director.profesores.editar_profesor import editar_profesor

def menu_profesores():
    while True:
        print("""
====================================
        GESTIÓN DE PROFESORES
====================================

1. Crear profesor
2. Asignar profesor a salon
3. Ver datos de profesores
4. Editar datos de profesores
5. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_profesor()

        elif opcion == "2":
            asignar_profesor()

        elif opcion == "3":
            menu_ver_datos_profesores()

        elif opcion == "4":
            editar_profesor()

        elif opcion == "5":
            print("\nVolviendo al menú director")
            break

        else:
            print("Opción inválida.")