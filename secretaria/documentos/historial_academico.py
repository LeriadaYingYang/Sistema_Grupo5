from basedatos_json import leer_json
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: historial_academico.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CERTIFICADOS = "datos/certificados.json"
RUTA_CONSTANCIAS = "datos/constancias.json"

def obtener_asignacion(id_alumno, asignaciones): # Busca la asignación activa de un alumno
    for asignacion in asignaciones:
        if (asignacion["id_alumno"] == id_alumno and asignacion["estado"] == "Activo"):
            return asignacion
    return None

def buscar_alumno_por_id(alumnos, id_alumno): # Busca un alumno activo según su ID
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None

def buscar_por_nombre(alumnos): # Busca alumnos por coincidencia de nombre o apellido
    texto = input("Ingresar nombre/apellido: ").lower()
    encontrados = []
    for alumno in alumnos:
        nombre_completo = (f"{alumno['nombres']} "f"{alumno['apellidos']}").lower()
        if (alumno["estado"] == "Activo" and texto in nombre_completo):
            encontrados.append(alumno)
    return encontrados

def buscar_por_dni(alumnos): # Busca alumnos mediante su DNI
    dni = input("Ingresar DNI: ")
    encontrados = []
    for alumno in alumnos:
        if (alumno["estado"] == "Activo" and alumno["dni"] == dni):
            encontrados.append(alumno)
    return encontrados

def mostrar_datos_generales(alumno,asignacion): # Muestra los datos académicos del alumno
    imprimir_titulo("=== DATOS ACADÉMICOS ===")
    print(f"Alumno: "f"{alumno['nombres']} "f"{alumno['apellidos']}")
    print(f"DNI: {alumno['dni']}")
    if asignacion:
        print(f"Carrera: "f"{asignacion['nombre_carrera']}")
        print(f"Salón: "f"{asignacion['nombre_salon']}")
        print(f"Turno: "f"{asignacion['turno']}")
    else:
        print("Sin asignación académica.")

def mostrar_historial(alumno,certificados,constancias): # Muestra certificados y constancias del alumno
    imprimir_titulo("=== HISTORIAL DOCUMENTAL ===")
    encontrados = 0
    for certificado in certificados:
        if (certificado["id_alumno"] == alumno["id_alumno"]):
            print(f"[CERTIFICADO] "f"{certificado['tipo_certificado']}")
            encontrados += 1
    for constancia in constancias:
        if (constancia["id_alumno"]== alumno["id_alumno"]):
            print(f"[CONSTANCIA] "f"{constancia['tipo_constancia']}")
            encontrados += 1
    if encontrados == 0:
        print("No existen registros.")

def mostrar_alumnos(encontrados): # Muestra los alumnos encontrados en la búsqueda
    imprimir_titulo("=== RESULTADOS ===")
    if len(encontrados) == 0:
        print("No se encontraron alumnos.")
        return
    for alumno in encontrados:
        print(f"ID: {alumno['id_alumno']} | "
            f"{alumno['nombres']} "
            f"{alumno['apellidos']} | "
            f"DNI: {alumno['dni']}")

def consultar_por_id(): # Consulta información académica mediante ID
    imprimir_titulo("=== CONSULTA POR ID ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    certificados = leer_json(RUTA_CERTIFICADOS)
    constancias = leer_json(RUTA_CONSTANCIAS)

#Controlando errores al ingresar ID de alumno
    try:
        id_alumno = int(input("Ingresar ID: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno_por_id(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    asignacion = obtener_asignacion(id_alumno,asignaciones)
    mostrar_datos_generales(alumno,asignacion)
    mostrar_historial(alumno,certificados,constancias)

def consultar_por_nombre(): # Realiza búsqueda de alumnos por nombre
    imprimir_titulo("=== CONSULTA POR NOMBRE ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    encontrados = buscar_por_nombre(alumnos)
    mostrar_alumnos(encontrados)

def consultar_por_dni(): # Realiza búsqueda de alumnos por DNI
    imprimir_titulo("=== CONSULTA POR DNI ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    encontrados = buscar_por_dni(alumnos)
    mostrar_alumnos(encontrados)

def mostrar_todo_historial(): # Muestra todos los alumnos activos registrados
    imprimir_titulo("=== HISTORIAL GENERAL ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    activos = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            print(f"{alumno['id_alumno']} | "
                f"{alumno['nombres']} "
                f"{alumno['apellidos']}")
            activos += 1
    if activos == 0:
        print("No hay alumnos activos.")

def menu_historial_academico(): # Muestra y gestiona el menú de historial académico
    while True:
        imprimir_titulo("=== MENU HISTORIAL ACADÉMICO ===")
        print("1. Consultar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por DNI")
        print("4. Mostrar alumnos activos")
        print("5. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":consultar_por_id()
            case "2":consultar_por_nombre()
            case "3":consultar_por_dni()
            case "4":mostrar_todo_historial()
            case "5":
                print("Regresando al menú de documentos...")
                break
            case _:
                print("Opción inválida.")