# Importa funciones para cada operación de notas y herramientas de interfaz comunes
from control_academico.gestion_notas.registrar_nota import registrar_notas
from control_academico.gestion_notas.consultar_notas import consultar_notas
from control_academico.gestion_notas.modificar_nota import menu_modificar_notas
from control_academico.gestion_notas.eliminar_nota import menu_eliminar_notas
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

# Función principal: menú del módulo de gestión de notas
def menu_notas():
    # Bucle que mantiene el menú activo hasta elegir volver
    while True:
        limpiar_pantalla() # Limpia la pantalla para mostrar el menú limpio
        imprimir_titulo("=== GESTIÓN DE NOTAS ===") # Muestra el título del módulo
        # Opciones de acciones disponibles
        print("1. Registrar nota")
        print("2. Consultar notas")
        print("3. Modificar nota")
        print("4. Eliminar nota")
        print("5. Volver")
        opcion = input("\nSeleccione una opción: ") # Captura la elección del usuario
        limpiar_pantalla() # Limpia antes de ejecutar la acción elegida

        # Ejecuta la función correspondiente o sale del menú
        if opcion == "1":registrar_notas()
        elif opcion == "2":consultar_notas()
        elif opcion == "3":menu_modificar_notas()
        elif opcion == "4":menu_eliminar_notas()
        elif opcion == "5":
            break # Termina el bucle y regresa al menú anterior
        else:
            print("Opción inválida.") # Mensaje para entradas no válidas
        pausa() # Detiene la ejecución para que se lea el mensaje o resultado