from director.asistencias.configurar_horarios import configurar_horarios
from director.asistencias.asistencia_alumnos import registrar_asistencia_alumnos
from director.asistencias.asistencia_profesores import registrar_asistencia_profesores
from director.asistencias.ver_asistencia_alumnos import menu_ver_asistencia_alumnos
from director.asistencias.horas_profesores import ver_horas_profesores


def menu_asistencias():
    while True:
        print("""
====================================
        GESTIÓN DE ASISTENCIAS
====================================

1. Configurar horarios
2. Registrar asistencia de alumnos
3. Registrar asistencia de profesores
4. Ver asistencia de alumnos
5. Ver horas trabajadas de profesores
6. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            configurar_horarios()

        elif opcion == "2":
            registrar_asistencia_alumnos()

        elif opcion == "3":
            registrar_asistencia_profesores()

        elif opcion == "4":
            menu_ver_asistencia_alumnos()

        elif opcion == "5":
            ver_horas_profesores()

        elif opcion == "6":
            print("\nVolviendo al menú director")
            break

        else:
            print("Opción inválida.")