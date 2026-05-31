from basedatos_json import leer_json
from secretaria.utilidades import (imprimir_titulo)

RUTA_ALUMNOS = "datos/alumnos.json"

def obtener_alumnos():
    return leer_json(RUTA_ALUMNOS)

def mostrar_alumno(alumno):
    print(f"ID: {alumno['id_alumno']} | "
        f"{alumno['nombres']} "
        f"{alumno['apellidos']} | "
        f"DNI: {alumno['dni']} | "
        f"Estado: {alumno['estado']}")

def buscar_alumno_por_id(alumnos,id_alumno):
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno):
            return alumno
    return None

def reporte_general_alumnos():
    imprimir_titulo("=== REPORTE GENERAL ALUMNOS ===")
    alumnos = obtener_alumnos()
    if len(alumnos) == 0:
        print("No existen alumnos.")
        return
    for alumno in alumnos:
        mostrar_alumno(alumno)
    print(f"\nTotal alumnos: "
        f"{len(alumnos)}")

def reporte_alumnos_activos():

    imprimir_titulo(
        "=== ALUMNOS ACTIVOS ==="
    )

    alumnos = obtener_alumnos()

    encontrados = 0

    for alumno in alumnos:

        if alumno["estado"] == "Activo":

            mostrar_alumno(alumno)

            encontrados += 1

    if encontrados == 0:
        print("No existen alumnos activos.")

    print(
        f"\nTotal activos: "
        f"{encontrados}"
    )


def reporte_alumnos_inactivos():

    imprimir_titulo(
        "=== ALUMNOS INACTIVOS ==="
    )

    alumnos = obtener_alumnos()

    encontrados = 0

    for alumno in alumnos:

        if alumno["estado"] == "Inactivo":

            mostrar_alumno(alumno)

            encontrados += 1

    if encontrados == 0:
        print("No existen alumnos inactivos.")

    print(
        f"\nTotal inactivos: "
        f"{encontrados}"
    )


# =========================================================
# BÚSQUEDAS
# =========================================================

def buscar_por_dni():

    imprimir_titulo(
        "=== BUSCAR POR DNI ==="
    )

    alumnos = obtener_alumnos()

    dni = input(
        "Ingresar DNI: "
    )

    encontrados = 0

    for alumno in alumnos:

        if alumno["dni"] == dni:

            mostrar_alumno(alumno)

            encontrados += 1

    if encontrados == 0:
        print("No se encontraron resultados.")


def buscar_por_nombre():

    imprimir_titulo(
        "=== BUSCAR POR NOMBRE ==="
    )

    alumnos = obtener_alumnos()

    texto = input(
        "Ingresar nombre/apellido: "
    ).lower()

    encontrados = 0

    for alumno in alumnos:

        nombre_completo = (

            f"{alumno['nombres']} "
            f"{alumno['apellidos']}"

        ).lower()

        if texto in nombre_completo:

            mostrar_alumno(alumno)

            encontrados += 1

    if encontrados == 0:
        print("No se encontraron resultados.")


def buscar_por_id():

    imprimir_titulo(
        "=== BUSCAR POR ID ==="
    )

    alumnos = obtener_alumnos()

    try:

        id_alumno = int(
            input(
                "Ingresar ID alumno: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    alumno = buscar_alumno_por_id(
        alumnos,
        id_alumno
    )

    if alumno is None:

        print("Alumno no encontrado.")
        return

    imprimir_titulo(
        "=== DATOS DEL ALUMNO ==="
    )

    for clave, valor in alumno.items():

        print(f"{clave}: {valor}")


# =========================================================
# ESTADÍSTICAS
# =========================================================

def estadisticas_alumnos():

    imprimir_titulo(
        "=== ESTADÍSTICAS ALUMNOS ==="
    )

    alumnos = obtener_alumnos()

    total = len(alumnos)

    activos = 0
    inactivos = 0

    for alumno in alumnos:

        if alumno["estado"] == "Activo":
            activos += 1

        elif alumno["estado"] == "Inactivo":
            inactivos += 1

    print(f"Total alumnos: {total}")
    print(f"Activos: {activos}")
    print(f"Inactivos: {inactivos}")


# =========================================================
# REPORTES AVANZADOS
# =========================================================

def reporte_ordenado_apellidos():

    imprimir_titulo(
        "=== REPORTE ORDENADO ==="
    )

    alumnos = obtener_alumnos()

    alumnos_ordenados = sorted(

        alumnos,

        key=lambda alumno:
        alumno["apellidos"]

    )

    for alumno in alumnos_ordenados:

        mostrar_alumno(alumno)


# =========================================================
# MENU INTERNO
# =========================================================

def menu_reporte_alumnos():

    while True:

        imprimir_titulo(
            "=== REPORTES ALUMNOS ==="
        )

        print("""
1. Reporte general
2. Alumnos activos
3. Alumnos inactivos
4. Buscar por ID
5. Buscar por DNI
6. Buscar por nombre
7. Estadísticas
8. Reporte ordenado
9. Volver
""")

        opcion = input(
            "Seleccione una opción: "
        )

        match opcion:

            # =============================================
            # REPORTES
            # =============================================

            case "1":

                reporte_general_alumnos()

            case "2":

                reporte_alumnos_activos()

            case "3":

                reporte_alumnos_inactivos()

            # =============================================
            # BÚSQUEDAS
            # =============================================

            case "4":

                buscar_por_id()

            case "5":

                buscar_por_dni()

            case "6":

                buscar_por_nombre()

            # =============================================
            # ESTADÍSTICAS
            # =============================================

            case "7":

                estadisticas_alumnos()

            # =============================================
            # ORDENAMIENTO
            # =============================================

            case "8":

                reporte_ordenado_apellidos()

            # =============================================
            # SALIR
            # =============================================

            case "9":

                print("Regresando...")
                break

            # =============================================
            # ERROR
            # =============================================

            case _:

                print("Opción inválida.")