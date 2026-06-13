from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def ver_notas_unidad():

    imprimir_titulo("VER NOTAS POR UNIDAD")

    notas = leer_json(RUTA_NOTAS)

    if not notas:
        print("No existen registros de notas.")
        return

    unidades = sorted(
        list(
            set(
                nota["id_unidad"]
                for nota in notas
                if nota["estado"] == "Activo"
            )
        )
    )

    print("\nUNIDADES DISPONIBLES")

    for unidad in unidades:
        print(f"Unidad ID: {unidad}")

    try:
        id_unidad = int(
            input("\nIngrese ID de la unidad: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    resultados = [

        nota

        for nota in notas

        if (
            nota["estado"] == "Activo"
            and nota["id_unidad"] == id_unidad
        )
    ]

    if len(resultados) == 0:
        print("No existen notas para esta unidad.")
        return

    imprimir_titulo("NOTAS DE LA UNIDAD")

    suma = 0

    for registro in resultados:

        promedio = registro["promedio_modulo"]

        suma += promedio

        print(
            f"\nAlumno: {registro['nombre_alumno']}"
            f"\nID Módulo: {registro['id_modulo']}"
            f"\nPromedio: {promedio}"
        )

        print("\nDETALLE DE ACTIVIDADES")

        for grupo in registro["grupos"]:

            print(
                f"\nGrupo: {grupo['nombre_grupo']}"
            )

            print(
                f"Promedio Grupo: "
                f"{grupo['promedio_grupo']}"
            )

            for actividad in grupo["actividades"]:

                print(
                    f"  - {actividad['nombre_actividad']}: "
                    f"{actividad['nota']}"
                )

        print("\n" + "-" * 40)

    promedio_general = round(
        suma / len(resultados),
        2
    )

    print(
        f"\nPROMEDIO GENERAL DE LA UNIDAD: "
        f"{promedio_general}"
    )