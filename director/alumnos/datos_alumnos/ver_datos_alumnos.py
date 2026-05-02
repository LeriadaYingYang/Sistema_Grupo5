from basedatos_json import leer_json

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"


def obtener_asignacion(alumno_id, asignaciones):
    """
    Busca la asignación activa de un alumno.
    """
    for asignacion in asignaciones:
        if asignacion["id_alumno"] == alumno_id and asignacion["estado"] == "Activo":
            return asignacion
    return None


def mostrar_alumno(alumno, asignacion):
    """
    Muestra los datos de un alumno de forma ordenada.
    """
    print("\n-----------------------------")
    print(f"ID: {alumno['id_alumno']}")
    print(f"Nombre: {alumno['nombres']} {alumno['apellidos']}")
    print(f"DNI: {alumno['dni']}")
    print(f"Correo: {alumno['correo']}")
    print(f"Celular: {alumno['celular']}")

    if asignacion:
        print(f"Carrera: {asignacion['nombre_carrera']}")
        print(f"Salón: {asignacion['nombre_salon']}")
        print(f"Turno: {asignacion['turno']}")
    else:
        print("Carrera: No asignada")
        print("Salón: No asignado")


def ver_todos_alumnos(alumnos, asignaciones):
    """
    Muestra todos los alumnos activos.
    """
    encontrados = 0

    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            asignacion = obtener_asignacion(alumno["id_alumno"], asignaciones)
            mostrar_alumno(alumno, asignacion)
            encontrados += 1

    if encontrados == 0:
        print("No hay alumnos activos registrados.")


def ver_por_carrera_y_salon(alumnos, asignaciones):
    """
    Primero muestra carreras, luego salones, y finalmente alumnos del salón elegido.
    """

    carreras = []

    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo":
            carrera = {
                "id_carrera": asignacion["id_carrera"],
                "nombre_carrera": asignacion["nombre_carrera"]
            }

            if carrera not in carreras:
                carreras.append(carrera)

    if len(carreras) == 0:
        print("No hay alumnos asignados a carreras.")
        return

    print("\n=== CARRERAS CON ALUMNOS ===")
    for carrera in carreras:
        print(f"ID: {carrera['id_carrera']} | Carrera: {carrera['nombre_carrera']}")

    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    salones = []

    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_carrera"] == id_carrera:
            salon = {
                "id_salon": asignacion["id_salon"],
                "nombre_salon": asignacion["nombre_salon"],
                "turno": asignacion["turno"]
            }

            if salon not in salones:
                salones.append(salon)

    if len(salones) == 0:
        print("No hay salones con alumnos para esa carrera.")
        return

    print("\n=== SALONES DE LA CARRERA ===")
    for salon in salones:
        print(
            f"ID: {salon['id_salon']} | "
            f"Salón: {salon['nombre_salon']} | "
            f"Turno: {salon['turno']}"
        )

    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    encontrados = 0

    print("\n=== ALUMNOS DEL SALÓN ===")

    for alumno in alumnos:
        if alumno["estado"] != "Activo":
            continue

        asignacion = obtener_asignacion(alumno["id_alumno"], asignaciones)

        if asignacion and asignacion["id_carrera"] == id_carrera and asignacion["id_salon"] == id_salon:
            mostrar_alumno(alumno, asignacion)
            encontrados += 1

    if encontrados == 0:
        print("No hay alumnos en ese salón.")


def buscar_por_nombre(alumnos, asignaciones):
    """
    Busca alumnos por nombre o apellido.
    """
    texto = input("Ingrese nombre o apellido a buscar: ").lower()
    encontrados = 0

    for alumno in alumnos:
        nombre_completo = f"{alumno['nombres']} {alumno['apellidos']}".lower()

        if alumno["estado"] == "Activo" and texto in nombre_completo:
            asignacion = obtener_asignacion(alumno["id_alumno"], asignaciones)
            mostrar_alumno(alumno, asignacion)
            encontrados += 1

    if encontrados == 0:
        print("No se encontraron alumnos con ese nombre.")


def buscar_por_dni(alumnos, asignaciones):
    """
    Busca un alumno por DNI exacto.
    """
    dni = input("Ingrese DNI del alumno: ")
    encontrado = False

    for alumno in alumnos:
        if alumno["estado"] == "Activo" and alumno["dni"] == dni:
            asignacion = obtener_asignacion(alumno["id_alumno"], asignaciones)
            mostrar_alumno(alumno, asignacion)
            encontrado = True
            break

    if not encontrado:
        print("No se encontró un alumno con ese DNI.")


def menu_ver_datos_alumnos():
    """
    Submenú para consultar datos de alumnos.
    """

    while True:
        alumnos = leer_json(RUTA_ALUMNOS)
        asignaciones = leer_json(RUTA_ASIGNACIONES)

        print("""
====================================
        VER DATOS DE ALUMNOS
====================================

1. Ver todos los alumnos
2. Ver alumnos por carrera y salón
3. Buscar alumno por nombre
4. Buscar alumno por DNI
5. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_todos_alumnos(alumnos, asignaciones)

        elif opcion == "2":
            ver_por_carrera_y_salon(alumnos, asignaciones)

        elif opcion == "3":
            buscar_por_nombre(alumnos, asignaciones)

        elif opcion == "4":
            buscar_por_dni(alumnos, asignaciones)

        elif opcion == "5":
            print("\nVolviendo al menú director...")
            break

        else:
            print("Opción inválida.")