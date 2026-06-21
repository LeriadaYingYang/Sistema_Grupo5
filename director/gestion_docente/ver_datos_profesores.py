import re
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_ASIGNACIONES = "datos/profesores_salones.json"

# ==========================================
# FUNCIONES REUTILIZABLES DE VALIDACIÓN
# ==========================================

def solicitar_opcion_menu(mensaje, opciones_validas):
    """Obliga al usuario a elegir una opción válida de un menú."""
    while True:
        valor = input(mensaje).strip()
        if valor in opciones_validas:
            return valor
        print(f" Error: Opción inválida. Elija una de las siguientes: {', '.join(opciones_validas)}")

def solicitar_texto_busqueda(mensaje):
    """
    Solicita un texto para búsqueda (nombres/apellidos).
    Impide valores vacíos y restringe a letras y espacios.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: El campo de búsqueda no puede estar vacío.")
            continue
        # Permite letras, tildes, ñ y espacios
        if re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", dato):
            return dato.lower()
        print(" Error: Solo se permiten letras y espacios para la búsqueda.")

def solicitar_dni_busqueda(mensaje):
    """
    Solicita un DNI para búsqueda.
    Debe tener exactamente 8 dígitos numéricos.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: El DNI no puede estar vacío.")
            continue
        # Expresión regular: exactamente 8 dígitos
        if re.fullmatch(r"\d{8}", dato):
            return dato
        print(" Error: El DNI debe contener exactamente 8 dígitos numéricos.")

# ==========================================
# LÓGICA PRINCIPAL DEL SISTEMA
# ==========================================

def obtener_asignaciones_profesor(id_profesor, asignaciones):
    """Obtiene las asignaciones activas de un profesor."""
    return [
        asignacion
        for asignacion in asignaciones
        if (
            asignacion.get("id_profesor") == id_profesor
            and asignacion.get("estado") == "Activo"
        )
    ]

def mostrar_profesor(profesor, asignaciones_profesor):
    """Muestra los datos del profesor y sus asignaciones."""
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(
        f"Nombre: "
        f"{profesor['nombres']} {profesor['apellidos']}"
    )
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")

    if asignaciones_profesor:
        print("\n--- Cursos asignados ---")
        for asignacion in asignaciones_profesor:
            print(
                f"Carrera: {asignacion['nombre_carrera']} | "
                f"Salón: {asignacion['nombre_salon']} | "
                f"Turno: {asignacion['turno']}"
            )
    else:
        print("\nNo tiene cursos asignados.")

def ver_todos_profesores(profesores, asignaciones):
    """Muestra todos los profesores activos."""
    profesores_activos = [
        profesor
        for profesor in profesores
        if profesor.get("estado") == "Activo"
    ]

    if not profesores_activos:
        print(" No hay profesores registrados o activos.")
        return

    for profesor in profesores_activos:
        asignaciones_profesor = obtener_asignaciones_profesor(
            profesor["id_profesor"],
            asignaciones
        )
        mostrar_profesor(profesor, asignaciones_profesor)

def buscar_por_nombre(profesores, asignaciones):
    """Busca profesores activos por nombre o apellido usando validación."""
    # Uso de la función de validación para garantizar texto limpio
    texto = solicitar_texto_busqueda("Ingrese nombre o apellido: ")

    encontrados = [
        profesor
        for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and texto in (
                f"{profesor['nombres']} {profesor['apellidos']}"
            ).lower()
        )
    ]

    if not encontrados:
        print(" No se encontraron profesores con ese criterio.")
        return

    for profesor in encontrados:
        asignaciones_profesor = obtener_asignaciones_profesor(
            profesor["id_profesor"],
            asignaciones
        )
        mostrar_profesor(profesor, asignaciones_profesor)

def buscar_por_dni(profesores, asignaciones):
    """Busca un profesor activo por DNI usando validación estricta."""
    # Uso de validación estricta de 8 dígitos para evitar búsquedas inútiles
    dni = solicitar_dni_busqueda("Ingrese DNI a buscar: ")

    profesor = next(
        (
            profesor
            for profesor in profesores
            if (
                profesor.get("estado") == "Activo"
                and profesor.get("dni") == dni
            )
        ),
        None
    )

    if profesor is None:
        print(f" No se encontró ningún profesor activo con el DNI {dni}.")
        return

    asignaciones_profesor = obtener_asignaciones_profesor(
        profesor["id_profesor"],
        asignaciones
    )
    mostrar_profesor(profesor, asignaciones_profesor)

def menu_ver_datos_profesores():
    """Menú validado para consultar profesores."""
    while True:
        imprimir_titulo("VER DATOS DE PROFESORES")

        profesores = leer_json(RUTA_PROFESORES)
        asignaciones = leer_json(RUTA_ASIGNACIONES)

        print("""
1. Ver todos los profesores
2. Buscar por nombre
3. Buscar por DNI
4. Volver al menú director
""")
        # Forzar selección válida mediante la función reutilizable
        opcion = solicitar_opcion_menu("Seleccione una opción (1-4): ", ["1", "2", "3", "4"])

        if opcion == "1":
            ver_todos_profesores(profesores, asignaciones)
        elif opcion == "2":
            buscar_por_nombre(profesores, asignaciones)
        elif opcion == "3":
            buscar_por_dni(profesores, asignaciones)
        elif opcion == "4":
            print("\nVolviendo...")
            break