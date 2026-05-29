from director.asistencias.configurar_horarios import configurar_horarios
from director.asistencias.asistencia_alumnos import registrar_asistencia_alumnos
from director.asistencias.asistencia_profesores import registrar_asistencia_profesores
from director.asistencias.ver_asistencia_alumnos import menu_ver_asistencia_alumnos
from director.asistencias.horas_profesores import ver_horas_profesores
from director.utilidades import imprimir_titulo

def menu_asistencias():  #muestra el menú principal de gestión de asistencias
    while True:
        imprimir_titulo("GESTIÓN DE ASISTENCIAS")
        print("""
1. Configurar horarios
2. Registrar asistencia de alumnos
3. Registrar asistencia de profesores
4. Ver asistencia de alumnos
5. Ver horas trabajadas de profesores
6. Volver al menú director
""")
        opcion = input("Seleccione una opción: ")  #solicita una opción al usuario
        if opcion == "1":  #abre la configuración de horarios
            configurar_horarios()
        elif opcion == "2":  #registra asistencia de alumnos
            registrar_asistencia_alumnos()
        elif opcion == "3":  #registra asistencia de profesores
            registrar_asistencia_profesores()
        elif opcion == "4":  #muestra asistencia de alumnos
            menu_ver_asistencia_alumnos()
        elif opcion == "5":  #muestra horas trabajadas de profesores
            ver_horas_profesores()
        elif opcion == "6":  #vuelve al menú del director
            print("\nVolviendo al menú director")
            break
        else:  #muestra mensaje si la opción no existe
            print("Opción inválida.")