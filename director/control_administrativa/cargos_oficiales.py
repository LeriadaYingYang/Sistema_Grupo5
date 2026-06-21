from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"


# --- FUNCIONES DE VALIDACIÓN  ---

def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: No se permiten números negativos.")
            else:
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras).")


def pedir_monto(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: El monto no puede ser negativo.")
            else:
                return round(valor, 2)
        except ValueError:
            print("Error: Debe ingresar un monto numérico válido.")


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: El campo no puede quedar vacío.")
        else:
            return texto


def pedir_dia_limite(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            dia = int(entrada)
            if dia < 1 or dia > 31:
                print("Error: Ingrese un día válido del mes (1-31).")
            else:
                return str(dia)
        except ValueError:
            print("Error: Carácter no válido.")


# --- LÓGICA DE BÚSQUEDA Y VISUALIZACIÓN ---

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item.get(campo_id) == valor_id and item.get("estado") == "Activo":
            return item
    return None


def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for plantilla in plantillas:
        if plantilla.get("estado") == "Activo":
            print(
                f"ID: {plantilla.get('id_plantilla')} | Carrera: {plantilla.get('nombre_carrera')} | Plantilla: {plantilla.get('nombre_plantilla')}")


def mostrar_carreras(carreras, id_carrera):
    imprimir_titulo("CARRERA DE LA PLANTILLA")
    for carrera in carreras:
        if carrera.get("estado") == "Activo" and carrera.get("id_carrera") == id_carrera:
            print(f"ID: {carrera.get('id_carrera')} | {carrera.get('nombre')}")


def cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):
    for cargo in cargos:
        if (cargo.get("estado") == "Activo"
                and cargo.get("id_plantilla") == id_plantilla
                and cargo.get("id_carrera") == id_carrera
                and cargo.get("nombre_cargo", "").lower() == nombre_cargo.lower()):
            return True
    return False


def pedir_frecuencia():
    while True:
        print("\n--- TIPOS DE FRECUENCIA ---")
        print("1. Único")
        print("2. Mensual")
        print("3. Por unidad")
        print("4. Por módulo")

        opcion = input("\nSeleccione frecuencia: ").strip()

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


# --- LÓGICA PRINCIPAL DEL MÓDULO ---

def crear_cargo_oficial():
    imprimir_titulo("CREAR CARGO OFICIAL")

    plantillas = leer_json(RUTA_PLANTILLAS) or []
    carreras = leer_json(RUTA_CARRERAS) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []

    if not plantillas:
        print("Primero debe crear plantillas académicas.")
        return

    mostrar_plantillas(plantillas)
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if not plantilla:
        print("Plantilla no encontrada o inactiva.")
        return

    mostrar_carreras(carreras, plantilla.get("id_carrera"))
    id_carrera = pedir_entero("\nIngrese ID de carrera: ")

    if id_carrera != plantilla.get("id_carrera"):
        print("La carrera no pertenece a la plantilla seleccionada.")
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if not carrera:
        print("Carrera no encontrada o inactiva.")
        return

    nombre_cargo = pedir_texto("Nombre del cargo: ")
    if cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):
        print("Este cargo oficial ya existe para esta plantilla y carrera.")
        return

    monto = pedir_monto("Monto del cargo: S/ ")
    frecuencia = pedir_frecuencia()
    fecha_limite = pedir_dia_limite("Día límite de pago cada mes (ejemplo: 10): ")

    nuevo_cargo = {
        "id_cargo_oficial": generar_id(cargos, "id_cargo_oficial"),
        "id_plantilla": plantilla.get("id_plantilla"),
        "nombre_plantilla": plantilla.get("nombre_plantilla"),
        "id_carrera": carrera.get("id_carrera"),
        "nombre_carrera": carrera.get("nombre"),
        "nombre_cargo": nombre_cargo,
        "monto": monto,
        "frecuencia": frecuencia,
        "fecha_limite": fecha_limite,
        "estado": "Activo"
    }

    cargos.append(nuevo_cargo)
    guardar_json(RUTA_CARGOS_OFICIALES, cargos)
    print("\nCargo oficial creado correctamente.")


def ver_cargos_oficiales():
    imprimir_titulo("CARGOS OFICIALES")
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []

    if not cargos:
        print("No hay cargos oficiales creados.")
        return False

    for cargo in cargos:
        print("\n-----------------------------")
        print(f"ID: {cargo.get('id_cargo_oficial', 'N/A')}")
        print(f"Plantilla: {cargo.get('nombre_plantilla', 'Desconocida')}")
        print(f"Carrera: {cargo.get('nombre_carrera', 'Desconocida')}")
        print(f"Cargo: {cargo.get('nombre_cargo', 'Desconocido')} | Estado: {cargo.get('estado', 'N/A')}")
        print(f"Monto: S/ {cargo.get('monto', 0.0)} | Frecuencia: {cargo.get('frecuencia', 'N/A')}")
        print(f"Día límite: {cargo.get('fecha_limite', 'N/A')}")

    return True


def modificar_cargo_oficial():
    imprimir_titulo("MODIFICAR CARGO OFICIAL")
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []

    if not ver_cargos_oficiales():
        return

    id_cargo = pedir_entero("\nIngrese ID del cargo que desea modificar: ")

    cargo = next((item for item in cargos if item.get("id_cargo_oficial") == id_cargo), None)

    if not cargo:
        print("Cargo no encontrado.")
        return

    while True:
        print(
            f"\nCargo seleccionado: {cargo.get('nombre_cargo')} | S/ {cargo.get('monto')} | {cargo.get('frecuencia')}")
        print("¿Qué desea modificar?")
        print("1. Cambiar nombre")
        print("2. Cambiar monto")
        print("3. Cambiar frecuencia")
        print("4. Cambiar día límite")
        print("5. Activar / desactivar cargo")
        print("6. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            cargo["nombre_cargo"] = pedir_texto("Nuevo nombre del cargo: ")
        elif opcion == "2":
            cargo["monto"] = pedir_monto("Nuevo monto: S/ ")
        elif opcion == "3":
            cargo["frecuencia"] = pedir_frecuencia()
        elif opcion == "4":
            cargo["fecha_limite"] = pedir_dia_limite("Nuevo día límite: ")
        elif opcion == "5":
            cargo["estado"] = "Inactivo" if cargo.get("estado") == "Activo" else "Activo"
            print(f"Nuevo estado: {cargo['estado']}")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
            continue

        guardar_json(RUTA_CARGOS_OFICIALES, cargos)
        print("\nCargo actualizado correctamente.")

        continuar = pedir_texto("¿Desea modificar otro dato del mismo cargo? (si/no): ").lower()
        if continuar != "si":
            break