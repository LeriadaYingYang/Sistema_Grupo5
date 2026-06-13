from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def consultar_rendimiento_academico():

    imprimir_titulo("CONSULTAR RENDIMIENTO ACADÉMICO")

    notas = leer_json(RUTA_NOTAS)

    if not notas:
        print("No existen registros de notas.")
        return

    alumnos = {}

    for nota in notas:

        if nota["estado"] == "Activo":

            alumnos[nota["id_alumno"]] = (
                nota["nombre_alumno"]
            )

    print("\nALUMNOS DISPONIBLES")

    for id_alumno, nombre in alumnos.items():

        print(
            f"ID: {id_alumno} | "
            f"{nombre}"
        )

    try:
        id_alumno = int(
            input("\nIngrese ID del alumno: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    registros = [

        nota

        for nota in notas

        if (
            nota["estado"] == "Activo"
            and nota["id_alumno"] == id_alumno
        )
    ]

    if len(registros) == 0:
        print("No existen notas para este alumno.")
        return

    imprimir_titulo("RENDIMIENTO ACADÉMICO")

    nombre_alumno = registros[0]["nombre_alumno"]

    print(f"\nAlumno: {nombre_alumno}")

    suma = 0

    for registro in registros:

        promedio = registro["promedio_modulo"]

        suma += promedio

        print(
            f"\nUnidad: {registro['id_unidad']}"
            f"\nMódulo: {registro['id_modulo']}"
            f"\nPromedio: {promedio}"
        )

    promedio_general = round(
        suma / len(registros),
        2
    )

    print(
        f"\nPROMEDIO GENERAL: "
        f"{promedio_general}"
    )

    if promedio_general >= 14:
        print("Rendimiento: Excelente")

    elif promedio_general >= 11:
        print("Rendimiento: Aprobado")

    else:
        print("Rendimiento: Bajo rendimiento")