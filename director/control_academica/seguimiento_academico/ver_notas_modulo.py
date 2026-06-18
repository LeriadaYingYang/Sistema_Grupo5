from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def cargar_notas():
    try:
        datos = leer_json(RUTA_NOTAS)

        if not isinstance(datos, list):
            return []

        return datos

    except Exception as e:
        print(f"Error al leer las notas: {e}")
        return []


def validar_entero(mensaje):

    while True:

        try:
            valor = int(input(mensaje).strip())

            if valor <= 0:
                print("Debe ingresar un número mayor a cero.")
                continue

            return valor

        except ValueError:
            print("Ingrese un número válido.")


def convertir_float(valor):

    try:
        return float(valor)

    except (ValueError, TypeError):
        return None


def ver_notas_modulo():

    imprimir_titulo("VER NOTAS POR MÓDULO")

    notas = cargar_notas()

    if not notas:
        print("No existen registros de notas.")
        return

    modulos = sorted(
        {
            nota.get("id_modulo")
            for nota in notas
            if (
                isinstance(nota, dict)
                and nota.get("estado") == "Activo"
                and nota.get("id_modulo") is not None
            )
        }
    )

    if not modulos:
        print("No existen módulos con registros activos.")
        return

    print("\nMÓDULOS DISPONIBLES")

    for modulo in modulos:
        print(f"Módulo ID: {modulo}")

    id_modulo = validar_entero(
        "\nIngrese ID del módulo: "
    )

    resultados = [

        nota for nota in notas

        if (
            isinstance(nota, dict)
            and nota.get("estado") == "Activo"
            and nota.get("id_modulo") == id_modulo
        )
    ]

    if not resultados:
        print("No existen notas para ese módulo.")
        return

    imprimir_titulo("NOTAS DEL MÓDULO")

    suma = 0
    cantidad = 0

    for registro in resultados:

        promedio = convertir_float(
            registro.get("promedio_modulo")
        )

        if promedio is None:
            continue

        suma += promedio
        cantidad += 1

        print(
            f"\nAlumno: "
            f"{registro.get('nombre_alumno', 'N/A')}"
            f"\nID Unidad: "
            f"{registro.get('id_unidad', 'N/A')}"
            f"\nPromedio Módulo: "
            f"{promedio}"
        )

        print("\nDetalle:")

        grupos = registro.get(
            "grupos",
            []
        )

        if not isinstance(grupos, list) or not grupos:
            print("Sin grupos registrados.")
        else:

            for grupo in grupos:

                if not isinstance(grupo, dict):
                    continue

                print(
                    f"\nGrupo: "
                    f"{grupo.get('nombre_grupo', 'N/A')}"
                )

                print(
                    f"Promedio Grupo: "
                    f"{grupo.get('promedio_grupo', 'N/A')}"
                )

                actividades = grupo.get(
                    "actividades",
                    []
                )

                if (
                    not isinstance(
                        actividades,
                        list
                    )
                    or not actividades
                ):
                    print(
                        "  Sin actividades registradas."
                    )
                else:

                    for actividad in actividades:

                        if not isinstance(
                            actividad,
                            dict
                        ):
                            continue

                        print(
                            f"  - "
                            f"{actividad.get('nombre_actividad', 'N/A')}: "
                            f"{actividad.get('nota', 'N/A')}"
                        )

        print("\n" + "-" * 40)

    if cantidad == 0:
        print(
            "\nNo existen promedios válidos "
            "para calcular."
        )
        return

    promedio_general = round(
        suma / cantidad,
        2
    )

    print(
        f"\nPROMEDIO GENERAL DEL MÓDULO: "
        f"{promedio_general}"
    )

    print(
        f"TOTAL REGISTROS ANALIZADOS: "
        f"{cantidad}"
    )