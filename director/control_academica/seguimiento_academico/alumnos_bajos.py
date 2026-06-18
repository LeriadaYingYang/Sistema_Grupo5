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


def convertir_float(valor):

    try:

        return float(valor)

    except (
        ValueError,
        TypeError
    ):

        return None


def alumnos_bajo_rendimiento():

    imprimir_titulo(
        "ALUMNOS CON BAJO RENDIMIENTO"
    )

    notas = cargar_notas()

    if not notas:

        print(
            "No existen registros "
            "de notas."
        )

        return

    alumnos = {}

    registros_validos = 0

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

        promedio_modulo = convertir_float(
            nota.get(
                "promedio_modulo"
            )
        )

        if (
            id_alumno is None
            or promedio_modulo is None
        ):
            continue

        registros_validos += 1

        if id_alumno not in alumnos:

            alumnos[id_alumno] = {

                "nombre":
                    nombre_alumno,

                "suma":
                    0,

                "cantidad":
                    0
            }

        alumnos[id_alumno][
            "suma"
        ] += promedio_modulo

        alumnos[id_alumno][
            "cantidad"
        ] += 1

    if registros_validos == 0:

        print(
            "No existen registros "
            "válidos para analizar."
        )

        return

    print(
        "\nALUMNOS CON "
        "PROMEDIO MENOR A 13\n"
    )

    encontrados = 0

    for (
        id_alumno,
        datos
    ) in alumnos.items():

        cantidad = datos.get(
            "cantidad",
            0
        )

        if cantidad <= 0:
            continue

        promedio = round(
            datos["suma"] /
            cantidad,
            2
        )

        if promedio < 13:

            encontrados += 1

            print(
                f"ID Alumno: "
                f"{id_alumno}"
            )

            print(
                f"Nombre: "
                f"{datos.get('nombre','N/A')}"
            )

            print(
                f"Promedio General: "
                f"{promedio}"
            )

            print(
                "-" * 40
            )

    if encontrados == 0:

        print(
            "No existen alumnos "
            "con bajo rendimiento."
        )

    else:

        print(
            f"\nTOTAL ALUMNOS "
            f"CON BAJO RENDIMIENTO: "
            f"{encontrados}"
        )

        print(
            f"REGISTROS ANALIZADOS: "
            f"{registros_validos}"
        )