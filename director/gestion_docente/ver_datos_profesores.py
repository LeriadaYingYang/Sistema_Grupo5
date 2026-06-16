from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_ASIGNACIONES = "datos/profesores_salones.json"


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
        print("No hay profesores registrados.")
        return

    for profesor in profesores_activos:
        asignaciones_profesor = (
            obtener_asignaciones_profesor(
                profesor["id_profesor"],
                asignaciones
            )
        )

        mostrar_profesor(
            profesor,
            asignaciones_profesor
        )


def buscar_por_nombre(profesores, asignaciones):
    """Busca profesores por nombre o apellido."""
    texto = input(
        "Ingrese nombre o apellido: "
    ).strip().lower()

    encontrados = [
        profesor
        for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and texto in (
                f"{profesor['nombres']} "
                f"{profesor['apellidos']}"
            ).lower()
        )
    ]

    if not encontrados:
        print("No se encontraron profesores.")
        return

    for profesor in encontrados:
        asignaciones_profesor = (
            obtener_asignaciones_profesor(
                profesor["id_profesor"],
                asignaciones
            )
        )

        mostrar_profesor(
            profesor,
            asignaciones_profesor
        )


def buscar_por_dni(profesores, asignaciones):
    """Busca un profesor por DNI."""
    dni = input(
        "Ingrese DNI: "
    ).strip()

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
        print(
            "No se encontró profesor "
            "con ese DNI."
        )
        return

    asignaciones_profesor = (
        obtener_asignaciones_profesor(
            profesor["id_profesor"],
            asignaciones
        )
    )

    mostrar_profesor(
        profesor,
        asignaciones_profesor
    )


def menu_ver_datos_profesores():
    """Menú para consultar profesores."""
    while True:
        imprimir_titulo(
            "VER DATOS DE PROFESORES"
        )

        profesores = leer_json(
            RUTA_PROFESORES
        )

        asignaciones = leer_json(
            RUTA_ASIGNACIONES
        )

        print("""
1. Ver todos los profesores
2. Buscar por nombre
3. Buscar por DNI
4. Volver al menú director
""")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":
            ver_todos_profesores(
                profesores,
                asignaciones
            )

        elif opcion == "2":
            buscar_por_nombre(
                profesores,
                asignaciones
            )

        elif opcion == "3":
            buscar_por_dni(
                profesores,
                asignaciones
            )

        elif opcion == "4":
            print("\nVolviendo...")
            break

        else:
            print("Opción inválida.")