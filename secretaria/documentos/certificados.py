from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CERTIFICADOS = "datos/certificados.json"

def obtener_asignacion(id_alumno, asignaciones):
    for asignacion in asignaciones:
        if (asignacion["id_alumno"] == id_alumno and asignacion["estado"] == "Activo"):
            return asignacion
    return None

def buscar_alumno(alumnos, id_alumno):
    for alumno in alumnos:
        if (alumno["id_alumno"] == id_alumno and alumno["estado"] == "Activo"):
            return alumno
    return None

def buscar_certificado(certificados, id_certificado):
    for certificado in certificados:
        if certificado["id_certificado"] == id_certificado:
            return certificado
    return None

def mostrar_alumnos(alumnos):
    imprimir_titulo("=== ALUMNOS DISPONIBLES ===")
    encontrados = 0
    for alumno in alumnos:
        if alumno["estado"] == "Activo":
            print(
                f"ID: {alumno['id_alumno']} | "
                f"{alumno['nombres']} {alumno['apellidos']} | "
                f"DNI: {alumno['dni']}")
            encontrados += 1
    if encontrados == 0:
        print("No hay alumnos activos.")

def mostrar_certificados():
    imprimir_titulo("=== LISTA DE CERTIFICADOS ===")
    certificados = leer_json(RUTA_CERTIFICADOS)
    if len(certificados) == 0:
        print("No existen certificados registrados.")
        return
    for certificado in certificados:
        print(
            f"ID: {certificado['id_certificado']} | "
            f"Alumno: {certificado['nombre_alumno']} | "
            f"Tipo: {certificado['tipo_certificado']} | "
            f"Estado: {certificado['estado']}")

def generar_certificado():
    imprimir_titulo("=== GENERAR CERTIFICADO ===")
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    certificados = leer_json(RUTA_CERTIFICADOS)
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
    alumno = buscar_alumno(alumnos, id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        return
    asignacion = obtener_asignacion(id_alumno,asignaciones)
    if asignacion is None:
        print("El alumno no tiene asignación activa.")
        return
    tipo = input("Tipo de certificado (Estudios/Matricula/Conducta): ")
    nuevo_certificado = {"id_certificado": generar_id(certificados,"id_certificado"),
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno":alumno["nombres"]+ " "+ alumno["apellidos"],
        "dni": alumno["dni"],
        "tipo_certificado": tipo,
        "carrera":asignacion["nombre_carrera"],
        "salon":asignacion["nombre_salon"],
        "estado": "Emitido"}

    certificados.append(nuevo_certificado)
    guardar_json(RUTA_CERTIFICADOS,certificados)
    imprimir_titulo("=== CERTIFICADO GENERADO ===")
    print(f"ID Certificado: "f"{nuevo_certificado['id_certificado']}")
    print(f"Alumno: "f"{nuevo_certificado['nombre_alumno']}")
    print(f"Tipo: "f"{nuevo_certificado['tipo_certificado']}")


def buscar_certificado_por_id():
    imprimir_titulo("=== BUSCAR CERTIFICADO ===")
    certificados = leer_json(RUTA_CERTIFICADOS)

#Controlando errores al ingresar ID de certificado
    try:
        id_certificado = int(input("Ingresar ID del certificado: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    certificado = buscar_certificado(certificados,id_certificado)
    if certificado is None:
        print("Certificado no encontrado.")
        return
    imprimir_titulo("=== DATOS DEL CERTIFICADO ===")
    for clave, valor in certificado.items():
        print(f"{clave}: {valor}")


def anular_certificado():
    imprimir_titulo("=== ANULAR CERTIFICADO ===")
    certificados = leer_json(RUTA_CERTIFICADOS)

#Controlando errores al ingresar ID de certificado
    try:
        id_certificado = int(input("Ingresar ID del certificado: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    certificado = buscar_certificado(certificados,id_certificado)
    if certificado is None:
        print("Certificado no encontrado.")
        return
    certificado["estado"] = "Anulado"
    guardar_json(RUTA_CERTIFICADOS,certificados)
    print("Certificado anulado correctamente.")

def menu_certificados():
    while True:
        imprimir_titulo("=== MENU CERTIFICADOS ===")
        print("1. Generar certificado")
        print("2. Mostrar certificados")
        print("3. Buscar certificado")
        print("4. Anular certificado")
        print("5. Volver")
        opcion = input("\nSeleccionar una opción: ")
        match opcion:
            case "1":generar_certificado()
            case "2":mostrar_certificados()
            case "3":buscar_certificado_por_id()
            case "4":anular_certificado()
            case "5":
                print("Regresando al menú de documentos...")
                break
            case _:
                print("Opción inválida.")