from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"

def buscar_por_id(lista, campo_id, valor_id):
    """Busca un registro activo por su ID."""
    for item in lista:
        if (
            item.get(campo_id) == valor_id and
            item.get("estado") == "Activo"
        ):
            return item
    return None

def solicitar_id(mensaje):
    """
    Solicita un ID numérico al usuario, repitiendo el ciclo hasta que
    ingrese un dato válido. Evita valores vacíos, alfanuméricos y espacios.
    """
    while True:
        valor = input(mensaje).strip() # Limpia espacios al inicio y final
        if not valor:
            print("❌ Error: El campo no puede estar vacío.")
            continue
        try:
            return int(valor) # Intenta convertir a entero
        except ValueError:
            print("❌ Error: Entrada inválida. Debe ingresar exclusivamente un número entero.")

def mostrar_profesores(profesores):
    """Muestra los profesores activos disponibles."""
    imprimir_titulo("PROFESORES DISPONIBLES")

    for profesor in profesores:
        if profesor.get("estado") == "Activo":
            print(
                f"ID: {profesor['id_profesor']} | "
                f"{profesor['nombres']} {profesor['apellidos']}"
            )

def mostrar_salones(salones):
    """Muestra los salones activos disponibles."""
    imprimir_titulo("SALONES DISPONIBLES")

    for salon in salones:
        if salon.get("estado") == "Activo":
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Carrera: {salon['nombre_carrera']} | "
                f"Turno: {salon['turno']}"
            )

def ya_existe_asignacion(asignaciones, id_profesor, id_salon):
    """Verifica si el profesor ya está asignado al salón."""
    return any(
        asignacion.get("id_profesor") == id_profesor and
        asignacion.get("id_salon") == id_salon and
        asignacion.get("estado") == "Activo"
        for asignacion in asignaciones
    )

def crear_asignacion(asignaciones, profesor, salon):
    """Crea el diccionario de una nueva asignación."""
    return {
        "id_profesor_salon": generar_id(
            asignaciones,
            "id_profesor_salon"
        ),
        "id_profesor": profesor["id_profesor"],
        "nombre_profesor": (
            f"{profesor['nombres']} {profesor['apellidos']}"
        ),
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "id_carrera": salon["id_carrera"],
        "nombre_carrera": salon["nombre_carrera"],
        "estado": "Activo"
    }

def asignar_profesor():
    """Asigna un profesor activo a un salón activo."""
    imprimir_titulo("ASIGNAR PROFESOR A SALÓN")

    profesores = leer_json(RUTA_PROFESORES)
    salones = leer_json(RUTA_SALONES)
    asignaciones = leer_json(RUTA_PROFESORES_SALONES)

    # Validar que existan registros activos antes de proceder
    if not any(profesores) or not any(profesor.get("estado") == "Activo" for profesor in profesores):
        print("❌ No hay profesores activos registrados.")
        return

    if not any(salones) or not any(salon.get("estado") == "Activo" for salon in salones):
        print("❌ No hay salones activos registrados.")
        return

    # Proceso de selección de Profesor (Ciclo de validación de existencia)
    while True:
        mostrar_profesores(profesores)
        id_profesor = solicitar_id("\nIngrese ID del profesor: ")
        
        profesor = buscar_por_id(profesores, "id_profesor", id_profesor)
        if profesor is not None:
            break # Si el profesor existe, rompemos el ciclo
        print(f"❌ No existe un profesor activo con ID {id_profesor}. Intente nuevamente.\n")

    # Proceso de selección de Salón (Ciclo de validación de existencia)
    while True:
        mostrar_salones(salones)
        id_salon = solicitar_id("\nIngrese ID del salón: ")
        
        salon = buscar_por_id(salones, "id_salon", id_salon)
        if salon is not None:
            break # Si el salón existe, rompemos el ciclo
        print(f"❌ No existe un salón activo con ID {id_salon}. Intente nuevamente.\n")

    # Validar duplicados
    if ya_existe_asignacion(asignaciones, id_profesor, id_salon):
        print("❌ Error: Este profesor ya está asignado a este salón.")
        return

    # Crear y guardar asignación
    nueva_asignacion = crear_asignacion(asignaciones, profesor, salon)
    asignaciones.append(nueva_asignacion)
    guardar_json(RUTA_PROFESORES_SALONES, asignaciones)

    print("\n✅ Profesor asignado correctamente.")
    print(f"Profesor: {nueva_asignacion['nombre_profesor']}")
    print(f"Carrera: {nueva_asignacion['nombre_carrera']}")
    print(f"Salón: {nueva_asignacion['nombre_salon']}")
    print(f"Turno: {nueva_asignacion['turno']}")