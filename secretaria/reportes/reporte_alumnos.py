from basedatos_json import leer_json
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: reporte_alumnos.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_ALUMNOS = "datos/alumnos.json"

def obtener_alumnos(): # Obtiene la lista de alumnos desde el archivo JSON
    return leer_json(RUTA_ALUMNOS)

def mostrar_alumno(alumno): # Muestra la información básica de un alumno
    print(f"ID: {alumno['id_alumno']} | "
        f"{alumno['nombres']} "
        f"{alumno['apellidos']} | "
        f"DNI: {alumno['dni']} | "
        f"Estado: {alumno['estado']}")

def buscar_alumno_por_id(alumnos,id_alumno): # Busca un alumno según su ID
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno):
            return alumno
    return None

def reporte_general_alumnos(): # Muestra el reporte general de alumnos
    imprimir_titulo("=== REPORTE GENERAL ALUMNOS ===")
    alumnos = obtener_alumnos()
    if len(alumnos) == 0:
        print("No existen alumnos.")
        return
    for alumno in alumnos:
        mostrar_alumno(alumno)
    print(f"\nTotal alumnos: "
        f"{len(alumnos)}")

def reporte_alumnos_activos(): # Muestra únicamente los alumnos activos
    imprimir_titulo("=== ALUMNOS ACTIVOS ===")
    alumnos = obtener_alumnos()
    encontrados = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            mostrar_alumno(alumno)
            encontrados += 1
    if encontrados == 0:
        print("No existen alumnos activos.")
    print(f"\nTotal activos: "
        f"{encontrados}")

def reporte_alumnos_inactivos(): # Muestra únicamente los alumnos inactivos
    imprimir_titulo("=== ALUMNOS INACTIVOS ===")
    alumnos = obtener_alumnos()
    encontrados = 0
    for alumno in alumnos:
        if alumno["estado"] == "Inactivo":
            mostrar_alumno(alumno)
            encontrados += 1
    if encontrados == 0:
        print("No existen alumnos inactivos.")
    print(f"\nTotal inactivos: "
        f"{encontrados}")

def buscar_por_dni(): # Busca alumnos mediante DNI
    imprimir_titulo("=== BUSCAR POR DNI ===")
    alumnos = obtener_alumnos()
    dni = input("Ingresar DNI: ")
    encontrados = 0
    for alumno in alumnos:
        if alumno["dni"] == dni:
            mostrar_alumno(alumno)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron resultados.")

def buscar_por_nombre(): # Busca alumnos por nombre o apellido
    imprimir_titulo("=== BUSCAR POR NOMBRE ===")
    alumnos = obtener_alumnos()
    texto = input("Ingresar nombre/apellido: ").lower()
    encontrados = 0
    for alumno in alumnos:
        nombre_completo = (f"{alumno['nombres']} "f"{alumno['apellidos']}").lower()
        if texto in nombre_completo:
            mostrar_alumno(alumno)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron resultados.")

def buscar_por_id(): # Busca y muestra un alumno por ID
    imprimir_titulo("=== BUSCAR POR ID ===")
    alumnos = obtener_alumnos()

#Captura de ID con validación de tipo numérico
    try:
        id_alumno = int(input("Ingresar ID alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno_por_id(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    imprimir_titulo("=== DATOS DEL ALUMNO ===")
    for clave, valor in alumno.items(): # Muestra toda la información del alumno
        print(f"{clave}: {valor}")

def estadisticas_alumnos(): # Muestra estadísticas generales de alumnos
    imprimir_titulo("=== ESTADÍSTICAS ALUMNOS ===")
    alumnos = obtener_alumnos()
    total = len(alumnos)
    activos = 0
    inactivos = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo": 
            activos += 1
        elif alumno["estado"] == "Inactivo":
            inactivos += 1
    print(f"Total alumnos: {total}")
    print(f"Activos: {activos}")
    print(f"Inactivos: {inactivos}")

def reporte_ordenado_apellidos(): # Ordena los alumnos por apellido
    imprimir_titulo("=== REPORTE ORDENADO ===")
    alumnos = obtener_alumnos()
    alumnos_ordenados = sorted( # Ordena alfabéticamente por apellidos
        alumnos,
        key=lambda alumno:
        alumno["apellidos"]
    )
    for alumno in alumnos_ordenados:
        mostrar_alumno(alumno)

def menu_reporte_alumnos(): # Muestra y gestiona el menú de reportes
    while True:
        imprimir_titulo("=== REPORTES ALUMNOS ===")
        print("""
1. Reporte general
2. Alumnos activos
3. Alumnos inactivos
4. Buscar por ID
5. Buscar por DNI
6. Buscar por nombre
7. Estadísticas
8. Reporte ordenado
9. Volver
""")
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "1":reporte_general_alumnos()
            case "2":reporte_alumnos_activos()
            case "3":reporte_alumnos_inactivos()
            case "4":buscar_por_id()
            case "5":buscar_por_dni()
            case "6":buscar_por_nombre()
            case "7":estadisticas_alumnos()
            case "8":reporte_ordenado_apellidos()
            case "9":
                print("Regresando a reportes...")
                break
            case _:
                print("Opción inválida.")