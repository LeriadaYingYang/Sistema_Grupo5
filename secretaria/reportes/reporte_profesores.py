from basedatos_json import leer_json
from secretaria.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"

def obtener_profesores():
    return leer_json(RUTA_PROFESORES)

def mostrar_profesor(profesor):
    print(
        f"ID: "
        f"{profesor.get('id_profesor', 'N/A')} | "
        f"{profesor.get('nombres', '')} "
        f"{profesor.get('apellidos', '')} | "
        f"DNI: "
        f"{profesor.get('dni', 'No registrado')} | "
        f"Especialidad: "
        f"{profesor.get('especialidad', 'No registrada')} | "
        f"Estado: "
        f"{profesor.get('estado', 'Desconocido')}")

def buscar_profesor_por_id(profesores,id_profesor):
    for profesor in profesores:
        if (profesor["id_profesor"] == id_profesor):
            return profesor
    return None

def reporte_general_profesores():
    imprimir_titulo("=== REPORTE GENERAL PROFESORES ===")
    profesores = obtener_profesores()
    if len(profesores) == 0:
        print("No existen profesores.")
        return
    for profesor in profesores:
        mostrar_profesor(profesor)
    print(f"\nTotal profesores: "
        f"{len(profesores)}")

def reporte_profesores_activos():
    imprimir_titulo("=== PROFESORES ACTIVOS ===")
    profesores = obtener_profesores()
    encontrados = 0
    for profesor in profesores:
        if profesor["estado"] == "Activo":
            mostrar_profesor(profesor)
            encontrados += 1
    if encontrados == 0:
        print("No existen profesores activos.")
    print(f"\nTotal activos: "
        f"{encontrados}")

def reporte_profesores_inactivos():
    imprimir_titulo("=== PROFESORES INACTIVOS ===")
    profesores = obtener_profesores()
    encontrados = 0
    for profesor in profesores:
        if profesor["estado"] == "Inactivo":
            mostrar_profesor(profesor)
            encontrados += 1
    if encontrados == 0:
        print("No existen profesores inactivos.")
    print(f"\nTotal inactivos: "
        f"{encontrados}")

def reporte_por_especialidad():
    imprimir_titulo("=== REPORTE ESPECIALIDAD ===")
    profesores = obtener_profesores()
    especialidad = input("Ingresar especialidad: ").lower()
    encontrados = 0
    for profesor in profesores:
        if (profesor.get("especialidad", "").lower() == especialidad):
            mostrar_profesor(profesor)
            encontrados += 1
    if encontrados == 0:
        print("No existen registros.")
    print(f"\nTotal encontrados: "
        f"{encontrados}")

def buscar_por_id():
    imprimir_titulo("=== BUSCAR PROFESOR ===")
    profesores = obtener_profesores()

# Captura de ID con validación de número entero
    try:
        id_profesor = int(input("Ingresar ID profesor: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    profesor = buscar_profesor_por_id(profesores,id_profesor)
    if profesor is None:
        print("Profesor no encontrado.")
        return
    imprimir_titulo("=== DATOS PROFESOR ===")
    for clave, valor in profesor.items():
        print(f"{clave}: {valor}")

def buscar_por_dni():
    imprimir_titulo("=== BUSCAR POR DNI ===")
    profesores = obtener_profesores()
    dni = input("Ingresar DNI: ")
    encontrados = 0
    for profesor in profesores:
        if profesor["dni"] == dni:
            mostrar_profesor(profesor)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron resultados.")

def buscar_por_nombre():
    imprimir_titulo("=== BUSCAR POR NOMBRE ===")
    profesores = obtener_profesores()
    texto = input("Ingresar nombre/apellido: ").lower()
    encontrados = 0
    for profesor in profesores:
        nombre_completo = (f"{profesor['nombres']} "f"{profesor['apellidos']}").lower()
        if texto in nombre_completo:
            mostrar_profesor(profesor)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron resultados.")

def estadisticas_profesores():
    imprimir_titulo("=== ESTADÍSTICAS PROFESORES ===")
    profesores = obtener_profesores()
    total = len(profesores)
    activos = 0
    inactivos = 0
    especialidades = {}
    for profesor in profesores:
        if profesor["estado"] == "Activo": activos += 1
        elif profesor["estado"] == "Inactivo": inactivos += 1
        especialidad = profesor.get("especialidad", "No registrada")
        if especialidad in especialidades:
            especialidades[especialidad] += 1
        else:
            especialidades[especialidad] = 1
    print(f"Total profesores: {total}")
    print(f"Activos: {activos}")
    print(f"Inactivos: {inactivos}")
    imprimir_titulo("=== ESPECIALIDADES ===")
    for especialidad, cantidad in especialidades.items():
        print(f"{especialidad}: "
            f"{cantidad}")

def reporte_ordenado_apellidos():
    imprimir_titulo("=== REPORTE ORDENADO ===")
    profesores = obtener_profesores()
    ordenados = sorted(profesores,key=lambda profesor:profesor["apellidos"])
    for profesor in ordenados:
        mostrar_profesor(profesor)

def menu_reporte_profesores():
    while True:
        imprimir_titulo("=== REPORTES PROFESORES ===")
        print("""

1. Reporte general
2. Profesores activos
3. Profesores inactivos
4. Reporte por especialidad
5. Buscar por ID
6. Buscar por DNI
7. Buscar por nombre
8. Estadísticas
9. Reporte ordenado
10. Volver

""")
        opcion = input("Seleccionar una opción: ")
        match opcion:
            case "1":reporte_general_profesores()
            case "2":reporte_profesores_activos()
            case "3":reporte_profesores_inactivos()
            case "4":reporte_por_especialidad()
            case "5":buscar_por_id()
            case "6":buscar_por_dni()
            case "7":buscar_por_nombre()
            case "8":estadisticas_profesores()
            case "9":reporte_ordenado_apellidos()
            case "10":
                print("Regresando a reportes...")
                break
            case _:
                print("Opción inválida.")