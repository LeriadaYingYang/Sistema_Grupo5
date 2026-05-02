from director.carreras.registrar_carrera import registrar_carrera
from director.salones.registrar_salon import registrar_salon
from director.plantillas.crear_plantilla import crear_plantilla
from director.unidades.registrar_unidad import registrar_unidad
from director.cursos.registrar_curso import registrar_curso
from director.notas.crear_tipo_nota import crear_tipo_nota
from director.profesores.main import menu_profesores
from director.alumnos.main import menu_alumnos
from director.alumnos.datos_alumnos.ver_datos_alumnos import menu_ver_datos_alumnos
from director.profesores.datos_profesores.ver_datos_profesores import menu_ver_datos_profesores

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
7. Crear y Asignar profesores a cursos
8. Crear y Asignar alumnos a carreras y salones
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
            registrar_curso()
        elif opcion == "6":
            crear_tipo_nota()
        elif opcion == "7":
            menu_profesores()
        elif opcion == "8":
            menu_alumnos()
        elif opcion == "9":
            menu_ver_datos_alumnos()
        elif opcion == "10":
            menu_ver_datos_profesores()

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