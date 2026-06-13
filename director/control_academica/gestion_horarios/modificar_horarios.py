from basedatos_json import leer_json, guardar_json
from director.utilidades import imprimir_titulo

RUTA_HORARIOS = "datos/horarios.json"


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None


def mostrar_horarios(horarios):
    imprimir_titulo("HORARIOS DISPONIBLES")

    encontrados = 0

    for horario in horarios:
        if horario["estado"] == "Activo":

            encontrados += 1

            print(
                f"ID Horario: {horario['id_horario']} | "
                f"Plantilla: {horario['nombre_plantilla']} | "
                f"Carrera: {horario['nombre_carrera']} | "
                f"Salón: {horario['nombre_salon']} | "
                f"Turno: {horario['turno']}"
            )

    if encontrados == 0:
        print("No existen horarios registrados.")


def mostrar_detalle_horario(horario):
    imprimir_titulo("DETALLE DEL HORARIO")

    for dia in horario["dias_horas"]:

        print(
            f"{dia['orden']}. "
            f"{dia['dia']} | "
            f"{dia['hora_inicio']} - "
            f"{dia['hora_fin']}"
        )


def modificar_horarios():

    imprimir_titulo("MODIFICAR HORARIOS")

    horarios = leer_json(RUTA_HORARIOS)

    if len(horarios) == 0:
        print("No existen horarios registrados.")
        return

    mostrar_horarios(horarios)

    try:
        id_horario = int(
            input("\nIngrese ID del horario: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    horario = buscar_por_id(
        horarios,
        "id_horario",
        id_horario
    )

    if horario is None:
        print("Horario no encontrado.")
        return

    while True:

        mostrar_detalle_horario(horario)

        print("\nOPCIONES")
        print("1. Modificar día")
        print("2. Modificar hora inicio")
        print("3. Modificar hora fin")
        print("4. Guardar cambios")
        print("5. Cancelar")

        opcion = input("\nSeleccione opción: ")

        if opcion == "1":

            try:
                orden = int(
                    input("Número de día a modificar: ")
                )

            except ValueError:
                print("Debe ingresar un número.")
                continue

            encontrado = False

            for dia in horario["dias_horas"]:

                if dia["orden"] == orden:

                    nuevo_dia = input(
                        "Nuevo nombre del día: "
                    ).strip()

                    dia["dia"] = nuevo_dia

                    encontrado = True

                    print("Día actualizado correctamente.")
                    break

            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "2":

            try:
                orden = int(
                    input("Número de día a modificar: ")
                )

            except ValueError:
                print("Debe ingresar un número.")
                continue

            encontrado = False

            for dia in horario["dias_horas"]:

                if dia["orden"] == orden:

                    nueva_hora = input(
                        "Nueva hora inicio (HH:MM): "
                    ).strip()

                    dia["hora_inicio"] = nueva_hora

                    encontrado = True

                    print("Hora inicio actualizada.")
                    break

            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "3":

            try:
                orden = int(
                    input("Número de día a modificar: ")
                )

            except ValueError:
                print("Debe ingresar un número.")
                continue

            encontrado = False

            for dia in horario["dias_horas"]:

                if dia["orden"] == orden:

                    nueva_hora = input(
                        "Nueva hora fin (HH:MM): "
                    ).strip()

                    dia["hora_fin"] = nueva_hora

                    encontrado = True

                    print("Hora fin actualizada.")
                    break

            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "4":

            guardar_json(
                RUTA_HORARIOS,
                horarios
            )

            print(
                "\nHorario modificado correctamente."
            )

            break

        elif opcion == "5":

            print("\nOperación cancelada.")
            break

        else:
            print("Opción inválida.")