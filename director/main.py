from director.carreras.registrar_carrera import registrar_carrera
from director.salones.registrar_salon import registrar_salon
from director.plantillas.crear_plantilla import crear_plantilla
from director.unidades.registrar_unidad import registrar_unidad

def menu_director():
    while True:
        print("""
==================================================
                MENÚ DIRECTOR
==================================================

1. Registrar carreras
2. Registrar salón y asignar carrera
3. Crear plantilla académica por carrera
4. Registrar módulos o unidades por carrera
5. Registrar cursos por módulo o unidad
6. Crear tipos de notas por unidad
7. Asignar profesores a cursos
8. Asignar alumnos a carreras y salones
9. Ver datos de alumnos
10. Ver datos de profesores
11. Ver notas por unidad o módulo
12. Ver notas finales de alumnos
13. Ver asistencias de alumnos
14. Ver asistencias de profesores
15. Ver reportes académicos
16. Autorizar modificación de notas
17. Definir pagos mensuales por carrera
18. Ver alumnos con deudas
19. Cerrar sesión
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_carrera()
        elif opcion == "2":
            registrar_salon()
        elif opcion == "3":
            crear_plantilla()
        elif opcion == "4":
            registrar_unidad()

        elif opcion == "5":
            print("\nRegistrar cursos por módulo o unidad")

        elif opcion == "6":
            print("\nCrear tipos de notas por unidad")

        elif opcion == "7":
            print("\nAsignar profesores a cursos")

        elif opcion == "8":
            print("\nAsignar alumnos a carreras y salones")

        elif opcion == "9":
            print("\nVer datos de alumnos")

        elif opcion == "10":
            print("\nVer datos de profesores")

        elif opcion == "11":
            print("\nVer notas por unidad o módulo")

        elif opcion == "12":
            print("\nVer notas finales de alumnos")

        elif opcion == "13":
            print("\nVer asistencias de alumnos")

        elif opcion == "14":
            print("\nVer asistencias de profesores")

        elif opcion == "15":
            print("\nVer reportes académicos")

        elif opcion == "16":
            print("\nAutorizar modificación de notas")

        elif opcion == "17":
            print("\nDefinir pagos mensuales por carrera")

        elif opcion == "18":
            print("\nVer alumnos con deudas")

        elif opcion == "19":
            print("\nCerrando sesión del director...")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")