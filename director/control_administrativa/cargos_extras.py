import re
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"

# ====================================================================
# FUNCIONES DE VALIDACIÓN MEJORADAS
# ====================================================================

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
            print("Error: ingrese un monto válido, sin negativos, letras ni símbolos. Ejemplo: 50 o 50.50")
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
            print("Error: use solo letras, números y espacios. No se permiten símbolos.")
        else:
            return texto

def pedir_texto_opcional(mensaje, valor_actual):
    texto = input(mensaje).strip()
    if texto == "":
        return valor_actual
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{3,60}", texto):
        print("Error: texto inválido, se mantuvo el dato anterior.")
        return valor_actual
    return texto

# ====================================================================
# LÓGICA DEL MÓDULO
# ====================================================================

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item.get(campo_id) == valor_id and item.get("estado") == "Activo":
            return item
    return None


def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS")
    for plantilla in plantillas:
        if plantilla.get("estado") == "Activo":
            print(
                f"ID: {plantilla.get('id_plantilla')} | {plantilla.get('nombre_plantilla')} | Carrera: {plantilla.get('nombre_carrera')}")


def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES")
    for salon in salones:
        if salon.get("estado") == "Activo" and salon.get("id_carrera") == id_carrera:
            print(f"ID: {salon.get('id_salon')} | {salon.get('nombre_salon')} | Turno: {salon.get('turno')}")


def mostrar_alumnos_salon(alumnos, asignaciones, id_salon):
    imprimir_titulo("ALUMNOS DEL SALÓN")
    encontrados = 0
    for asignacion in asignaciones:
        if asignacion.get("estado") == "Activo" and asignacion.get("id_salon") == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion.get("id_alumno"))
            if alumno:
                encontrados += 1
                print(
                    f"ID: {alumno.get('id_alumno')} | {alumno.get('nombres')} {alumno.get('apellidos')} | DNI: {alumno.get('dni')}")
    if encontrados == 0:
        print("No hay alumnos asignados a este salón.")

def crear_cargo_extra():  # 1. Crear cargo extra genérico para toda la institución
    imprimir_titulo("CREAR CARGO EXTRA GENERAL")
    cargos = leer_json(RUTA_CARGOS_EXTRAS) or []

    print("Este cargo se creará de forma general (aplicable a toda la institución).")
    nombre = pedir_texto("Nombre del cargo extra: ")
    monto = pedir_monto("Monto del cargo extra: S/ ")

    nuevo = {
        "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
        "nombre": nombre,
        "monto": monto,
        "aplica_a": "General",
        "id_plantilla": None,
        "nombre_plantilla": "Todas",
        "id_carrera": None,
        "nombre_carrera": "Todas",
        "id_salon": None,
        "nombre_salon": "Todos",
        "id_alumno": None,
        "nombre_alumno": "Todos",
        "estado": "Activo"
    }
    cargos.append(nuevo)
    guardar_json(RUTA_CARGOS_EXTRAS, cargos)
    print("\nCargo extra general creado correctamente.")

def asignar_cargo_extra():  # 2. Asignar cargo extra a grupo o alumno
    while True:
        imprimir_titulo("ASIGNAR CARGO EXTRA")
        print("1. Asignar a toda una Carrera")
        print("2. Asignar a un Salón")
        print("3. Asignar a un Alumno específico")
        print("4. Cancelar / Volver")

        opcion = input("\nSeleccione a quién asignar el cargo: ").strip()

        if opcion in ["1", "2", "3"]:
            plantillas = leer_json(RUTA_PLANTILLAS) or []
            salones = leer_json(RUTA_SALONES) or []
            alumnos = leer_json(RUTA_ALUMNOS) or []
            asignaciones = leer_json(RUTA_ASIGNACIONES) or []
            cargos = leer_json(RUTA_CARGOS_EXTRAS) or []

            if not plantillas:
                print("No hay plantillas registradas en el sistema.")
                return

            mostrar_plantillas(plantillas)
            id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")
            plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

            if not plantilla:
                print("Plantilla no válida o inactiva.")
                continue

            id_salon, nombre_salon = None, None
            id_alumno, nombre_alumno = None, None
            aplica_a = "Carrera"

            if opcion in ["2", "3"]:
                mostrar_salones(salones, plantilla["id_carrera"])
                id_salon = pedir_entero("\nIngrese ID de salón: ")
                salon = buscar_por_id(salones, "id_salon", id_salon)

                if not salon or salon["id_carrera"] != plantilla["id_carrera"]:
                    print("Salón no válido.")
                    continue
                nombre_salon = salon["nombre_salon"]
                aplica_a = "Salón"

            if opcion == "3":
                mostrar_alumnos_salon(alumnos, asignaciones, id_salon)
                id_alumno = pedir_entero("\nIngrese ID del alumno: ")
                alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)

                if not alumno:
                    print("Alumno no válido.")
                    continue
                nombre_alumno = f"{alumno['nombres']} {alumno['apellidos']}"
                aplica_a = "Alumno"

            nombre_cargo = pedir_texto("Nombre del cargo extra a asignar: ")
            monto_cargo = pedir_monto("Monto del cargo extra: S/ ")

            nuevo = {
                "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
                "nombre": nombre_cargo,
                "monto": monto_cargo,
                "aplica_a": aplica_a,
                "id_plantilla": plantilla["id_plantilla"],
                "nombre_plantilla": plantilla["nombre_plantilla"],
                "id_carrera": plantilla["id_carrera"],
                "nombre_carrera": plantilla["nombre_carrera"],
                "id_salon": id_salon,
                "nombre_salon": nombre_salon,
                "id_alumno": id_alumno,
                "nombre_alumno": nombre_alumno,
                "estado": "Activo"
            }
            cargos.append(nuevo)
            guardar_json(RUTA_CARGOS_EXTRAS, cargos)
            print(f"\nCargo extra asignado a {aplica_a} correctamente.")

        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

def ver_cargos_extras():  # 4. Ver cargos extras
    imprimir_titulo("CARGOS EXTRAS REGISTRADOS")
    cargos = leer_json(RUTA_CARGOS_EXTRAS) or []

    if len(cargos) == 0:
        print("No hay cargos extras registrados en el sistema.")
        return False

    for cargo in cargos:
        print("\n-----------------------------")
        print(f"ID: {cargo.get('id_cargo_extra')} | Cargo: {cargo.get('nombre')}")
        print(f"Monto: S/ {cargo.get('monto')} | Aplica a: {cargo.get('aplica_a')}")
        if cargo.get('aplica_a') != "General":
            print(f"Carrera: {cargo.get('nombre_carrera')}")
            if cargo.get('nombre_salon'):
                print(f"Salón: {cargo.get('nombre_salon')}")
            if cargo.get('nombre_alumno'):
                print(f"Alumno: {cargo.get('nombre_alumno')}")
        print(f"Estado: {cargo.get('estado')}")
    return True

def editar_cargo_extra():  # 3. Editar cargo extra
    imprimir_titulo("EDITAR CARGO EXTRA")
    cargos = leer_json(RUTA_CARGOS_EXTRAS) or []

    if not ver_cargos_extras():
        return

    id_cargo = pedir_entero("\nIngrese ID del cargo que desea editar: ")

    cargo_encontrado = None
    for cargo in cargos:
        if cargo.get("id_cargo_extra") == id_cargo:
            cargo_encontrado = cargo
            break

    if cargo_encontrado is None:
        print("Error: Cargo no encontrado.")
        return

    print(f"\nEditando cargo: {cargo_encontrado['nombre']} | S/ {cargo_encontrado['monto']}")
    print("Deje en blanco y presione Enter si no desea cambiar un dato.")

    cargo_encontrado["nombre"] = pedir_texto_opcional("Nuevo nombre del cargo: ", cargo_encontrado["nombre"])

    nuevo_monto_str = input("Nuevo monto (S/): ").strip()
    if nuevo_monto_str:
        if not re.fullmatch(r"\d+(\.\d{1,2})?", nuevo_monto_str):
            print("Monto inválido ignorado, se mantuvo el anterior.")
        else:
            monto_val = float(nuevo_monto_str)
            if monto_val <= 0:
                print("El monto debe ser mayor que 0, se mantuvo el anterior.")
            else:
                cargo_encontrado["monto"] = round(monto_val, 2)

    guardar_json(RUTA_CARGOS_EXTRAS, cargos)
    print("\nCargo extra actualizado correctamente.")

def eliminar_cargo_extra():  # 5. Eliminar / Restaurar cargo extra
    imprimir_titulo("ELIMINAR / RESTAURAR CARGO EXTRA")
    cargos = leer_json(RUTA_CARGOS_EXTRAS) or []

    if not ver_cargos_extras():
        return

    id_cargo = pedir_entero("\nIngrese ID del cargo que desea eliminar/restaurar: ")

    for cargo in cargos:
        if cargo.get("id_cargo_extra") == id_cargo:
            if cargo.get("estado") == "Activo":
                cargo["estado"] = "Inactivo"
                print(f"\nEl cargo '{cargo['nombre']}' ha sido eliminado (desactivado).")
            else:
                cargo["estado"] = "Activo"
                print(f"\nEl cargo '{cargo['nombre']}' ha sido restaurado (activado).")

            guardar_json(RUTA_CARGOS_EXTRAS, cargos)
            return

    print("Error: Cargo no encontrado.")

# ====================================================================
# MENÚ PRINCIPAL DEL MÓDULO
# ====================================================================

def menu_cargos_extras():
    while True:
        imprimir_titulo("GESTIÓN DE CARGOS EXTRAS")
        print("1. Crear cargo extra (General)")
        print("2. Asignar cargo extra (A Carrera, Salón o Alumno)")
        print("3. Editar cargo extra")
        print("4. Ver cargos extras")
        print("5. Eliminar / Restaurar cargo extra")
        print("6. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            crear_cargo_extra()
        elif opcion == "2":
            asignar_cargo_extra()
        elif opcion == "3":
            editar_cargo_extra()
        elif opcion == "4":
            ver_cargos_extras()
        elif opcion == "5":
            eliminar_cargo_extra()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
