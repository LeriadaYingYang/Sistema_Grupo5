from control_academico.gestion_asistencias.main import menu_asistencias
from control_academico.gestion_notas.main import menu_notas
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

def menu_control_academico():
    while True:
        limpiar_pantalla()
        imprimir_titulo("=== CONTROL ACADÉMICO ===")
        print("1. Gestión de asistencias")
        print("2. Gestión de notas")
        print("3. Volver")
        opcion = input("\nSeleccione una opción: ")
        if opcion == "1":menu_asistencias()
        elif opcion == "2":menu_notas()
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")
            pausa()