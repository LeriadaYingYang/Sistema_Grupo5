from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None


def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}"
            )


def mostrar_carreras(carreras, id_carrera):
    imprimir_titulo("CARRERA")

    for carrera in carreras:
        if (
            carrera["estado"] == "Activo"
            and carrera["id_carrera"] == id_carrera
        ):
            print(
                f"ID: {carrera['id_carrera']} | "
                f"{carrera['nombre']}"
            )


def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES DISPONIBLES")

    encontrados = 0

    for salon in salones:
        if (
            salon["estado"] == "Activo"
            and salon["id_carrera"] == id_carrera
        ):
            encontrados += 1

            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Turno: {salon['turno']}"
            )

    if encontrados == 0:
        print("No existen salones para esta carrera.")


def horario_ya_existe(horarios, id_plantilla, id_salon):
    for horario in horarios:
        if (
            horario["estado"] == "Activo"
            and horario["id_plantilla"] == id_plantilla
            and horario["id_salon"] == id_salon
        ):
            return True

    return False


def pedir_horarios():
    dias_horas = []

    while True:
        try:
            cantidad = int(
                input("¿Cuántos días tendrá el horario?: ")
            )

            if cantidad <= 0:
                print("Debe ingresar un número mayor a cero.")
                continue

            break

        except ValueError:
            print("Ingrese un número válido.")

    for i in range(1, cantidad + 1):

        print(f"\nDÍA {i}")

        dia = input("Nombre del día: ").strip()

        hora_inicio = input(
            "Hora inicio (HH:MM): "
        ).strip()

        hora_fin = input(
            "Hora fin (HH:MM): "
        ).strip()

        dias_horas.append(
            {
                "orden": i,
                "dia": dia,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin
            }
        )

    return dias_horas


def configurar_horarios():

    imprimir_titulo("CONFIGURAR HORARIOS")

    plantillas = leer_json(RUTA_PLANTILLAS)
    carreras = leer_json(RUTA_CARRERAS)
    salones = leer_json(RUTA_SALONES)
    horarios = leer_json(RUTA_HORARIOS)

    if not plantillas:
        print("No existen plantillas registradas.")
        return

    if not salones:
        print("No existen salones registrados.")
        return

    mostrar_plantillas(plantillas)

    try:
        id_plantilla = int(
            input("\nIngrese ID de plantilla: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    plantilla = buscar_por_id(
        plantillas,
        "id_plantilla",
        id_plantilla
    )

    if plantilla is None:
        print("Plantilla no encontrada.")
        return

    mostrar_carreras(
        carreras,
        plantilla["id_carrera"]
    )

    mostrar_salones(
        salones,
        plantilla["id_carrera"]
    )

    try:
        id_salon = int(
            input("\nIngrese ID del salón: ")
        )

    except ValueError:
        print("Debe ingresar un número.")
        return

    salon = buscar_por_id(
        salones,
        "id_salon",
        id_salon
    )

    if salon is None:
        print("Salón no encontrado.")
        return

    if salon["id_carrera"] != plantilla["id_carrera"]:
        print(
            "El salón no pertenece a la carrera de la plantilla."
        )
        return

    if horario_ya_existe(
        horarios,
        id_plantilla,
        id_salon
    ):
        print(
            "Ya existe un horario configurado para "
            "esta plantilla y salón."
        )
        return

    dias_horas = pedir_horarios()

    nuevo_horario = {
        "id_horario": generar_id(
            horarios,
            "id_horario"
        ),
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "dias_horas": dias_horas,
        "estado": "Activo"
    }

    horarios.append(nuevo_horario)

    guardar_json(
        RUTA_HORARIOS,
        horarios
    )

    print("\nHorario registrado correctamente.")