from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def cargar_notas():

    try:

        datos = leer_json(
            RUTA_NOTAS
        )

        if not isinstance(
            datos,
            list
        ):
            return []

        return datos

    except Exception as e:

        print(
            f"Error al leer notas: {e}"
        )

        return []


def validar_entero(mensaje):

    while True:

        try:

            valor = int(
                input(mensaje).strip()
            )

            if valor <= 0:

                print(
                    "Debe ingresar un número "
                    "mayor a cero."
                )

                continue

            return valor

        except ValueError:

            print(
                "Ingrese un número válido."
            )


def convertir_float(valor):

    try:

        return float(valor)

    except (
        ValueError,
        TypeError
    ):

        return None


def consultar_rendimiento_academico():

    imprimir_titulo(
        "CONSULTAR RENDIMIENTO ACADÉMICO"
    )

    notas = cargar_notas()

    if not notas:

        print(
            "No existen registros "
            "de notas."
        )

        return

    alumnos = {}

    for nota in notas:

        if not isinstance(
            nota,
            dict
        ):
            continue

        if nota.get("estado") != "Activo":
            continue

        id_alumno = nota.get(
            "id_alumno"
        )

        nombre_alumno = nota.get(
            "nombre_alumno",
            "Sin nombre"
        )

        if id_alumno is None:
            continue

        alumnos[id_alumno] = nombre_alumno

    if not alumnos:

        print(
            "No existen alumnos "
            "con registros activos."
        )

        return

    print("\nALUMNOS DISPONIBLES")

    for (
        id_alumno,
        nombre
    ) in sorted(
        alumnos.items()
    ):

        print(
            f"ID: {id_alumno} | "
            f"{nombre}"
        )

    id_alumno = validar_entero(
        "\nIngrese ID del alumno: "
    )

    registros = [

        nota for nota in notas

        if (
            isinstance(
                nota,
                dict
            )
            and nota.get("estado")
            == "Activo"
            and nota.get(
                "id_alumno"
            ) == id_alumno
        )
    ]

    if not registros:

        print(
            "No existen notas "
            "para este alumno."
        )

        return

    imprimir_titulo(
        "RENDIMIENTO ACADÉMICO"
    )

    nombre_alumno = registros[0].get(
        "nombre_alumno",
        "Sin nombre"
    )

    print(
        f"\nAlumno: "
        f"{nombre_alumno}"
    )

    suma = 0
    cantidad = 0

    for registro in registros:

        promedio = convertir_float(
            registro.get(
                "promedio_modulo"
            )
        )

        if promedio is None:
            continue

        suma += promedio
        cantidad += 1

        print(
            f"\nUnidad: "
            f"{registro.get('id_unidad','N/A')}"
            f"\nMódulo: "
            f"{registro.get('id_modulo','N/A')}"
            f"\nPromedio: "
            f"{promedio}"
        )

    if cantidad == 0:

        print(
            "\nNo existen promedios "
            "válidos para calcular."
        )

        return

    promedio_general = round(
        suma / cantidad,
        2
    )

    print(
        f"\nPROMEDIO GENERAL: "
        f"{promedio_general}"
    )

    if promedio_general >= 14:

        print(
            "Rendimiento: Excelente"
        )

    elif promedio_general >= 13:

        print(
            "Rendimiento: Aprobado"
        )

    else:

        print(
            "Rendimiento: Bajo rendimiento"
        )

    print(
        f"\nTOTAL MÓDULOS EVALUADOS: "
        f"{cantidad}"
    )