from basedatos_json import leer_json,guardar_json,generar_id
from secretaria.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_MATRICULAS = "datos/matriculas.json"

def mostrar_alumnos(alumnos):
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

def buscar_alumno(alumnos,id_alumno):
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None

def buscar_matricula(matriculas,id_matricula):
    for matricula in matriculas:
        if (matricula["id_matricula"] == id_matricula):
            return matricula
    return None

def verificar_matricula_activa(matriculas,id_alumno):
    for matricula in matriculas:
        if (matricula["id_alumno"] == id_alumno and matricula["estado"] == "Activa"):
            return matricula
    return None

def seleccionar_carrera():
    print("""

=== CARRERAS DISPONIBLES ===

1. Ingeniería de Sistemas
2. Administración
3. Contabilidad
4. Enfermería
5. Arquitectura

""")
    opcion = input("Seleccionar carrera: ")
    carreras = {
        "1": "Ingeniería de Sistemas",
        "2": "Administración",
        "3": "Contabilidad",
        "4": "Enfermería",
        "5": "Arquitectura"
    }
    return carreras.get(opcion)

def seleccionar_turno():
    print("""

=== TURNOS DISPONIBLES ===

1. Mañana
2. Tarde
3. Noche

""")

    opcion = input(
        "Seleccionar turno: "
    )
    turnos = {
        "1": "Mañana",
        "2": "Tarde",
        "3": "Noche"
    }
    return turnos.get(opcion)

def seleccionar_salon():
    print("""

=== SALONES DISPONIBLES ===

1. A101
2. B202
3. C303
4. D404

""")
    opcion = input(
        "Seleccionar salón: "
    )
    salones = {
        "1": "A101",
        "2": "B202",
        "3": "C303",
        "4": "D404"
    }
    return salones.get(opcion)

def mostrar_matriculas():
    imprimir_titulo("=== LISTA MATRÍCULAS ===")
    matriculas = leer_json(RUTA_MATRICULAS)
    if len(matriculas) == 0:
        print("No existen matrículas.")
        return
    for matricula in matriculas:
        print(f"ID: "
            f"{matricula['id_matricula']} | "
            f"Alumno: "
            f"{matricula['nombre_alumno']} | "
            f"Carrera: "
            f"{matricula['carrera']} | "
            f"Estado: "
            f"{matricula['estado']}")

def mostrar_matriculas_activas():
    imprimir_titulo("=== MATRÍCULAS ACTIVAS ===")
    matriculas = leer_json(RUTA_MATRICULAS)
    encontrados = 0
    for matricula in matriculas:
        if matricula["estado"] == "Activa":
            print(f"{matricula['id_matricula']} | "
                f"{matricula['nombre_alumno']} | "
                f"{matricula['carrera']}")
            encontrados += 1
    if encontrados == 0:
        print("No existen matrículas activas.")

def registrar_matricula():
    imprimir_titulo("=== REGISTRAR MATRÍCULA ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    matriculas = leer_json(RUTA_MATRICULAS)
    if len(alumnos) == 0:
        print("No existen alumnos.")
        return
    mostrar_alumnos(alumnos)

#Controlando errores de entrada para ID alumno
    try:
        id_alumno = int(input("\nIngresar ID alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_alumno(alumnos,id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return

    matricula_existente = (verificar_matricula_activa(matriculas,id_alumno))

    if matricula_existente:
        print("El alumno ya tiene ""una matrícula activa.")
        return
    carrera = seleccionar_carrera()
    if carrera is None:
        print("Carrera inválida.")
        return
    turno = seleccionar_turno()
    if turno is None:
        print("Turno inválido.")
        return
    salon = seleccionar_salon()
    if salon is None:
        print("Salón inválido.")
        return
    periodo = input("Ingresar periodo académico: ")
    ciclo = input("Ingresar ciclo: ")

    nueva_matricula = {
        "id_matricula":generar_id(matriculas,"id_matricula"),
        "id_alumno":alumno["id_alumno"],
        "nombre_alumno":f"{alumno['nombres']} "f"{alumno['apellidos']}",
        "dni":alumno["dni"],
        "carrera":carrera,
        "salon":salon,
        "turno":turno,
        "periodo":periodo,
        "ciclo":ciclo,
        "estado":"Activa"
    }
    matriculas.append(nueva_matricula)
    guardar_json(RUTA_MATRICULAS,matriculas)
    imprimir_titulo("=== MATRÍCULA REGISTRADA ===")
    print(f"ID: "f"{nueva_matricula['id_matricula']}")
    print(f"Alumno: "f"{nueva_matricula['nombre_alumno']}")
    print(f"Carrera: "f"{nueva_matricula['carrera']}")
    print(f"Estado: "f"{nueva_matricula['estado']}")

def buscar_matricula_por_id():
    imprimir_titulo("=== BUSCAR MATRÍCULA ===")
    matriculas = leer_json(RUTA_MATRICULAS)

# Validar que el ID ingresado sea un número entero
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
    for clave, valor in matricula.items():
        print(f"{clave}: {valor}")

def actualizar_estado_matricula():
    imprimir_titulo("=== ACTUALIZAR ESTADO ===")
    matriculas = leer_json(RUTA_MATRICULAS)

# Validar que el ID ingresado sea un número entero
    try:
        id_matricula = int(input("Ingresar ID matrícula: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    matricula = buscar_matricula(matriculas,id_matricula)
    if matricula is None:
        print("Matrícula no encontrada.")
        return
    print("""

1. Activa
2. Retirada
3. Finalizada

""")
    opcion = input("Seleccionar estado: ")
    estados = {
        "1": "Activa",
        "2": "Retirada",
        "3": "Finalizada"
    }
    if opcion not in estados:
        print("Opción inválida.")
        return
    matricula["estado"] = estados[opcion]
    guardar_json(RUTA_MATRICULAS,matriculas)
    print("Estado actualizado correctamente.")

def menu_registrar_matricula():
    while True:
        imprimir_titulo("=== MENU MATRÍCULAS ===")
        print("1. Registrar matrícula")
        print("2. Mostrar matrículas")
        print("3. Mostrar matrículas activas")
        print("4. Buscar matrícula")
        print("5. Actualizar estado")
        print("6. Volver")
        opcion = input(
            "\nSeleccionar una opción: "
        )
        match opcion:
            case "1":registrar_matricula()
            case "2":mostrar_matriculas()
            case "3":mostrar_matriculas_activas()
            case "4":buscar_matricula_por_id()
            case "5":actualizar_estado_matricula()
            case "6":
                print("Regresando a matrículas...")
                break
            case _:
                print("Opción inválida.")