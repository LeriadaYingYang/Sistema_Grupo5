from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def cargar_notas():
    """
    Carga las notas desde el archivo JSON.
    """

    try:
        datos = leer_json(RUTA_NOTAS)

        if not isinstance(datos, list):
            print("Error: El archivo de notas no contiene una lista válida.")
            return []

        return datos

    except Exception as e:
        print(f"Error al leer el archivo de notas: {e}")
        return []


def convertir_float(valor):
    """
    Convierte un valor a float de forma segura.
    """

    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def reporte_academico_general():

    imprimir_titulo("REPORTE ACADÉMICO GENERAL")

    notas = cargar_notas()

    if not notas:
        print("No existen registros de notas.")
        return

    alumnos = {}
    registros_validos = 0

    for nota in notas:

        if not isinstance(nota, dict):
            continue

        if nota.get("estado") != "Activo":
            continue

        id_alumno = nota.get("id_alumno")
        nombre_alumno = nota.get("nombre_alumno", "Sin nombre")

        promedio_modulo = convertir_float(
            nota.get("promedio_modulo")
        )

        if id_alumno is None or promedio_modulo is None:
            continue

        registros_validos += 1

        if id_alumno not in alumnos:

            alumnos[id_alumno] = {
                "nombre": nombre_alumno,
                "suma": 0,
                "cantidad": 0
            }

        alumnos[id_alumno]["suma"] += promedio_modulo
        alumnos[id_alumno]["cantidad"] += 1

    if registros_validos == 0:
        print("No existen registros válidos para generar el reporte.")
        return

    total_alumnos = 0
    suma_general = 0
    aprobados = 0
    desaprobados = 0

    mejor_alumno = ""
    mejor_promedio = -1

    peor_alumno = ""
    peor_promedio = 21

    for datos in alumnos.values():

        cantidad = datos.get("cantidad", 0)

        if cantidad <= 0:
            continue

        promedio = round(
            datos["suma"] / cantidad,
            2
        )

        total_alumnos += 1
        suma_general += promedio

        if promedio >= 13:
            aprobados += 1
        else:
            desaprobados += 1

        if promedio > mejor_promedio:
            mejor_promedio = promedio
            mejor_alumno = datos.get(
                "nombre",
                "Sin nombre"
            )

        if promedio < peor_promedio:
            peor_promedio = promedio
            peor_alumno = datos.get(
                "nombre",
                "Sin nombre"
            )

    if total_alumnos == 0:
        print("No existen alumnos evaluados.")
        return

    promedio_general = round(
        suma_general / total_alumnos,
        2
    )

    imprimir_titulo("RESUMEN GENERAL")

    print(
        f"Total de alumnos evaluados: "
        f"{total_alumnos}"
    )

    print(
        f"Promedio académico general: "
        f"{promedio_general}"
    )

    print(
        f"Aprobados (>=13): "
        f"{aprobados}"
    )

    print(
        f"Desaprobados (<13): "
        f"{desaprobados}"
    )

    print(
        f"\nMejor alumno: "
        f"{mejor_alumno}"
    )

    print(
        f"Promedio: "
        f"{mejor_promedio}"
    )

    print(
        f"\nAlumno con menor rendimiento: "
        f"{peor_alumno}"
    )

    print(
        f"Promedio: "
        f"{peor_promedio}"
    )

    print(
        f"\nRegistros válidos analizados: "
        f"{registros_validos}"
    )