from basedatos_json import leer_json

RUTA_PROFESORES = "datos/profesores.json"
RUTA_ASIGNACIONES = "datos/profesores_salones.json"

def obtener_asignaciones_profesor(id_profesor, asignaciones):#devuelve todas las asignaciones activas de un profesor.

    resultado = []

    for asignacion in asignaciones:
        if asignacion["id_profesor"] == id_profesor and asignacion["estado"] == "Activo":
            resultado.append(asignacion)

    return resultado

def mostrar_profesor(profesor, asignaciones_profesor):#muestra los datos del profesor con sus asignaciones.

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
                f"Carrera: {asignacion['nombre_carrera']} | "
                f"Salón: {asignacion['nombre_salon']} | "
                  f"Turno: {asignacion['turno']}")
    else:
        print("No tiene cursos asignados.")

def ver_todos_profesores(profesores, asignaciones):
    encontrados = 0

    for profesor in profesores:
        if profesor["estado"] == "Activo":
            asignaciones_profesor = obtener_asignaciones_profesor(
                profesor["id_profesor"], asignaciones)
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrados += 1

    if encontrados == 0:
        print("No hay profesores registrados.")

def buscar_por_nombre(profesores, asignaciones):
    texto = input("Ingrese nombre o apellido: ").lower()
    encontrados = 0

    for profesor in profesores:
        nombre_completo = f"{profesor['nombres']} {profesor['apellidos']}".lower()

        if profesor["estado"] == "Activo" and texto in nombre_completo:
            asignaciones_profesor = obtener_asignaciones_profesor(
                profesor["id_profesor"], asignaciones)
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
                profesor["id_profesor"], asignaciones)
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
2. Buscar por nombre
3. Buscar por DNI
4. Volver al menú director
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_todos_profesores(profesores, asignaciones)

        elif opcion == "2":
            buscar_por_nombre(profesores, asignaciones)

        elif opcion == "3":
            buscar_por_dni(profesores, asignaciones)

        elif opcion == "4":
            print("\nVolviendo")
            break

        else:
            print("Opción inválida.")