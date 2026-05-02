from basedatos_json import leer_json

RUTA_PROFESORES = "datos/profesores.json"
RUTA_ASIGNACIONES = "datos/profesores_cursos.json"


def obtener_asignaciones_profesor(id_profesor, asignaciones):
    """
    Devuelve todas las asignaciones activas de un profesor.
    """
    resultado = []

    for asignacion in asignaciones:
        if asignacion["id_profesor"] == id_profesor and asignacion["estado"] == "Activo":
            resultado.append(asignacion)

    return resultado


def mostrar_profesor(profesor, asignaciones_profesor):
    """
    Muestra los datos del profesor con sus asignaciones.
    """
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(f"Nombre: {profesor['nombres']} {profesor['apellidos']}")
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")

    if len(asignaciones_profesor) > 0:
        print("\n--- Cursos asignados ---")
        for asignacion in asignaciones_profesor:
            print(
                f"Curso: {asignacion['nombre_curso']} | "
                f"Salón: {asignacion['nombre_salon']} | "
                f"Carrera: {asignacion['nombre_carrera']}"
            )
    else:
        print("No tiene cursos asignados.")


def ver_todos_profesores(profesores, asignaciones):
    encontrados = 0

    for profesor in profesores:
        if profesor["estado"] == "Activo":
            asignaciones_profesor = obtener_asignaciones_profesor(
                profesor["id_profesor"], asignaciones
            )
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrados += 1

    if encontrados == 0:
        print("No hay profesores registrados.")


def ver_por_carrera(profesores, asignaciones):
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
        print("No hay profesores asignados.")
        return

    print("\n=== CARRERAS DISPONIBLES ===")
    for carrera in carreras:
        print(f"ID: {carrera['id_carrera']} | {carrera['nombre_carrera']}")

    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    encontrados = 0

    for profesor in profesores:
        if profesor["estado"] != "Activo":
            continue

        asignaciones_profesor = obtener_asignaciones_profesor(
            profesor["id_profesor"], asignaciones
        )

        asignaciones_filtradas = [
            a for a in asignaciones_profesor if a["id_carrera"] == id_carrera
        ]

        if asignaciones_filtradas:
            mostrar_profesor(profesor, asignaciones_filtradas)
            encontrados += 1

    if encontrados == 0:
        print("No hay profesores en esa carrera.")


def buscar_por_nombre(profesores, asignaciones):
    texto = input("Ingrese nombre o apellido: ").lower()
    encontrados = 0

    for profesor in profesores:
        nombre_completo = f"{profesor['nombres']} {profesor['apellidos']}".lower()

        if profesor["estado"] == "Activo" and texto in nombre_completo:
            asignaciones_profesor = obtener_asignaciones_profesor(
                profesor["id_profesor"], asignaciones
            )
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrados += 1

    if encontrados == 0:
        print("No se encontraron profesores.")


def buscar_por_dni(profesores, asignaciones):
    dni = input("Ingrese DNI: ")
    encontrado = False

    for profesor in profesores:
        if profesor["estado"] == "Activo" and profesor["dni"] == dni:
            asignaciones_profesor = obtener_asignaciones_profesor(
                profesor["id_profesor"], asignaciones
            )
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrado = True
            break

    if not encontrado:
        print("No se encontró profesor con ese DNI.")


def menu_ver_datos_profesores():
    while True:
        profesores = leer_json(RUTA_PROFESORES)
        asignaciones = leer_json(RUTA_ASIGNACIONES)

        print("""
====================================
      VER DATOS DE PROFESORES
====================================

1. Ver todos los profesores
2. Ver profesores por carrera
3. Buscar por nombre
4. Buscar por DNI
5. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_todos_profesores(profesores, asignaciones)

        elif opcion == "2":
            ver_por_carrera(profesores, asignaciones)

        elif opcion == "3":
            buscar_por_nombre(profesores, asignaciones)

        elif opcion == "4":
            buscar_por_dni(profesores, asignaciones)

        elif opcion == "5":
            print("\nVolviendo...")
            break

        else:
            print("Opción inválida.")