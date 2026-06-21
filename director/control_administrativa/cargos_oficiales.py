import re
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"


# --- FUNCIONES DE VALIDACIÓN MEJORADAS ---

def pedir_entero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if not re.fullmatch(r"\d+", entrada):
            print("Error: ingrese solo números enteros positivos, sin letras ni símbolos.")
            continue
        valor = int(entrada)
        if valor == 0:
            print("Error: el ID debe ser mayor que 0.")
        else:
            return valor


def pedir_monto(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if not re.fullmatch(r"\d+(\.\d{1,2})?", entrada):
            print("Error: ingrese un monto válido, sin negativos, letras ni símbolos. Ejemplo: 150 o 150.50")
            continue
        valor = float(entrada)
        if valor <= 0:
            print("Error: el monto debe ser mayor que 0.")
        else:
            return round(valor, 2)


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: el campo no puede quedar vacío.")
        elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{3,60}", texto):
            print("Error: use solo letras, números y espacios. Mínimo 3 caracteres, sin símbolos.")
        else:
            return texto


def pedir_dia_limite(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if not re.fullmatch(r"\d+", entrada):
            print("Error: ingrese solo números para el día límite, sin letras ni símbolos.")
            continue
        dia = int(entrada)
        if dia < 1 or dia > 31:
            print("Error: el día límite debe estar entre 1 y 31.")
        else:
            return str(dia)


# -----------------------------------------

def buscar_por_id(lista, campo_id, valor_id):  # busca un registro activo utilizando su identificador
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None


def mostrar_plantillas(plantillas):  # muestra las plantillas académicas disponibles para seleccionar
    imprimir_titulo("PLANTILLAS DISPONIBLES")

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")


def mostrar_carreras(carreras, id_carrera):  # muestra la carrera asociada a la plantilla elegida
    imprimir_titulo("CARRERA DE LA PLANTILLA")
    for carrera in carreras:
        if carrera["estado"] == "Activo" and carrera["id_carrera"] == id_carrera:
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")


def cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):  # valida que no exista un cargo repetido
    for cargo in cargos:
        if (
                cargo["estado"] == "Activo"
                and cargo["id_plantilla"] == id_plantilla
                and cargo["id_carrera"] == id_carrera
                and cargo["nombre_cargo"].lower() == nombre_cargo.lower()):
            return True
    return False


def pedir_frecuencia():  # permite seleccionar la frecuencia de cobro del cargo
    while True:
        print("""
--- TIPOS DE FRECUENCIA ---

1. Único
2. Mensual
3. Por unidad
4. Por módulo
""")

        opcion = input("Seleccione frecuencia: ").strip()

        if opcion == "1":
            return "Único"
        elif opcion == "2":
            return "Mensual"
        elif opcion == "3":
            return "Por unidad"
        elif opcion == "4":
            return "Por módulo"
        else:
            print("Opción inválida.")


def crear_cargo_oficial():  # registra un cargo oficial que será utilizado en los pagos de alumnos
    imprimir_titulo("CREAR CARGO OFICIAL")

    # Se agrega "or []" como validación de persistencia por si el JSON está vacío o no existe
    plantillas = leer_json(RUTA_PLANTILLAS) or []
    carreras = leer_json(RUTA_CARRERAS) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []

    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        return

    mostrar_plantillas(plantillas)

    # Usando validación
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return

    mostrar_carreras(carreras, plantilla["id_carrera"])

    # Usando validación
    id_carrera = pedir_entero("\nIngrese ID de carrera: ")

    if id_carrera != plantilla["id_carrera"]:
        print("La carrera no pertenece a la plantilla seleccionada.")
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        return

    # Usando validación
    nombre_cargo = pedir_texto("Nombre del cargo: ")
    if cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):
        print("Este cargo oficial ya existe para esta plantilla y carrera.")
        return

    # Usando validación
    monto = pedir_monto("Monto del cargo: S/ ")
    frecuencia = pedir_frecuencia()

    # Usando la nueva validación exclusiva para el límite de días (0-31)
    fecha_limite = pedir_dia_limite("Fecha límite o regla (ejemplo: Día 10 de cada mes): ")

    nuevo_cargo = {
        "id_cargo_oficial": generar_id(cargos, "id_cargo_oficial"),
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "nombre_cargo": nombre_cargo,
        "monto": monto,
        "frecuencia": frecuencia,
        "fecha_limite": fecha_limite,
        "estado": "Activo"}

    cargos.append(nuevo_cargo)  # agrega el nuevo cargo a la lista de cargos oficiales
    guardar_json(RUTA_CARGOS_OFICIALES, cargos)  # guarda el cargo oficial en el archivo json
    print("\nCargo oficial creado correctamente.")


def ver_cargos_oficiales():  # muestra todos los cargos oficiales registrados en el sistema
    imprimir_titulo("CARGOS OFICIALES")
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    if len(cargos) == 0:
        print("No hay cargos oficiales creados.")
        return
    for cargo in cargos:
        print("\n-----------------------------")
        print(f"ID: {cargo['id_cargo_oficial']}")
        print(f"Plantilla: {cargo['nombre_plantilla']}")
        print(f"Carrera: {cargo['nombre_carrera']}")
        print(f"Cargo: {cargo['nombre_cargo']}")
        print(f"Monto: S/ {cargo['monto']}")
        print(f"Frecuencia: {cargo['frecuencia']}")
        print(f"Fecha límite: {cargo['fecha_limite']}")
        print(f"Estado: {cargo['estado']}")


def modificar_cargo_oficial():  # permite editar datos de un cargo oficial existente
    imprimir_titulo("MODIFICAR CARGO OFICIAL")
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    if len(cargos) == 0:
        print("No hay cargos oficiales creados.")
        return

    ver_cargos_oficiales()

    # Usando validación
    id_cargo = pedir_entero("\nIngrese ID del cargo que desea modificar: ")

    cargo = None
    for item in cargos:
        if item["id_cargo_oficial"] == id_cargo:
            cargo = item
            break

    if cargo is None:
        print("Cargo no encontrado.")
        return

    while True:
        print(f"""
Cargo seleccionado:
{cargo['nombre_cargo']} | S/ {cargo['monto']} | {cargo['frecuencia']}

¿Qué desea modificar?

1. Cambiar nombre
2. Cambiar monto
3. Cambiar frecuencia
4. Cambiar fecha límite
5. Activar / desactivar cargo
6. Volver
""")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            cargo["nombre_cargo"] = pedir_texto("Nuevo nombre del cargo: ")
        elif opcion == "2":
            cargo["monto"] = pedir_monto("Nuevo monto: S/ ")
        elif opcion == "3":
            cargo["frecuencia"] = pedir_frecuencia()
        elif opcion == "4":
            # validación de fechas (0-31)
            cargo["fecha_limite"] = pedir_dia_limite("Nueva fecha límite o regla: ")
        elif opcion == "5":
            if cargo["estado"] == "Activo":
                cargo["estado"] = "Inactivo"
            else:
                cargo["estado"] = "Activo"
            print(f"Nuevo estado: {cargo['estado']}")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
            continue

        guardar_json(RUTA_CARGOS_OFICIALES, cargos)  # guarda inmediatamente los cambios realizados
        print("\nCargo actualizado correctamente.")

        continuar = pedir_texto("¿Desea modificar otro dato del mismo cargo? (si/no): ").lower()
        if continuar != "si":
            break
