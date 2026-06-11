from control_academico.gestion_asistencias.configurar_horarios import configurar_horarios
from control_academico.gestion_asistencias.rgs_as_alumnos import registrar_asistencia_alumnos
from control_academico.gestion_asistencias.rgs_as_profesores import registrar_asistencia_profesores
from control_academico.gestion_asistencias.ver_as_alumnos import ver_asistencia_alumnos
from control_academico.gestion_asistencias.ver_horas_profesores import ver_horas_profesores
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

def menu_asistencias():
    while True:
        limpiar_pantalla()
        imprimir_titulo("=== GESTIÓN DE ASISTENCIAS ===")
        print("1. Configurar horarios")
        print("2. Registrar asistencia alumnos")
        print("3. Registrar asistencia profesores")
        print("4. Ver asistencia alumnos")
        print("5. Ver horas profesores")
        print("6. Volver")
        opcion = input("\nSeleccione una opción: ")
        limpiar_pantalla()
        if opcion == "1":configurar_horarios()
        elif opcion == "2":registrar_asistencia_alumnos()
        elif opcion == "3":registrar_asistencia_profesores()
        elif opcion == "4":ver_asistencia_alumnos()
        elif opcion == "5":ver_horas_profesores()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
        pausa()