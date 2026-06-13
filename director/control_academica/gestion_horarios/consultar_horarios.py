from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_HORARIOS = "datos/horarios.json"


def consultar_horarios():

    imprimir_titulo("CONSULTAR HORARIOS")

    horarios = leer_json(RUTA_HORARIOS)

    if not horarios:
        print("No existen horarios registrados.")
        return

    print("\n1. Ver todos")
    print("2. Filtrar por plantilla")
    print("3. Filtrar por carrera")
    print("4. Filtrar por salón")

    opcion = input("\nSeleccione opción: ")

    if opcion == "1":

        mostrar_horarios(
            [h for h in horarios if h["estado"] == "Activo"]
        )

    elif opcion == "2":

        nombre = input(
            "Nombre de plantilla: "
        ).strip().lower()

        filtrados = [
            h for h in horarios
            if h["estado"] == "Activo"
            and nombre in h["nombre_plantilla"].lower()
        ]

        mostrar_horarios(filtrados)

    elif opcion == "3":

        nombre = input(
            "Nombre de carrera: "
        ).strip().lower()

        filtrados = [
            h for h in horarios
            if h["estado"] == "Activo"
            and nombre in h["nombre_carrera"].lower()
        ]

        mostrar_horarios(filtrados)

    elif opcion == "4":

        nombre = input(
            "Nombre de salón: "
        ).strip().lower()

        filtrados = [
            h for h in horarios
            if h["estado"] == "Activo"
            and nombre in h["nombre_salon"].lower()
        ]

        mostrar_horarios(filtrados)

    else:
        print("Opción inválida.")


def mostrar_horarios(lista):

    imprimir_titulo("RESULTADOS")

    if not lista:
        print("No se encontraron registros.")
        return

    for horario in lista:

        print(
            f"\nID Horario: {horario['id_horario']}"
            f"\nPlantilla: {horario['nombre_plantilla']}"
            f"\nCarrera: {horario['nombre_carrera']}"
            f"\nSalón: {horario['nombre_salon']}"
            f"\nTurno: {horario['turno']}"
        )

        print("\nDÍAS Y HORARIOS:")

        for dia in horario["dias_horas"]:

            print(
                f"  {dia['orden']}. "
                f"{dia['dia']} | "
                f"{dia['hora_inicio']} - "
                f"{dia['hora_fin']}"
            )

        print("\n" + "-" * 40)