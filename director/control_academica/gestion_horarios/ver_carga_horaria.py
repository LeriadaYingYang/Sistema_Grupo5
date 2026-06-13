from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASIGNACIONES = "datos/horarios_profesores.json"


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None


def calcular_horas(hora_inicio, hora_fin):
    try:
        inicio = datetime.strptime(hora_inicio, "%H:%M")
        fin = datetime.strptime(hora_fin, "%H:%M")

        horas = (fin - inicio).total_seconds() / 3600

        return round(max(horas, 0), 2)

    except:
        return 0


def mostrar_profesores(profesores):

    imprimir_titulo("PROFESORES DISPONIBLES")

    encontrados = 0

    for profesor in profesores:

        if profesor["estado"] == "Activo":

            encontrados += 1

            print(
                f"ID: {profesor['id_profesor']} | "
                f"{profesor['nombres']} {profesor['apellidos']}"
            )

    if encontrados == 0:
        print("No existen profesores activos.")


def ver_carga_horaria_docente():

    imprimir_titulo("CARGA HORARIA DOCENTE")

    profesores = leer_json(RUTA_PROFESORES)
    horarios = leer_json(RUTA_HORARIOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)

    if len(profesores) == 0:
        print("No existen profesores registrados.")
        return

    if len(asignaciones) == 0:
        print("No existen asignaciones de horarios.")
        return

    mostrar_profesores(profesores)

    try:
        id_profesor = int(
            input("\nIngrese ID del profesor: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    profesor = buscar_por_id(
        profesores,
        "id_profesor",
        id_profesor
    )

    if profesor is None:
        print("Profesor no encontrado.")
        return

    asignaciones_profesor = [
        a for a in asignaciones
        if a["estado"] == "Activo"
        and a["id_profesor"] == id_profesor
    ]

    if len(asignaciones_profesor) == 0:
        print("Este profesor no tiene horarios asignados.")
        return

    imprimir_titulo("DETALLE DE CARGA HORARIA")

    print(
        f"Profesor: "
        f"{profesor['nombres']} "
        f"{profesor['apellidos']}"
    )

    total_horas = 0

    for asignacion in asignaciones_profesor:

        horario = buscar_por_id(
            horarios,
            "id_horario",
            asignacion["id_horario"]
        )

        if horario is None:
            continue

        print(
            f"\nPlantilla: {horario['nombre_plantilla']}"
        )

        print(
            f"Carrera: {horario['nombre_carrera']}"
        )

        print(
            f"Salón: {horario['nombre_salon']}"
        )

        print(
            f"Turno: {horario['turno']}"
        )

        print("\nDÍAS ASIGNADOS:")

        for dia in horario["dias_horas"]:

            horas_dia = calcular_horas(
                dia["hora_inicio"],
                dia["hora_fin"]
            )

            total_horas += horas_dia

            print(
                f"{dia['dia']} | "
                f"{dia['hora_inicio']} - "
                f"{dia['hora_fin']} "
                f"({horas_dia} horas)"
            )

        print("-" * 40)

    print(
        f"\nTOTAL HORAS ASIGNADAS: "
        f"{round(total_horas, 2)} horas"
    )