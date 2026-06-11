# Importa funciones específicas para cada operación de asistencia y herramientas de interfaz
from control_academico.gestion_asistencias.configurar_horarios import configurar_horarios
from control_academico.gestion_asistencias.rgs_as_alumnos import registrar_asistencia_alumnos
from control_academico.gestion_asistencias.rgs_as_profesores import registrar_asistencia_profesores
from control_academico.gestion_asistencias.ver_as_alumnos import ver_asistencia_alumnos
from control_academico.gestion_asistencias.ver_horas_profesores import ver_horas_profesores
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

# Función que muestra y gestiona el menú de asistencia
def menu_asistencias():
    # Bucle que mantiene el menú activo hasta elegir "Volver"
    while True:
        limpiar_pantalla() # Limpia la consola antes de mostrar el menú
        imprimir_titulo("=== GESTIÓN DE ASISTENCIAS ===") # Muestra el título del módulo
        # Lista de opciones disponibles
        print("1. Configurar horarios")
        print("2. Registrar asistencia alumnos")
        print("3. Registrar asistencia profesores")
        print("4. Ver asistencia alumnos")
        print("5. Ver horas profesores")
        print("6. Volver")
        opcion = input("\nSeleccione una opción: ") # Captura la selección del usuario
        limpiar_pantalla() # Limpia antes de ejecutar la acción elegida

        # Ejecuta la función correspondiente o sale del menú
        if opcion == "1":configurar_horarios()
        elif opcion == "2":registrar_asistencia_alumnos()
        elif opcion == "3":registrar_asistencia_profesores()
        elif opcion == "4":ver_asistencia_alumnos()
        elif opcion == "5":ver_horas_profesores()
        elif opcion == "6":
            break # Finaliza el bucle y regresa al menú anterior
        else:
            print("Opción inválida.") # Mensaje de error para entradas incorrectas
        pausa() # Pausa para que el usuario lea el resultado o mensaje