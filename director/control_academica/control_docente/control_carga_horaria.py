from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


def convertir_hora(hora):
    """
    Convierte formatos:
    08:00
    8
    8 a 9
    """

    try:

        hora = str(hora).strip().lower()

        if ":" in hora:
            return datetime.strptime(
                hora,
                "%H:%M"
            )

        if "a" in hora:
            inicio = hora.split("a")[0].strip()

            if inicio.isdigit():

                return datetime.strptime(
                    f"{int(inicio):02d}:00",
                    "%H:%M"
                )

        if hora.isdigit():

            return datetime.strptime(
                f"{int(hora):02d}:00",
                "%H:%M"
            )

    except:
        pass

    return None


def calcular_horas_programadas(horarios):

    total = 0

    for horario in horarios:

        if horario.get("estado") != "Activo":
            continue

        for dia in horario.get("dias_horas", []):

            inicio = convertir_hora(
                dia.get("hora_inicio")
            )

            fin = convertir_hora(
                dia.get("hora_fin")
            )

            if inicio and fin:

                horas = (
                    fin - inicio
                ).total_seconds() / 3600

                if horas > 0:
                    total += horas

    return round(total, 2)


def control_carga_horaria():

    imprimir_titulo(
        "CONTROL DE CARGA HORARIA DOCENTE"
    )

    profesores = leer_json(
        RUTA_PROFESORES
    )

    asistencias = leer_json(
        RUTA_ASISTENCIA
    )

    horarios = leer_json(
        RUTA_HORARIOS
    )

    if not profesores:
        print(
            "No existen profesores registrados."
        )
        return

    print("\nPROFESORES")

    for profesor in profesores:

        if profesor.get("estado") == "Activo":

            print(
                f"{profesor['id_profesor']} - "
                f"{profesor['nombres']} "
                f"{profesor['apellidos']}"
            )

    try:

        id_profesor = int(
            input(
                "\nIngrese ID del profesor: "
            )
        )

    except ValueError:

        print("Debe ingresar un número.")
        return

    profesor = next(

        (
            p
            for p in profesores
            if p["id_profesor"] == id_profesor
            and p["estado"] == "Activo"
        ),

        None

    )

    if profesor is None:

        print("Profesor no encontrado.")
        return

    horas_trabajadas = 0

    for asistencia in asistencias:

        if (
            asistencia.get(
                "id_profesor"
            ) == id_profesor
        ):

            horas_trabajadas += asistencia.get(
                "horas_trabajadas",
                0
            )

    horas_programadas = calcular_horas_programadas(
        horarios
    )

    if horas_programadas <= 0:

        cumplimiento = 0

    else:

        cumplimiento = round(
            (
                horas_trabajadas
                / horas_programadas
            )
            * 100,
            2
        )

    imprimir_titulo(
        "RESULTADO"
    )

    print(
        f"\nProfesor: "
        f"{profesor['nombres']} "
        f"{profesor['apellidos']}"
    )

    print(
        f"Horas programadas: "
        f"{horas_programadas}"
    )

    print(
        f"Horas trabajadas: "
        f"{round(horas_trabajadas, 2)}"
    )

    print(
        f"Cumplimiento: "
        f"{cumplimiento}%"
    )

    if cumplimiento >= 90:

        print(
            "Estado: Excelente"
        )

    elif cumplimiento >= 70:

        print(
            "Estado: Bueno"
        )

    else:

        print(
            "Estado: Bajo"
        )