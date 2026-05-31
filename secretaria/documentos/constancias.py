from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: constancias.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CONSTANCIAS = "datos/constancias.json"

def obtener_asignacion(id_alumno, asignaciones): # Busca la asignación activa de un alumno
    for asignacion in asignaciones:
        if (asignacion["id_alumno"] == id_alumno and asignacion["estado"] == "Activo"):
            return asignacion
    return None

def buscar_alumno(alumnos, id_alumno): # Busca un alumno activo según su ID
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None

def buscar_constancia(constancias, id_constancia): # Busca una constancia según su ID
    for constancia in constancias:
        if constancia["id_constancia"] == id_constancia:
            return constancia
    return None

def mostrar_alumnos(alumnos): # Muestra la lista de alumnos activos
    imprimir_titulo("=== ALUMNOS DISPONIBLES ===")
    encontrados = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            print(f"ID: {alumno['id_alumno']} | "
                f"{alumno['nombres']} "
                f"{alumno['apellidos']} | "
                f"DNI: {alumno['dni']}")
            encontrados += 1
    if encontrados == 0:
        print("No hay alumnos activos.")

def mostrar_constancias(): # Muestra las constancias registradas
    imprimir_titulo("=== LISTA DE CONSTANCIAS ===")
    constancias = leer_json(RUTA_CONSTANCIAS)
    if len(constancias) == 0:
        print("No existen constancias registradas.")
        return
    for constancia in constancias:
        print(f"ID: {constancia['id_constancia']} | "
            f"Alumno: {constancia['nombre_alumno']} | "
            f"Tipo: {constancia['tipo_constancia']} | "
            f"Estado: {constancia['estado']}")

def generar_constancia(): # Genera una nueva constancia para un alumno
    imprimir_titulo("=== GENERAR CONSTANCIA ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    constancias = leer_json(RUTA_CONSTANCIAS)
    if len(alumnos) == 0:
        print("No hay alumnos registrados.")
        return
    mostrar_alumnos(alumnos)

#Controlando errores al ingresar ID de alumno
    try:
        id_alumno = int(input("\nIngresar ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    asignacion = obtener_asignacion(id_alumno,asignaciones)
    if asignacion is None:
        print("El alumno no tiene asignación activa.")
        return
    print("""

=== TIPOS DE CONSTANCIA ===

1. Estudios
2. Matrícula
3. Conducta
4. Egreso

""")
    opcion = input("Seleccionar opción: ")
    tipos = {
        "1": "Constancia de Estudios",
        "2": "Constancia de Matrícula",
        "3": "Constancia de Conducta",
        "4": "Constancia de Egreso"
    }
    if opcion not in tipos:
        print("Opción inválida.")
        return
    nueva_constancia = { # Crea el registro de la nueva constancia
        "id_constancia":generar_id(constancias,"id_constancia"),
        "id_alumno":alumno["id_alumno"],
        "nombre_alumno":alumno["nombres"]+ " "+ alumno["apellidos"],
        "dni":alumno["dni"],
        "tipo_constancia":tipos[opcion],
        "carrera":asignacion["nombre_carrera"],
        "salon":asignacion["nombre_salon"],
        "turno":asignacion["turno"],
        "estado":"Emitida"
    }
    constancias.append(nueva_constancia) # Agrega y guarda la constancia generada
    guardar_json(RUTA_CONSTANCIAS,constancias)
    imprimir_titulo("=== CONSTANCIA GENERADA ===")
    print(f"ID: "f"{nueva_constancia['id_constancia']}")
    print(f"Alumno: "f"{nueva_constancia['nombre_alumno']}")
    print(f"Tipo: "f"{nueva_constancia['tipo_constancia']}")

def buscar_constancia_por_id(): # Busca una constancia mediante su ID
    imprimir_titulo("=== BUSCAR CONSTANCIA ===")
    constancias = leer_json(RUTA_CONSTANCIAS)

#Controlando errores al ingresar ID de constancia
    try:
        id_constancia = int(input("Ingresar ID: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    constancia = buscar_constancia(constancias,id_constancia)
    if constancia is None:
        print("Constancia no encontrada.")
        return
    imprimir_titulo("=== DATOS DE CONSTANCIA ===")
    for clave, valor in constancia.items(): #Muestra todos los datos de la constancia
        print(f"{clave}: {valor}")

def anular_constancia(): # Cambia el estado de una constancia a anulada
    imprimir_titulo("=== ANULAR CONSTANCIA ===")
    constancias = leer_json(RUTA_CONSTANCIAS)

#Controlando errores al ingresar ID de constancia
    try:
        id_constancia = int(input("Ingresar ID: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    constancia = buscar_constancia(constancias,id_constancia)
    if constancia is None:
        print("Constancia no encontrada.")
        return
    constancia["estado"] = "Anulada"
    guardar_json(RUTA_CONSTANCIAS,constancias)
    print("=== CONSTANCIA ANULADA CORRECTAMENTE ===")

def menu_constancias(): # Muestra y gestiona el menú de constancias
    while True:
        imprimir_titulo("=== MENU CONSTANCIAS ===")
        print("1. Generar constancia")
        print("2. Mostrar constancias")
        print("3. Buscar constancia")
        print("4. Anular constancia")
        print("5. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":
                generar_constancia()
            case "2":
                mostrar_constancias()
            case "3":
                buscar_constancia_por_id()
            case "4":
                anular_constancia()
            case "5":
                print("Regresando al menú de documentos...")
                break
            case _:
                print("Opción inválida.")