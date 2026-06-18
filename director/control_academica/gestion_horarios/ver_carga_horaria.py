from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASIGNACIONES = "datos/horarios_profesores.json"


def cargar_datos(ruta):
    try:
        datos = leer_json(ruta)

        if not isinstance(datos, list):
            return []

        return datos

    except Exception as e:
        print(f"Error al leer datos: {e}")
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


def validar_hora(hora):

    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False


def buscar_por_id(lista, campo_id, valor_id):

    if not isinstance(lista, list):
        return None

    for item in lista:

        if (
            item.get(campo_id) == valor_id
            and item.get("estado") == "Activo"
        ):
            return item

    return None


def calcular_horas(hora_inicio, hora_fin):

    try:

        if (
            not validar_hora(hora_inicio)
            or not validar_hora(hora_fin)
        ):
            return 0

        inicio = datetime.strptime(
            hora_inicio,
            "%H:%M"
        )

        fin = datetime.strptime(
            hora_fin,
            "%H:%M"
        )

        horas = (
            fin - inicio
        ).total_seconds() / 3600

        return round(
            max(horas, 0),
            2
        )

    except Exception:
        return 0


def mostrar_profesores(profesores):

    imprimir_titulo(
        "PROFESORES DISPONIBLES"
    )

    encontrados = 0

    for profesor in profesores:

        if profesor.get("estado") == "Activo":

            encontrados += 1

            print(
                f"ID: {profesor.get('id_profesor','N/A')} | "
                f"{profesor.get('nombres','')} "
                f"{profesor.get('apellidos','')}"
            )

    if encontrados == 0:
        print("No existen profesores activos.")


def ver_carga_horaria_docente():

    imprimir_titulo(
        "CARGA HORARIA DOCENTE"
    )

    profesores = cargar_datos(
        RUTA_PROFESORES
    )

    horarios = cargar_datos(
        RUTA_HORARIOS
    )

    asignaciones = cargar_datos(
        RUTA_ASIGNACIONES
    )

    profesores_activos = [
        p for p in profesores
        if p.get("estado") == "Activo"
    ]

    if not profesores_activos:
        print("No existen profesores activos.")
        return

    asignaciones_activas = [
        a for a in asignaciones
        if a.get("estado") == "Activo"
    ]

    if not asignaciones_activas:
        print("No existen asignaciones activas.")
        return

    mostrar_profesores(
        profesores_activos
    )

    id_profesor = validar_entero(
        "\nIngrese ID del profesor: "
    )

    profesor = buscar_por_id(
        profesores,
        "id_profesor",
        id_profesor
    )

    if profesor is None:

        print(
            "Profesor no encontrado."
        )

        return

    asignaciones_profesor = [

        a for a in asignaciones_activas

        if a.get("id_profesor")
        == id_profesor
    ]

    if not asignaciones_profesor:

        print(
            "Este profesor no tiene "
            "horarios asignados."
        )

        return

    imprimir_titulo(
        "DETALLE DE CARGA HORARIA"
    )

    print(
        f"Profesor: "
        f"{profesor.get('nombres','')} "
        f"{profesor.get('apellidos','')}"
    )

    total_horas = 0
    total_horarios = 0

    for asignacion in asignaciones_profesor:

        horario = buscar_por_id(
            horarios,
            "id_horario",
            asignacion.get(
                "id_horario"
            )
        )

        if horario is None:
            continue

        total_horarios += 1

        print(
            f"\nPlantilla: "
            f"{horario.get('nombre_plantilla','N/A')}"
        )

        print(
            f"Carrera: "
            f"{horario.get('nombre_carrera','N/A')}"
        )

        print(
            f"Salón: "
            f"{horario.get('nombre_salon','N/A')}"
        )

        print(
            f"Turno: "
            f"{horario.get('turno','N/A')}"
        )

        print("\nDÍAS ASIGNADOS:")

        dias_horas = horario.get(
            "dias_horas",
            []
        )

        if (
            not isinstance(
                dias_horas,
                list
            )
            or not dias_horas
        ):

            print(
                "No existen días "
                "configurados."
            )

            continue

        for dia in dias_horas:

            hora_inicio = dia.get(
                "hora_inicio",
                ""
            )

            hora_fin = dia.get(
                "hora_fin",
                ""
            )

            horas_dia = calcular_horas(
                hora_inicio,
                hora_fin
            )

            total_horas += horas_dia

            print(
                f"{dia.get('dia','N/A')} | "
                f"{hora_inicio} - "
                f"{hora_fin} "
                f"({horas_dia} horas)"
            )

        print("-" * 40)

    if total_horarios == 0:

        print(
            "\nNo se encontraron "
            "horarios válidos."
        )

        return

    print(
        f"\nHORARIOS ASIGNADOS: "
        f"{total_horarios}"
    )

    print(
        f"TOTAL HORAS ASIGNADAS: "
        f"{round(total_horas, 2)} horas"
    )