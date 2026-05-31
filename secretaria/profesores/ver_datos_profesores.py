from basedatos_json import leer_json

RUTA_PROFESORES = "datos/profesores.json"
RUTA_ASIGNACIONES = "datos/profesores_salones.json"

def obtener_asignaciones_profesor(id_profesor, asignaciones):  #Obtiene todas las asignaciones activas de un profesor
    resultado = []

    for asignacion in asignaciones:
        if asignacion["id_profesor"] == id_profesor and asignacion["estado"] == "Activo":
            resultado.append(asignacion)

    return resultado

def mostrar_profesor(profesor, asignaciones_profesor):  #Muestra los datos personales del profesor y sus salones asignados
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(f"Nombre: {profesor['nombres']} {profesor['apellidos']}")
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")

    if len(asignaciones_profesor) > 0:
        print("\n=== CURSOS ASIGNADOS ===")

        for asignacion in asignaciones_profesor:
            print(
                f"Carrera: {asignacion['nombre_carrera']} | "
                f"Salón: {asignacion['nombre_salon']} | "
                f"Turno: {asignacion['turno']}"
            )
    else:
        print("No tiene cursos asignados.")

def ver_todos_profesores(profesores, asignaciones):  #Muestra todos los profesores activos con sus asignaciones
    encontrados = 0

    for profesor in profesores:
        if profesor["estado"] == "Activo":
            asignaciones_profesor = obtener_asignaciones_profesor(profesor["id_profesor"], asignaciones)
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrados += 1
    if encontrados == 0:
        print("No hay profesores registrados.")

def buscar_por_nombre(profesores, asignaciones):  #Busca profesores activos por nombre o apellido aproximado
    texto = input("Ingresar nombre o apellido: ").lower()
    encontrados = 0

    for profesor in profesores:
        nombre_completo = f"{profesor['nombres']} {profesor['apellidos']}".lower()

        if profesor["estado"] == "Activo" and texto in nombre_completo:
            asignaciones_profesor = obtener_asignaciones_profesor(profesor["id_profesor"], asignaciones)
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron profesores.")

def buscar_por_dni(profesores, asignaciones):  # Busca un profesor activo por dni exacto
    dni = input("Ingresar DNI: ")
    encontrado = False
    for profesor in profesores:
        if profesor["estado"] == "Activo" and profesor["dni"] == dni:
            asignaciones_profesor = obtener_asignaciones_profesor(profesor["id_profesor"], asignaciones)
            mostrar_profesor(profesor, asignaciones_profesor)
            encontrado = True
            break
    if not encontrado:
        print("No se encontró profesor con ese DNI.")

def menu_ver_datos_profesores():  #muestra el menú para consultar información de profesores
    while True:
        profesores = leer_json(RUTA_PROFESORES)  #carga los profesores registrados
        asignaciones = leer_json(RUTA_ASIGNACIONES)  #carga las asignaciones de profesores a salones
        print("""
=== VER DATOS DE PROFESORES ===

1. Ver todos los profesores
2. Buscar por nombre
3. Buscar por DNI
4. Volver al menú director
""")

        opcion = input("Seleccionar una opción: ")

        if opcion == "1":  #Muestra todos los profesores activos
            ver_todos_profesores(profesores, asignaciones)
        elif opcion == "2":  #Busca profesores por nombre o apellido
            buscar_por_nombre(profesores, asignaciones)
        elif opcion == "3":  #Busca profesor por dni
            buscar_por_dni(profesores, asignaciones)
        elif opcion == "4":  #Vuelve al menú anterior
            print("\nVolviendo...")
            break

        else:
            print("Opción inválida.")