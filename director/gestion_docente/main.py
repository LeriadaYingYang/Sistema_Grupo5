from director.gestion_docente.crear_profesor import crear_profesor
from director.gestion_docente.asignar_profesor import asignar_profesor
from director.gestion_docente.ver_datos_profesores import menu_ver_datos_profesores
from director.gestion_docente.editar_profesor import editar_profesor
from director.utilidades import imprimir_titulo, imprimir_menu

# ==========================================
# FUNCIONES REUTILIZABLES DE VALIDACIÓN
# ==========================================

def solicitar_opcion_menu(mensaje, opciones_validas):
    """
    Solicita una opción al usuario limpiando espacios en blanco.
    Repite la solicitud indefinidamente si ingresa un valor inválido.
    """
    while True:
        valor = input(mensaje).strip()  # Elimina espacios innecesarios al inicio y final
        if valor in opciones_validas:
            return valor
        # Muestra un mensaje amigable y claro sin romper el programa
        print(f"❌ Error: Opción inválida. Por favor, seleccione una de las siguientes opciones: {', '.join(opciones_validas)}")


# ==========================================
# VISTA PRINCIPAL (GESTIÓN)
# ==========================================

def menu_profesores():
    """Muestra el menú principal para administrar profesores con validación de entrada."""
    while True:
        imprimir_titulo("GESTIÓN DE PROFESORES")
        imprimir_menu([
            "Crear Profesor", 
            "Asignar Profesor a Salon", 
            "Ver datos de Profesores",
            "Editar Datos de Profesor", 
            "Volver"
        ])

        # Forzamos a que el usuario introduzca una opción estrictamente válida (del 1 al 5)
        opcion = solicitar_opcion_menu("Seleccione una opción (1-5): ", ["1", "2", "3", "4", "5"])

        if opcion == "1":    # Abre el registro para crear un nuevo profesor
            crear_profesor()
        elif opcion == "2":  # Permite asignar un profesor registrado a un salón existente
            asignar_profesor()
        elif opcion == "3":  # Abre el submenú para consultar información de profesores
            menu_ver_datos_profesores()
        elif opcion == "4":  # Permite buscar y modificar los datos personales de un profesor
            editar_profesor()
        elif opcion == "5":  # Regresa al menú principal del director
            print("\nVolviendo al menú director...")
            break