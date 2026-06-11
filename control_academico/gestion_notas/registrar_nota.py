from basedatos_json import leer_json,guardar_json,generar_id
from control_academico.utilidades import imprimir_titulo

RUTA_MODULOS = "datos/modulos.json"
RUTA_MATRICULAS = "datos/matriculas.json"
RUTA_NOTAS = "datos/notas_alumnos.json"

def cargar_datos():
    return (leer_json(RUTA_MODULOS),leer_json(RUTA_MATRICULAS),leer_json(RUTA_NOTAS))

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def pedir_decimal(mensaje):
    while True:
        try:
            nota = float(input(mensaje))
            if 0 <= nota <= 20:
                return nota
            print("La nota debe estar entre 0 y 20.")
        except ValueError:
            print("Ingrese una nota válida.")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El campo no puede estar vacío.")

def buscar_por_id(lista, campo_id, valor_id):
    return next(
        (item for item in lista
            if item[campo_id] == valor_id and item["estado"] in ["Activo", "Activa"]),None)

def mostrar_modulos(modulos):
    imprimir_titulo("=== MÓDULOS DISPONIBLES ===")
    modulos_activos = [modulo for modulo in modulos
        if modulo["estado"] == "Activo"]
    if not modulos_activos:
        print("No existen módulos registrados.")
        return False
    for modulo in modulos_activos:
        print(f"ID: {modulo['id_modulo']} | "
            f"Carrera: {modulo['nombre_carrera']} | "
            f"Unidad: {modulo['nombre_unidad']} | "
            f"Módulo: {modulo['nombre_modulo']}")
    return True

def obtener_alumnos_matriculados(matriculas,nombre_carrera,nombre_salon):
    return [matricula for matricula in matriculas
        if matricula["estado"] == "Activa" and matricula["carrera"].lower()
        == nombre_carrera.lower() and matricula["salon"].lower() == nombre_salon.lower()]

def registro_existe(registros,id_alumno,id_modulo):
    return any(registro["estado"] == "Activo" and registro["id_alumno"] == id_alumno
        and registro["id_modulo"] == id_modulo for registro in registros)

def calcular_promedio(notas):
    if not notas:
        return 0
    promedio = (sum(item["nota"] for item in notas)/ len(notas))
    return round(promedio, 2)

def pedir_notas():
    notas = []
    cantidad = pedir_entero("¿Cuántas evaluaciones registrar?: ")
    while cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        cantidad = pedir_entero("¿Cuántas evaluaciones registrar?: ")
    for orden in range(1, cantidad + 1):
        print(f"\n=== NOTA {orden} ===")
        nombre_nota = pedir_texto("Nombre evaluación: ")
        nota = pedir_decimal("Calificación (0-20): ")
        notas.append(
            {"orden": orden,"nombre_nota": nombre_nota,"nota": nota})
    return notas

def crear_registro_nota(registros,alumno,modulo,notas):
    return {"id_registro_nota":
        generar_id(registros,"id_registro_nota"),
        "id_alumno":alumno["id_alumno"],
        "nombre_alumno":alumno["nombre_alumno"],
        "id_carrera":modulo["id_carrera"],
        "id_salon":modulo["id_salon"],
        "id_unidad":modulo["id_unidad"],
        "id_modulo":modulo["id_modulo"],
        "notas":notas,
        "promedio_modulo":calcular_promedio(notas),
        "estado":"Activo"}

def registrar_notas_completas():
    imprimir_titulo("=== REGISTRAR NOTAS DEL MÓDULO ===")
    (modulos,matriculas,registros) = cargar_datos()
    if not mostrar_modulos(modulos):
        return
    id_modulo = pedir_entero("\nIngrese ID módulo: ")
    modulo = buscar_por_id(modulos,"id_modulo",id_modulo)
    if modulo is None:
        print("Módulo no encontrado.")
        return
    alumnos = (obtener_alumnos_matriculados(matriculas,modulo["nombre_carrera"],modulo["nombre_salon"]))
    if not alumnos:
        print("No existen alumnos matriculados.")
        return
    registros_creados = 0
    for alumno in alumnos:
        if registro_existe(registros,alumno["id_alumno"],modulo["id_modulo"]):
            continue
        imprimir_titulo(f"ALUMNO: "
            f"{alumno['nombre_alumno']}")
        notas = pedir_notas()
        nuevo_registro = (crear_registro_nota(registros,alumno,modulo,notas))
        registros.append(nuevo_registro)
        registros_creados += 1
    guardar_json(RUTA_NOTAS,registros)
    print(f"\nRegistros creados: "
        f"{registros_creados}")

def agregar_nota_existente():
    imprimir_titulo("=== AGREGAR NOTA EXISTENTE ===")
    registros = leer_json(RUTA_NOTAS)
    if not registros:
        print("No existen registros.")
        return
    id_registro = pedir_entero("Ingrese ID registro: ")
    registro = buscar_por_id(registros,"id_registro_nota",id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    nombre_nota = pedir_texto("Nombre evaluación: ")
    nota = pedir_decimal("Calificación (0-20): ")
    nuevo_orden = (len(registro["notas"]) + 1)
    registro["notas"].append(
        {"orden": nuevo_orden,"nombre_nota": nombre_nota,"nota": nota})
    registro["promedio_modulo"] = (calcular_promedio(
            registro["notas"]))
    guardar_json(RUTA_NOTAS,registros)
    print("\nNota agregada correctamente.")

def registrar_notas():
    while True:
        imprimir_titulo("=== REGISTRAR NOTAS ===")
        print("1. Registrar todas las notas de un módulo")
        print("2. Agregar nota a un registro existente")
        print("3. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":registrar_notas_completas()
        elif opcion == "2":agregar_nota_existente()
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")