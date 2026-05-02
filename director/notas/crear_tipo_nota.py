from basedatos_json import leer_json, guardar_json, generar_id

RUTA_UNIDADES = "datos/unidades.json"
RUTA_TIPOS_NOTAS = "datos/tipos_notas.json"


def mostrar_unidades(unidades):
    print("\n=== UNIDADES DISPONIBLES ===")

    for unidad in unidades:
        if unidad["estado"] == "Activo":
            print(
                f"ID: {unidad['id_unidad']} | "
                f"Carrera: {unidad['nombre_carrera']} | "
                f"Unidad: {unidad['nombre_unidad']}"
            )


def buscar_unidad_por_id(unidades, id_unidad):
    for unidad in unidades:
        if unidad["id_unidad"] == id_unidad and unidad["estado"] == "Activo":
            return unidad
    return None


def calcular_total_porcentaje(tipos_notas, id_unidad):#Suma los porcentajes existentes de una unidad.

    total = 0
    for nota in tipos_notas:
        if nota["id_unidad"] == id_unidad:
            total += nota["porcentaje"]
    return total


def crear_tipo_nota():
    print("\n====================================")
    print("   CREAR TIPOS DE NOTAS POR UNIDAD")
    print("====================================")

    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("Primero debe registrar una unidad.")
        return

    mostrar_unidades(unidades)

    try:
        id_unidad = int(input("\nIngrese el ID de la unidad: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    unidad = buscar_unidad_por_id(unidades, id_unidad)

    if unidad is None:
        print("Unidad no encontrada.")
        return

    tipos_notas = leer_json(RUTA_TIPOS_NOTAS)

    #mostrar porcentaje actual
    total_actual = calcular_total_porcentaje(tipos_notas, id_unidad)

    print(f"\nPorcentaje actual acumulado: {total_actual}%")

    if total_actual >= 100:
        print("Ya se completó el 100% para esta unidad.")
        return

    nombre = input("Nombre del tipo de nota: ")

    while True:
        try:
            porcentaje = float(input("Porcentaje (%): "))
            break
        except ValueError:
            print("Ingrese un número válido.")

    if total_actual + porcentaje > 100:
        print("Error: se excede el 100%.")
        return

    nuevo_tipo = {
        "id_tipo_nota": generar_id(tipos_notas, "id_tipo_nota"),
        "id_unidad": unidad["id_unidad"],
        "nombre_unidad": unidad["nombre_unidad"],
        "nombre_carrera": unidad["nombre_carrera"],
        "nombre_nota": nombre,
        "porcentaje": porcentaje,
        "estado": "Activo"
    }

    tipos_notas.append(nuevo_tipo)
    guardar_json(RUTA_TIPOS_NOTAS, tipos_notas)

    print("\nTipo de nota registrado correctamente.")
    print(f"Unidad: {nuevo_tipo['nombre_unidad']}")
    print(f"Nota: {nuevo_tipo['nombre_nota']} ({porcentaje}%)")

    nuevo_total = calcular_total_porcentaje(tipos_notas, id_unidad)
    print(f"Nuevo total acumulado: {nuevo_total}%")