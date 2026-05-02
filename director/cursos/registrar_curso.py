from basedatos_json import leer_json, guardar_json, generar_id

RUTA_UNIDADES = "datos/unidades.json"
RUTA_CURSOS = "datos/cursos.json"


def mostrar_unidades(unidades):#Muestra las unidades disponibles.

    print("\n=== UNIDADES DISPONIBLES ===")

    for unidad in unidades:
        if unidad["estado"] == "Activo":
            print(
                f"ID: {unidad['id_unidad']} | "
                f"Carrera: {unidad['nombre_carrera']} | "
                f"Unidad: {unidad['nombre_unidad']}"
            )


def buscar_unidad_por_id(unidades, id_unidad):#Busca una unidad activa por su ID.

    for unidad in unidades:
        if unidad["id_unidad"] == id_unidad and unidad["estado"] == "Activo":
            return unidad

    return None


def registrar_curso():#Registra un curso dentro de una unidad.

    print("\n====================================")
    print("        REGISTRAR CURSO")
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
        print("No existe una unidad activa con ese ID.")
        return

    cursos = leer_json(RUTA_CURSOS)

    nombre_curso = input("Nombre del curso: ")
    descripcion = input("Descripción del curso: ")

    nuevo_curso = {
        "id_curso": generar_id(cursos, "id_curso"),
        "id_unidad": unidad["id_unidad"],
        "id_plantilla": unidad["id_plantilla"],
        "id_carrera": unidad["id_carrera"],
        "nombre_carrera": unidad["nombre_carrera"],
        "nombre_unidad": unidad["nombre_unidad"],
        "nombre_curso": nombre_curso,
        "descripcion": descripcion,
        "estado": "Activo"
    }

    cursos.append(nuevo_curso)
    guardar_json(RUTA_CURSOS, cursos)

    print("\nCurso registrado correctamente.")
    print(f"ID curso generado: {nuevo_curso['id_curso']}")
    print(f"Unidad: {nuevo_curso['nombre_unidad']}")
    print(f"Carrera: {nuevo_curso['nombre_carrera']}")