from basedatos_json import (leer_json,guardar_json,generar_id)
from secretaria.utilidades import (imprimir_titulo)

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_MATRICULAS = "datos/matriculas.json"

def buscar_alumno(alumnos,id_alumno):
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None


def buscar_matricula(
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


def obtener_matricula_activa(
    matriculas,
    id_alumno
):

    for matricula in matriculas:

        if (
            matricula["id_alumno"]
            == id_alumno
            and matricula["estado"]
            == "Activa"
        ):

            return matricula

    return None


def mostrar_matriculas_activas():

    imprimir_titulo(
        "=== MATRÍCULAS ACTIVAS ==="
    )

    matriculas = leer_json(
        RUTA_MATRICULAS
    )

    encontrados = 0

    for matricula in matriculas:

        if matricula["estado"] == "Activa":

            print(
                f"ID: "
                f"{matricula['id_matricula']} | "

                f"Alumno: "
                f"{matricula['nombre_alumno']} | "

                f"Periodo: "
                f"{matricula['periodo']} | "

                f"Ciclo: "
                f"{matricula['ciclo']}"
            )

            encontrados += 1

    if encontrados == 0:
        print("No existen matrículas activas.")


# =========================================================
# RENOVACIÓN PRINCIPAL
# =========================================================

def renovar_matricula():

    imprimir_titulo(
        "=== RENOVAR MATRÍCULA ==="
    )

    alumnos = leer_json(
        RUTA_ALUMNOS
    )

    matriculas = leer_json(
        RUTA_MATRICULAS
    )

    mostrar_matriculas_activas()

    # =====================================================
    # VALIDAR ID MATRÍCULA
    # =====================================================

    try:

        id_matricula = int(
            input(
                "\nIngresar ID matrícula: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    matricula_actual = buscar_matricula(
        matriculas,
        id_matricula
    )

    if matricula_actual is None:
        print("Matrícula no encontrada.")
        return

    if matricula_actual["estado"] != "Activa":

        print(
            "La matrícula no se encuentra activa."
        )

        return

    # =====================================================
    # DATOS NUEVOS
    # =====================================================

    nuevo_periodo = input(
        "Nuevo periodo académico: "
    )

    nuevo_ciclo = input(
        "Nuevo ciclo: "
    )

    # =====================================================
    # FINALIZAR MATRÍCULA ANTERIOR
    # =====================================================

    matricula_actual["estado"] = "Finalizada"

    # =====================================================
    # CREAR NUEVA MATRÍCULA
    # =====================================================

    nueva_matricula = {

        "id_matricula":

            generar_id(
                matriculas,
                "id_matricula"
            ),

        "id_alumno":
            matricula_actual["id_alumno"],

        "nombre_alumno":
            matricula_actual["nombre_alumno"],

        "dni":
            matricula_actual["dni"],

        "carrera":
            matricula_actual["carrera"],

        "salon":
            matricula_actual["salon"],

        "turno":
            matricula_actual["turno"],

        "periodo":
            nuevo_periodo,

        "ciclo":
            nuevo_ciclo,

        "estado":
            "Activa"
    }

    matriculas.append(
        nueva_matricula
    )

    guardar_json(
        RUTA_MATRICULAS,
        matriculas
    )

    # =====================================================
    # RESULTADO
    # =====================================================

    imprimir_titulo(
        "=== MATRÍCULA RENOVADA ==="
    )

    print(
        f"Nueva matrícula: "
        f"{nueva_matricula['id_matricula']}"
    )

    print(
        f"Alumno: "
        f"{nueva_matricula['nombre_alumno']}"
    )

    print(
        f"Periodo: "
        f"{nueva_matricula['periodo']}"
    )

    print(
        f"Estado: "
        f"{nueva_matricula['estado']}"
    )


# =========================================================
# CONSULTAS
# =========================================================

def mostrar_historial_renovaciones():

    imprimir_titulo(
        "=== HISTORIAL MATRÍCULAS ==="
    )

    matriculas = leer_json(
        RUTA_MATRICULAS
    )

    if len(matriculas) == 0:
        print("No existen matrículas.")
        return

    for matricula in matriculas:

        print(
            f"ID: "
            f"{matricula['id_matricula']} | "

            f"{matricula['nombre_alumno']} | "

            f"{matricula['periodo']} | "

            f"{matricula['estado']}"
        )


def buscar_renovacion_por_id():

    imprimir_titulo(
        "=== BUSCAR MATRÍCULA ==="
    )

    matriculas = leer_json(
        RUTA_MATRICULAS
    )

    try:

        id_matricula = int(
            input(
                "Ingresar ID matrícula: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    matricula = buscar_matricula(
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
# ACTUALIZACIÓN ESTADOS
# =========================================================

def actualizar_estado_renovacion():

    imprimir_titulo(
        "=== ACTUALIZAR ESTADO ==="
    )

    matriculas = leer_json(
        RUTA_MATRICULAS
    )

    try:

        id_matricula = int(
            input(
                "Ingresar ID matrícula: "
            )
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    matricula = buscar_matricula(
        matriculas,
        id_matricula
    )

    if matricula is None:
        print("Matrícula no encontrada.")
        return

    print("""

1. Activa
2. Finalizada
3. Retirada

""")

    opcion = input(
        "Seleccionar estado: "
    )

    estados = {

        "1": "Activa",

        "2": "Finalizada",

        "3": "Retirada"
    }

    if opcion not in estados:
        print("Opción inválida.")
        return

    matricula["estado"] = estados[opcion]

    guardar_json(
        RUTA_MATRICULAS,
        matriculas
    )

    print(
        "Estado actualizado correctamente."
    )


# =========================================================
# MENU INTERNO
# =========================================================

def menu_renovar_matricula():

    while True:

        imprimir_titulo(
            "=== MENU RENOVAR MATRÍCULA ==="
        )

        print("1. Renovar matrícula")
        print("2. Mostrar historial")
        print("3. Mostrar activas")
        print("4. Buscar matrícula")
        print("5. Actualizar estado")
        print("6. Volver")

        opcion = input(
            "\nSeleccione una opción: "
        )

        match opcion:

            case "1":
                renovar_matricula()

            case "2":
                mostrar_historial_renovaciones()

            case "3":
                mostrar_matriculas_activas()

            case "4":
                buscar_renovacion_por_id()

            case "5":
                actualizar_estado_renovacion()

            case "6":
                print("Regresando...")
                break

            case _:
                print("Opción inválida.")