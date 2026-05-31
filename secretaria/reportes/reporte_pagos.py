from basedatos_json import leer_json

from secretaria.utilidades import (
    imprimir_titulo
)


# =========================================================
# RUTAS
# =========================================================

RUTA_PAGOS = "datos/pagos.json"


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def obtener_pagos():

    return leer_json(
        RUTA_PAGOS
    )


def mostrar_pago(pago):

    print(
        f"ID Pago: "
        f"{pago['id_pago']} | "

        f"Alumno: "
        f"{pago['nombre_alumno']} | "

        f"Monto: "
        f"S/. {pago['monto']} | "

        f"Método: "
        f"{pago['metodo_pago']} | "

        f"Estado: "
        f"{pago['estado']}"
    )


def buscar_pago_por_id(
    pagos,
    id_pago
):

    for pago in pagos:

        if (
            pago["id_pago"]
            == id_pago
        ):

            return pago

    return None


# =========================================================
# REPORTES GENERALES
# =========================================================

def reporte_general_pagos():

    imprimir_titulo(
        "=== REPORTE GENERAL PAGOS ==="
    )

    pagos = obtener_pagos()

    if len(pagos) == 0:

        print("No existen pagos.")
        return

    for pago in pagos:

        mostrar_pago(pago)

    print(
        f"\nTotal pagos: "
        f"{len(pagos)}"
    )


# =========================================================
# REPORTES POR ESTADO
# =========================================================

def reporte_pagos_pagados():

    imprimir_titulo(
        "=== PAGOS REALIZADOS ==="
    )

    pagos = obtener_pagos()

    encontrados = 0

    for pago in pagos:

        if pago["estado"] == "Pagado":

            mostrar_pago(pago)

            encontrados += 1

    if encontrados == 0:
        print("No existen pagos realizados.")

    print(
        f"\nTotal pagados: "
        f"{encontrados}"
    )


def reporte_pagos_pendientes():

    imprimir_titulo(
        "=== PAGOS PENDIENTES ==="
    )

    pagos = obtener_pagos()

    encontrados = 0

    for pago in pagos:

        if pago["estado"] == "Pendiente":

            mostrar_pago(pago)

            encontrados += 1

    if encontrados == 0:
        print("No existen pagos pendientes.")

    print(
        f"\nTotal pendientes: "
        f"{encontrados}"
    )


# =========================================================
# REPORTES POR MÉTODO
# =========================================================

def reporte_por_metodo_pago():

    imprimir_titulo(
        "=== REPORTE MÉTODO PAGO ==="
    )

    pagos = obtener_pagos()

    metodo = input(
        "Ingresar método: "
    ).lower()

    encontrados = 0

    for pago in pagos:

        if (
            pago["metodo_pago"]
            .lower() == metodo
        ):

            mostrar_pago(pago)

            encontrados += 1

    if encontrados == 0:
        print("No existen registros.")

    print(
        f"\nTotal encontrados: "
        f"{encontrados}"
    )


# =========================================================
# REPORTES POR MONTO
# =========================================================

def reporte_mayores_montos():

    imprimir_titulo(
        "=== MAYORES PAGOS ==="
    )

    pagos = obtener_pagos()

    ordenados = sorted(

        pagos,

        key=lambda pago:
        pago["monto"],

        reverse=True
    )

    for pago in ordenados:

        mostrar_pago(pago)


# =========================================================
# BÚSQUEDAS
# =========================================================

def buscar_pago():

    imprimir_titulo(
        "=== BUSCAR PAGO ==="
    )

    pagos = obtener_pagos()

    try:

        id_pago = int(
            input(
                "Ingresar ID pago: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    pago = buscar_pago_por_id(
        pagos,
        id_pago
    )

    if pago is None:

        print("Pago no encontrado.")
        return

    imprimir_titulo(
        "=== DATOS PAGO ==="
    )

    for clave, valor in pago.items():

        print(f"{clave}: {valor}")


# =========================================================
# ESTADÍSTICAS
# =========================================================

def estadisticas_pagos():

    imprimir_titulo(
        "=== ESTADÍSTICAS PAGOS ==="
    )

    pagos = obtener_pagos()

    total_pagos = len(pagos)

    total_pagados = 0
    total_pendientes = 0

    monto_pagado = 0
    monto_pendiente = 0

    for pago in pagos:

        if pago["estado"] == "Pagado":

            total_pagados += 1

            monto_pagado += pago["monto"]

        elif pago["estado"] == "Pendiente":

            total_pendientes += 1

            monto_pendiente += pago["monto"]

    print(f"Total registros: {total_pagos}")

    print(f"Pagados: {total_pagados}")
    print(f"Pendientes: {total_pendientes}")

    print(f"Monto recaudado: S/. {monto_pagado}")
    print(f"Monto pendiente: S/. {monto_pendiente}")


# =========================================================
# REPORTES ORDENADOS
# =========================================================

def reporte_ordenado_alumnos():

    imprimir_titulo(
        "=== PAGOS ORDENADOS ==="
    )

    pagos = obtener_pagos()

    ordenados = sorted(

        pagos,

        key=lambda pago:
        pago["nombre_alumno"]

    )

    for pago in ordenados:

        mostrar_pago(pago)


# =========================================================
# MENU INTERNO
# =========================================================

def menu_reporte_pagos():

    while True:

        imprimir_titulo(
            "=== REPORTES PAGOS ==="
        )

        print("""
1. Reporte general
2. Pagos realizados
3. Pagos pendientes
4. Reporte por método
5. Mayores montos
6. Buscar pago
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

                reporte_general_pagos()

            case "2":

                reporte_pagos_pagados()

            case "3":

                reporte_pagos_pendientes()

            # =============================================
            # FILTROS
            # =============================================

            case "4":

                reporte_por_metodo_pago()

            case "5":

                reporte_mayores_montos()

            # =============================================
            # BÚSQUEDAS
            # =============================================

            case "6":

                buscar_pago()

            # =============================================
            # ESTADÍSTICAS
            # =============================================

            case "7":

                estadisticas_pagos()

            # =============================================
            # ORDENAMIENTO
            # =============================================

            case "8":

                reporte_ordenado_alumnos()

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