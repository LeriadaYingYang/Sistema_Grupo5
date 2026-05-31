from basedatos_json import leer_json

from secretaria.utilidades import (
    imprimir_titulo
)


# =========================================================
# RUTAS
# =========================================================

RUTA_MATRICULAS = "datos/matriculas.json"


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def obtener_matriculas():

    return leer_json(
        RUTA_MATRICULAS
    )


def mostrar_matricula(matricula):

    print(
        f"ID: "
        f"{matricula['id_matricula']} | "

        f"Alumno: "
        f"{matricula['nombre_alumno']} | "

        f"Carrera: "
        f"{matricula['carrera']} | "

        f"Periodo: "
        f"{matricula['periodo']} | "

        f"Estado: "
        f"{matricula['estado']}"
    )


def buscar_matricula_por_id(
    matriculas,
    id_matricula
):

    for matricula in matriculas:

        if (
            matricula["id_matricula"]
            == id_matricula
        ):

            return matricula

    return None


# =========================================================
# REPORTES GENERALES
# =========================================================

def reporte_general_matriculas():

    imprimir_titulo(
        "=== REPORTE GENERAL MATRÍCULAS ==="
    )

    matriculas = obtener_matriculas()

    if len(matriculas) == 0:

        print("No existen matrículas.")
        return

    for matricula in matriculas:

        mostrar_matricula(matricula)

    print(
        f"\nTotal matrículas: "
        f"{len(matriculas)}"
    )


# =========================================================
# REPORTES POR ESTADO
# =========================================================

def reporte_matriculas_activas():

    imprimir_titulo(
        "=== MATRÍCULAS ACTIVAS ==="
    )

    matriculas = obtener_matriculas()

    encontrados = 0

    for matricula in matriculas:

        if matricula["estado"] == "Activa":

            mostrar_matricula(matricula)

            encontrados += 1

    if encontrados == 0:
        print("No existen matrículas activas.")

    print(
        f"\nTotal activas: "
        f"{encontrados}"
    )


def reporte_matriculas_retiradas():

    imprimir_titulo(
        "=== MATRÍCULAS RETIRADAS ==="
    )

    matriculas = obtener_matriculas()

    encontrados = 0

    for matricula in matriculas:

        if matricula["estado"] == "Retirada":

            mostrar_matricula(matricula)

            encontrados += 1

    if encontrados == 0:
        print("No existen matrículas retiradas.")

    print(
        f"\nTotal retiradas: "
        f"{encontrados}"
    )


def reporte_matriculas_finalizadas():

    imprimir_titulo(
        "=== MATRÍCULAS FINALIZADAS ==="
    )

    matriculas = obtener_matriculas()

    encontrados = 0

    for matricula in matriculas:

        if matricula["estado"] == "Finalizada":

            mostrar_matricula(matricula)

            encontrados += 1

    if encontrados == 0:
        print("No existen matrículas finalizadas.")

    print(
        f"\nTotal finalizadas: "
        f"{encontrados}"
    )


# =========================================================
# REPORTES POR CARRERA
# =========================================================

def reporte_por_carrera():

    imprimir_titulo(
        "=== REPORTE POR CARRERA ==="
    )

    matriculas = obtener_matriculas()

    carrera = input(
        "Ingresar carrera: "
    ).lower()

    encontrados = 0

    for matricula in matriculas:

        if (
            matricula["carrera"]
            .lower() == carrera
        ):

            mostrar_matricula(matricula)

            encontrados += 1

    if encontrados == 0:
        print("No existen registros.")

    print(
        f"\nTotal encontrados: "
        f"{encontrados}"
    )


# =========================================================
# REPORTES POR PERIODO
# =========================================================

def reporte_por_periodo():

    imprimir_titulo(
        "=== REPORTE POR PERIODO ==="
    )

    matriculas = obtener_matriculas()

    periodo = input(
        "Ingresar periodo: "
    )

    encontrados = 0

    for matricula in matriculas:

        if (
            matricula["periodo"]
            == periodo
        ):

            mostrar_matricula(matricula)

            encontrados += 1

    if encontrados == 0:
        print("No existen registros.")

    print(
        f"\nTotal encontrados: "
        f"{encontrados}"
    )


# =========================================================
# BÚSQUEDAS
# =========================================================

def buscar_por_id():

    imprimir_titulo(
        "=== BUSCAR MATRÍCULA ==="
    )

    matriculas = obtener_matriculas()

    try:

        id_matricula = int(
            input(
                "Ingresar ID matrícula: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    matricula = buscar_matricula_por_id(
        matriculas,
        id_matricula
    )

    if matricula is None:

        print("Matrícula no encontrada.")
        return

    imprimir_titulo(
        "=== DATOS MATRÍCULA ==="
    )

    for clave, valor in matricula.items():

        print(f"{clave}: {valor}")


# =========================================================
# ESTADÍSTICAS
# =========================================================

def estadisticas_matriculas():

    imprimir_titulo(
        "=== ESTADÍSTICAS MATRÍCULAS ==="
    )

    matriculas = obtener_matriculas()

    total = len(matriculas)

    activas = 0
    retiradas = 0
    finalizadas = 0

    for matricula in matriculas:

        estado = matricula["estado"]

        if estado == "Activa":

            activas += 1

        elif estado == "Retirada":

            retiradas += 1

        elif estado == "Finalizada":

            finalizadas += 1

    print(f"Total matrículas: {total}")
    print(f"Activas: {activas}")
    print(f"Retiradas: {retiradas}")
    print(f"Finalizadas: {finalizadas}")


# =========================================================
# REPORTES ORDENADOS
# =========================================================

def reporte_ordenado_periodo():

    imprimir_titulo(
        "=== REPORTE ORDENADO ==="
    )

    matriculas = obtener_matriculas()

    ordenadas = sorted(

        matriculas,

        key=lambda matricula:
        matricula["periodo"]

    )

    for matricula in ordenadas:

        mostrar_matricula(matricula)


# =========================================================
# MENU INTERNO
# =========================================================

def menu_reporte_matriculas():

    while True:

        imprimir_titulo(
            "=== REPORTES MATRÍCULAS ==="
        )

        print("""
1. Reporte general
2. Matrículas activas
3. Matrículas retiradas
4. Matrículas finalizadas
5. Reporte por carrera
6. Reporte por periodo
7. Buscar matrícula
8. Estadísticas
9. Reporte ordenado
10. Volver
""")

        opcion = input(
            "Seleccione una opción: "
        )

        match opcion:

            # =============================================
            # REPORTES GENERALES
            # =============================================

            case "1":

                reporte_general_matriculas()

            case "2":

                reporte_matriculas_activas()

            case "3":

                reporte_matriculas_retiradas()

            case "4":

                reporte_matriculas_finalizadas()

            # =============================================
            # FILTROS
            # =============================================

            case "5":

                reporte_por_carrera()

            case "6":

                reporte_por_periodo()

            # =============================================
            # BÚSQUEDAS
            # =============================================

            case "7":

                buscar_por_id()

            # =============================================
            # ESTADÍSTICAS
            # =============================================

            case "8":

                estadisticas_matriculas()

            # =============================================
            # ORDENAMIENTO
            # =============================================

            case "9":

                reporte_ordenado_periodo()

            # =============================================
            # SALIR
            # =============================================

            case "10":

                print("Regresando...")
                break

            # =============================================
            # ERROR
            # =============================================

            case _:

                print("Opción inválida.")