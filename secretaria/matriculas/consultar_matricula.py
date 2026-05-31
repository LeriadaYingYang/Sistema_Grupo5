from basedatos_json import leer_json
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: consultar_matricula.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_MATRICULAS = "datos/matriculas.json"

def buscar_matricula_por_id(matriculas,id_matricula): # Busca una matrícula según su ID
    for matricula in matriculas:
        if (matricula["id_matricula"] == id_matricula):
            return matricula
    return None

def buscar_matricula_por_alumno(matriculas,id_alumno): # Obtiene todas las matrículas de un alumno
    encontrados = []
    for matricula in matriculas:
        if (matricula["id_alumno"]== id_alumno):
            encontrados.append(matricula)
    return encontrados

def buscar_alumno_por_id(alumnos,id_alumno): # Busca un alumno según su ID
    for alumno in alumnos:
        if (alumno["id_alumno"]== id_alumno):
            return alumno
    return None

def buscar_por_dni(alumnos): # Busca alumnos mediante DNI
    dni = input("Ingresar DNI: ")
    encontrados = []
    for alumno in alumnos:
        if alumno["dni"] == dni:
            encontrados.append(alumno)
    return encontrados

def buscar_por_nombre(alumnos): # Busca alumnos por nombre o apellido
    texto = input("Ingresar nombre/apellido: ").lower()
    encontrados = []
    for alumno in alumnos:
        nombre_completo = (f"{alumno['nombres']} "f"{alumno['apellidos']}").lower()
        if texto in nombre_completo:
            encontrados.append(alumno)
    return encontrados

def mostrar_alumnos(alumnos): # Muestra la lista de alumnos encontrados
    imprimir_titulo("=== ALUMNOS ENCONTRADOS ===")
    if len(alumnos) == 0:
        print("No se encontraron alumnos.")
        return
    for alumno in alumnos:
        print(f"ID: {alumno['id_alumno']} | "
            f"{alumno['nombres']} "
            f"{alumno['apellidos']} | "
            f"DNI: {alumno['dni']}")

def mostrar_matricula(matricula): # Muestra todos los datos de una matrícula
    imprimir_titulo("=== DATOS DE MATRÍCULA ===")
    for clave, valor in matricula.items():
        print(f"{clave}: {valor}")

def mostrar_historial_matriculas(matriculas): # Muestra el historial de matrículas
    imprimir_titulo("=== HISTORIAL DE MATRÍCULAS ===")
    if len(matriculas) == 0:
        print("No existen matrículas.")
        return
    for matricula in matriculas:
        print(f"ID: "f"{matricula['id_matricula']} | "
            f"Periodo: "f"{matricula['periodo']} | "
            f"Carrera: "f"{matricula['carrera']} | "
            f"Estado: "f"{matricula['estado']}")

def consultar_por_id(): # Consulta una matrícula mediante ID
    imprimir_titulo("=== CONSULTAR MATRÍCULA ===")
    matriculas = leer_json(RUTA_MATRICULAS)

# Validar que el ID ingresado sea un número entero
    try:
        id_matricula = int(input("Ingresar ID matrícula: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    matricula = buscar_matricula_por_id(matriculas,id_matricula)
    if matricula is None:
        print("Matrícula no encontrada.")
        return
    mostrar_matricula(matricula)

def consultar_por_alumno(): # Consulta el historial de matrículas de un alumno
    imprimir_titulo("=== CONSULTAR POR ALUMNO ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    matriculas = leer_json(RUTA_MATRICULAS)

# Validar que el ID ingresado sea un número entero
    try:
        id_alumno = int(input("Ingresar ID alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno_por_id(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    historial = buscar_matricula_por_alumno(matriculas,id_alumno)
    print(f"\nAlumno: "
        f"{alumno['nombres']} "
        f"{alumno['apellidos']}")
    mostrar_historial_matriculas(historial)

def consultar_por_dni(): # Consulta alumnos mediante DNI
    imprimir_titulo("=== CONSULTAR POR DNI ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    encontrados = buscar_por_dni(alumnos)
    mostrar_alumnos(encontrados)

def consultar_por_nombre(): # Consulta alumnos mediante nombre
    imprimir_titulo("=== CONSULTAR POR NOMBRE ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    encontrados = buscar_por_nombre(alumnos)
    mostrar_alumnos(encontrados)

def mostrar_matriculas_activas(): # Muestra las matrículas activas registradas
    imprimir_titulo("=== MATRÍCULAS ACTIVAS ===")
    matriculas = leer_json(RUTA_MATRICULAS)
    encontrados = 0
    for matricula in matriculas:
        if matricula["estado"] == "Activa":
            print(f"ID: "
                f"{matricula['id_matricula']} | "
                f"Alumno: "
                f"{matricula['nombre_alumno']} | "
                f"Carrera: "
                f"{matricula['carrera']}")
            encontrados += 1
    if encontrados == 0:
        print("No existen matrículas activas.")

def menu_consultar_matricula(): # Muestra y gestiona el menú de consultas de matrícula
    while True:
        imprimir_titulo("=== CONSULTAR MATRÍCULA ===")
        print("1. Consultar por ID")
        print("2. Consultar por alumno")
        print("3. Buscar por DNI")
        print("4. Buscar por nombre")
        print("5. Mostrar matrículas activas")
        print("6. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":
                consultar_por_id()
            case "2":
                consultar_por_alumno()
            case "3":
                consultar_por_dni()
            case "4":
                consultar_por_nombre()
            case "5":
                mostrar_matriculas_activas()
            case "6":
                print("Regresando a matrículas...")
                break
            case _:
                print("Opción inválida.")