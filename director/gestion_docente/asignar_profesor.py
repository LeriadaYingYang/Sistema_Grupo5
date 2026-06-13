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
    """Solicita un ID numérico al usuario."""
    try:
        return int(input(mensaje))
    except ValueError:
        print("Debe ingresar un número válido.")
        return None


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

    # Validar profesores activos
    if not any(
        profesor.get("estado") == "Activo"
        for profesor in profesores
    ):
        print("No hay profesores activos registrados.")
        return

    # Validar salones activos
    if not any(
        salon.get("estado") == "Activo"
        for salon in salones
    ):
        print("No hay salones activos registrados.")
        return

    # Seleccionar profesor
    mostrar_profesores(profesores)

    id_profesor = solicitar_id(
        "\nIngrese ID del profesor: "
    )

    if id_profesor is None:
        return

    profesor = buscar_por_id(
        profesores,
        "id_profesor",
        id_profesor
    )

    if profesor is None:
        print(
            f"No existe un profesor activo "
            f"con ID {id_profesor}."
        )
        return

    # Seleccionar salón
    mostrar_salones(salones)

    id_salon = solicitar_id(
        "\nIngrese ID del salón: "
    )

    if id_salon is None:
        return

    salon = buscar_por_id(
        salones,
        "id_salon",
        id_salon
    )

    if salon is None:
        print(
            f"No existe un salón activo "
            f"con ID {id_salon}."
        )
        return

    # Validar duplicados
    if ya_existe_asignacion(
        asignaciones,
        id_profesor,
        id_salon
    ):
        print(
            "Este profesor ya está "
            "asignado a este salón."
        )
        return

    # Crear y guardar asignación
    nueva_asignacion = crear_asignacion(
        asignaciones,
        profesor,
        salon
    )

    asignaciones.append(nueva_asignacion)

    guardar_json(
        RUTA_PROFESORES_SALONES,
        asignaciones
    )

    print("\nProfesor asignado correctamente.")
    print(
        f"Profesor: "
        f"{nueva_asignacion['nombre_profesor']}"
    )
    print(
        f"Carrera: "
        f"{nueva_asignacion['nombre_carrera']}"
    )
    print(
        f"Salón: "
        f"{nueva_asignacion['nombre_salon']}"
    )
    print(
        f"Turno: "
        f"{nueva_asignacion['turno']}"
    )