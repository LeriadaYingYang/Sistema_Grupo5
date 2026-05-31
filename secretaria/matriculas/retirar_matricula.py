from basedatos_json import leer_json,guardar_json
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: retirar_matricula.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_MATRICULAS = "datos/matriculas.json"

def buscar_matricula(matriculas,id_matricula): # Busca una matrícula según su ID
    for matricula in matriculas:
        if (matricula["id_matricula"] == id_matricula):
            return matricula
    return None

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
                f"{matricula['carrera']} | "
                f"Periodo: "
                f"{matricula['periodo']}")
            encontrados += 1
    if encontrados == 0:
        print("No existen matrículas activas.")

def mostrar_historial_retiros(): # Muestra el historial de matrículas retiradas
    imprimir_titulo("=== HISTORIAL RETIROS ===")
    matriculas = leer_json(RUTA_MATRICULAS)
    encontrados = 0
    for matricula in matriculas:
        if matricula["estado"] == "Retirada":
            print(f"ID: "
                f"{matricula['id_matricula']} | "
                f"{matricula['nombre_alumno']} | "
                f"Motivo: "
                f"{matricula.get('motivo_retiro', 'N/A')}")
            encontrados += 1
    if encontrados == 0:
        print("No existen retiros registrados.")

def retirar_matricula(): # Retira una matrícula activa
    imprimir_titulo("=== RETIRAR MATRÍCULA ===")
    matriculas = leer_json(RUTA_MATRICULAS)
    mostrar_matriculas_activas()

# Capturar ID matrícula a retirar
    try:
        id_matricula = int(input("\nIngresar ID matrícula: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    matricula = buscar_matricula(matriculas,id_matricula)
    if matricula is None:
        print("Matrícula no encontrada.")
        return
    if matricula["estado"] != "Activa":
        print("Solo pueden retirarse ""matrículas activas.")
        return
    print("""

=== MOTIVOS DE RETIRO ===

1. Problemas económicos
2. Cambio de institución
3. Motivos personales
4. Bajo rendimiento
5. Salud
6. Otro

""")
    opcion = input("Seleccionar motivo: ")
    motivos = {
        "1": "Problemas económicos",
        "2": "Cambio de institución",
        "3": "Motivos personales",
        "4": "Bajo rendimiento",
        "5": "Salud",
        "6": "Otro"}
    if opcion not in motivos:
        print("Opción inválida.")
        return
    descripcion = input("Descripción adicional: ") 

# Actualiza el estado y motivo del retiro
    matricula["estado"] = "Retirada" 
    matricula["motivo_retiro"] = (motivos[opcion])
    matricula["descripcion_retiro"] = (descripcion)
    guardar_json(RUTA_MATRICULAS,matriculas)
    imprimir_titulo("=== MATRÍCULA RETIRADA ===")
    print(f"ID: "
        f"{matricula['id_matricula']}")
    print(f"Alumno: "
        f"{matricula['nombre_alumno']}")
    print( f"Estado: "
        f"{matricula['estado']}")
    print(f"Motivo: "
        f"{matricula['motivo_retiro']}")

def buscar_retiro_por_id(): # Busca y muestra una matrícula por ID
    imprimir_titulo("=== BUSCAR MATRÍCULA ===")
    matriculas = leer_json(RUTA_MATRICULAS)

# Capturar ID matrícula a buscar
    try:
        id_matricula = int(input("Ingresar ID matrícula: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    matricula = buscar_matricula(matriculas,id_matricula)
    if matricula is None:
        print("Matrícula no encontrada.")
        return
    imprimir_titulo("=== DATOS MATRÍCULA ===")
    for clave, valor in matricula.items(): # Muestra toda la información de la matrícula
        print(f"{clave}: {valor}")

def reactivar_matricula(): # Reactiva una matrícula retirada
    imprimir_titulo("=== REACTIVAR MATRÍCULA ===")
    matriculas = leer_json(RUTA_MATRICULAS)

# Capturar ID matrícula a reactivar
    try:
        id_matricula = int(input("Ingresar ID matrícula: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    matricula = buscar_matricula(matriculas,id_matricula)
    if matricula is None:
        print("Matrícula no encontrada.")
        return
    if matricula["estado"] != "Retirada":
        print("La matrícula no está retirada.")
        return
    matricula["estado"] = "Activa" # Cambia el estado nuevamente a activa
    guardar_json(RUTA_MATRICULAS,matriculas)
    print("=== MATRÍCULA REACTIVADA CORRECTAMENTE ===")

def menu_retirar_matricula(): # Muestra y gestiona el menú de retiro de matrículas
    while True:
        imprimir_titulo("=== MENU RETIRO MATRÍCULA ===")
        print("1. Retirar matrícula")
        print("2. Mostrar activas")
        print("3. Historial retiros")
        print("4. Buscar matrícula")
        print("5. Reactivar matrícula")
        print("6. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":retirar_matricula()
            case "2":mostrar_matriculas_activas()
            case "3":mostrar_historial_retiros()
            case "4":buscar_retiro_por_id()
            case "5":reactivar_matricula()
            case "6":
                print("Regresando a matrículas...")
                break
            case _:
                print("Opción inválida.")