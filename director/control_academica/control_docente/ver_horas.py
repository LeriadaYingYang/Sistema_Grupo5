from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"


def ver_horas_trabajadas():

    imprimir_titulo("VER HORAS TRABAJADAS")

    asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES)

    if not asistencias:
        print("No existen registros de asistencia docente.")
        return

    profesores = {}

    for asistencia in asistencias:

        if asistencia.get("estado") == "Activo":

            profesores[
                asistencia["id_profesor"]
            ] = asistencia.get(
                "nombre_profesor",
                f"Profesor {asistencia['id_profesor']}"
            )

    if not profesores:
        print("No existen profesores con registros.")
        return

    print("\nPROFESORES DISPONIBLES\n")

    for id_profesor, nombre in profesores.items():

        print(
            f"ID: {id_profesor} | "
            f"{nombre}"
        )

    try:

        id_profesor = int(
            input("\nIngrese ID del profesor: ")
        )

    except ValueError:

        print("Debe ingresar un número.")
        return

    registros = [

        asistencia

        for asistencia in asistencias

        if (
            asistencia.get("estado") == "Activo"
            and asistencia["id_profesor"] == id_profesor
        )
    ]

    if len(registros) == 0:

        print("No existen registros para este profesor.")
        return

    imprimir_titulo("HORAS TRABAJADAS")

    nombre_profesor = registros[0].get(
        "nombre_profesor",
        f"Profesor {id_profesor}"
    )

    print(f"\nProfesor: {nombre_profesor}")

    total_horas = 0

    for registro in registros:

        horas = registro.get(
            "horas_trabajadas",
            0
        )

        total_horas += horas

        print(
            f"\nFecha: {registro['fecha']}"
            f"\nHora Entrada: {registro.get('hora_entrada', 'N/A')}"
            f"\nHora Salida: {registro.get('hora_salida', 'N/A')}"
            f"\nHoras Trabajadas: {horas}"
        )

        print("-" * 40)

    print(
        f"\nTOTAL DE HORAS TRABAJADAS: "
        f"{round(total_horas, 2)}"
    )