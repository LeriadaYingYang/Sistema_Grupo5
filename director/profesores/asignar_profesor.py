from basedatos_json import leer_json, guardar_json, generar_id

RUTA_PROFESORES = "datos/profesores.json"
RUTA_CURSOS = "datos/cursos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PROFESORES_CURSOS = "datos/profesores_cursos.json"


def mostrar_profesores(profesores):
    """
    Muestra profesores activos.
    """
    print("\n=== PROFESORES DISPONIBLES ===")

    for profesor in profesores:
        if profesor["estado"] == "Activo":
            print(
                f"ID: {profesor['id_profesor']} | "
                f"{profesor['nombres']} {profesor['apellidos']}"
            )


def mostrar_cursos(cursos):
    """
    Muestra cursos activos.
    """
    print("\n=== CURSOS DISPONIBLES ===")

    for curso in cursos:
        if curso["estado"] == "Activo":
            print(
                f"ID: {curso['id_curso']} | "
                f"Carrera: {curso['nombre_carrera']} | "
                f"Unidad: {curso['nombre_unidad']} | "
                f"Curso: {curso['nombre_curso']}"
            )


def mostrar_salones(salones):
    """
    Muestra salones activos.
    """
    print("\n=== SALONES DISPONIBLES ===")

    for salon in salones:
        if salon["estado"] == "Activo":
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Carrera: {salon['nombre_carrera']} | "
                f"Turno: {salon['turno']}"
            )


def buscar_por_id(lista, campo_id, valor_id):
    """
    Busca un elemento activo por su ID.
    """
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None


def ya_existe_asignacion(asignaciones, id_profesor, id_curso, id_salon):
    """
    Evita que se repita la misma asignación.
    """
    for asignacion in asignaciones:
        if (
            asignacion["id_profesor"] == id_profesor and
            asignacion["id_curso"] == id_curso and
            asignacion["id_salon"] == id_salon
        ):
            return True
    return False


def asignar_profesor():#asigna un profesor a un curso y a un salón.


    print("\n====================================")
    print("      ASIGNAR PROFESOR A CURSO")
    print("====================================")

    profesores = leer_json(RUTA_PROFESORES)
    cursos = leer_json(RUTA_CURSOS)
    salones = leer_json(RUTA_SALONES)
    asignaciones = leer_json(RUTA_PROFESORES_CURSOS)

    if len(profesores) == 0:
        print("Primero debe registrar profesores.")
        return

    if len(cursos) == 0:
        print("Primero debe registrar cursos.")
        return

    if len(salones) == 0:
        print("Primero debe registrar salones.")
        return

    mostrar_profesores(profesores)

    try:
        id_profesor = int(input("\nIngrese ID del profesor: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    profesor = buscar_por_id(profesores, "id_profesor", id_profesor)

    if profesor is None:
        print("Profesor no encontrado.")
        return

    mostrar_cursos(cursos)

    try:
        id_curso = int(input("\nIngrese ID del curso: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    curso = buscar_por_id(cursos, "id_curso", id_curso)

    if curso is None:
        print("Curso no encontrado.")
        return

    mostrar_salones(salones)

    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None:
        print("Salón no encontrado.")
        return

    if ya_existe_asignacion(asignaciones, id_profesor, id_curso, id_salon):
        print("Este profesor ya está asignado a ese curso y salón.")
        return

    nueva_asignacion = {
        "id_profesor_curso": generar_id(asignaciones, "id_profesor_curso"),
        "id_profesor": profesor["id_profesor"],
        "nombre_profesor": profesor["nombres"] + " " + profesor["apellidos"],
        "id_curso": curso["id_curso"],
        "nombre_curso": curso["nombre_curso"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "id_carrera": curso["id_carrera"],
        "nombre_carrera": curso["nombre_carrera"],
        "estado": "Activo"
    }

    asignaciones.append(nueva_asignacion)
    guardar_json(RUTA_PROFESORES_CURSOS, asignaciones)

    print("\nProfesor asignado correctamente.")
    print(f"Profesor: {nueva_asignacion['nombre_profesor']}")
    print(f"Curso: {nueva_asignacion['nombre_curso']}")
    print(f"Salón: {nueva_asignacion['nombre_salon']}")