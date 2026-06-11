# Importa funciones de otros módulos: menús de asistencias y notas, y herramientas de interfaz
from control_academico.gestion_asistencias.main import menu_asistencias
from control_academico.gestion_notas.main import menu_notas
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

# Función principal: menú principal del sistema de control académico
def menu_control_academico(): 
    # Bucle infinito: mantiene el menú activo hasta elegir "Volver"
    while True:
        limpiar_pantalla()  # Limpia la consola para una vista limpia
        imprimir_titulo("=== CONTROL ACADÉMICO ===")  # Muestra el título del módulo
        # Opciones disponibles para el usuario
        print("1. Gestión de asistencias")
        print("2. Gestión de notas")
        print("3. Volver")
        opcion = input("\nSeleccione una opción: ")  # Captura la elección del usuario

        # Navegación: llama al módulo correspondiente o sale del menú
        if opcion == "1":menu_asistencias()  # Accede al sistema de asistencias
        elif opcion == "2":menu_notas()  # Accede al sistema de notas
        elif opcion == "3":
            break  # Termina el bucle y regresa al menú anterior
        else:
            # Manejo de entradas incorrectas
            print("Opción inválida.")
            pausa()  # Detiene la ejecución para que el usuario lea el mensaje