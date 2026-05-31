from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"

def buscar_por_id(lista, campo_id, valor_id):  #Busca un registro activo utilizando su identificador
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):  #Muestra las plantillas académicas disponibles para seleccionar
    imprimir_titulo("=== PLANTILLAS DISPONIBLES ===")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")

def mostrar_carreras(carreras, id_carrera):  #Muestra la carrera asociada a la plantilla elegida
    imprimir_titulo("=== CARRERA DE LA PLANTILLA ===")
    for carrera in carreras:
        if carrera["estado"] == "Activo" and carrera["id_carrera"] == id_carrera:
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):  #Valida que no exista un cargo repetido
    for cargo in cargos:
        if (
            cargo["estado"] == "Activo"
            and cargo["id_plantilla"] == id_plantilla
            and cargo["id_carrera"] == id_carrera
            and cargo["nombre_cargo"].lower() == nombre_cargo.lower()):
            return True
    return False

def pedir_frecuencia():  #Permite seleccionar la frecuencia de cobro del cargo
    while True:
        print("""
=== TIPOS DE FRECUENCIA ===

1. Único
2. Mensual
3. Por unidad
4. Por módulo
""")
        opcion = input("Seleccione frecuencia: ")
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

def crear_cargo_oficial():  #Registra un cargo oficial que será utilizado en los pagos de alumnos
    imprimir_titulo("=== CREAR CARGO OFICIAL ===")
    plantillas = leer_json(RUTA_PLANTILLAS)
    carreras = leer_json(RUTA_CARRERAS)
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        return
    mostrar_plantillas(plantillas)

#Controlando errores al ingresar ID de plantilla
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return
    mostrar_carreras(carreras, plantilla["id_carrera"])

#Controlando errores al ingresar ID de carrera
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    if id_carrera != plantilla["id_carrera"]:
        print("La carrera no pertenece a la plantilla seleccionada.")
        return
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        return
    nombre_cargo = input("Nombre del cargo: ")
    if cargo_ya_existe(cargos, id_plantilla, id_carrera, nombre_cargo):
        print("Este cargo oficial ya existe para esta plantilla y carrera.")
        return

#Controlando errores al ingresar monto del cargo
    try:
        monto = float(input("Monto del cargo: S/ "))
    except ValueError:
        print("Debe ingresar un monto válido.")
        return
    frecuencia = pedir_frecuencia()
    fecha_limite = input("Fecha límite o regla (ejemplo: Día 10 de cada mes): ")
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
    cargos.append(nuevo_cargo)  # Agrega el nuevo cargo a la lista de cargos oficiales
    guardar_json(RUTA_CARGOS_OFICIALES, cargos)  # Guarda el cargo oficial en el archivo json
    print("\nCargo oficial creado correctamente.")

def ver_cargos_oficiales():  # Muestra todos los cargos oficiales registrados en el sistema
    imprimir_titulo("=== CARGOS OFICIALES ===")
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
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

def modificar_cargo_oficial():  # Permite editar datos de un cargo oficial existente
    imprimir_titulo("=== MODIFICAR CARGO OFICIAL ===")
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    if len(cargos) == 0:
        print("No hay cargos oficiales creados.")
        return
    ver_cargos_oficiales()

#Controlando errores al ingresar ID de cargo oficial
    try:
        id_cargo = int(input("\nIngrese ID del cargo que desea modificar: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
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
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            cargo["nombre_cargo"] = input("Nuevo nombre del cargo: ")
        elif opcion == "2":

#Controlando errores al ingresar nuevo monto del cargo
            try:
                cargo["monto"] = float(input("Nuevo monto: S/ "))
            except ValueError:
                print("Monto inválido.")
                continue
        elif opcion == "3":
            cargo["frecuencia"] = pedir_frecuencia()
        elif opcion == "4":
            cargo["fecha_limite"] = input("Nueva fecha límite o regla: ")
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
        guardar_json(RUTA_CARGOS_OFICIALES, cargos)  # Guarda inmediatamente los cambios realizados
        print("\n=== CARGO ACTUALIZADO CORRECTAMENTE ===")
        continuar = input("¿Desea modificar otro dato del mismo cargo? (si/no): ").lower()
        if continuar != "si":
            break