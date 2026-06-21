from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
from director.control_administrativa.descuentos import crear_descuento_convenio, ver_descuentos_convenios
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS = "datos/descuentos_convenios.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"


# --- FUNCIONES DE VALIDACIÓN---

def pedir_entero(mensaje):
    """Asegura que el ID ingresado sea un número válido y no letras."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: No se permiten números negativos.")
            else:
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras).")


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item.get(campo_id) == valor_id and item.get("estado") == "Activo":
            return item
    return None


def calcular_monto_final(monto, descuento):
    tipo = descuento.get("tipo")
    valor = descuento.get("valor", 0)

    if tipo == "Porcentaje":
        return round(monto - (monto * valor / 100), 2)
    elif tipo == "Monto fijo":
        final = monto - valor
        return round(final if final > 0 else 0, 2)

    return monto


# --- VISUALIZACIÓN DE DATOS ---

def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS")
    for p in plantillas:
        if p.get("estado") == "Activo":
            print(f"ID: {p.get('id_plantilla')} | {p.get('nombre_plantilla')} | Carrera: {p.get('nombre_carrera')}")


def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES")
    for s in salones:
        if s.get("estado") == "Activo" and s.get("id_carrera") == id_carrera:
            print(f"ID: {s.get('id_salon')} | {s.get('nombre_salon')} | Turno: {s.get('turno')}")


def mostrar_alumnos_salon(alumnos, asignaciones, id_salon):
    imprimir_titulo("ALUMNOS DEL SALÓN")
    encontrados = 0
    for a in asignaciones:
        if a.get("estado") == "Activo" and a.get("id_salon") == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", a.get("id_alumno"))
            if alumno:
                encontrados += 1
                print(
                    f"ID: {alumno.get('id_alumno')} | {alumno.get('nombres')} {alumno.get('apellidos')} | DNI: {alumno.get('dni')}")
    if encontrados == 0:
        print("No hay alumnos asignados a este salón.")


def mostrar_cargos_oficiales(cargos, id_plantilla, id_carrera):
    imprimir_titulo("CARGOS OFICIALES")
    encontrados = 0
    for c in cargos:
        if (c.get("estado") == "Activo" and c.get("id_plantilla") == id_plantilla and c.get(
                "id_carrera") == id_carrera):
            encontrados += 1
            print(
                f"ID: {c.get('id_cargo_oficial')} | {c.get('nombre_cargo')} | S/ {c.get('monto')} | {c.get('frecuencia')}")
    if encontrados == 0:
        print("No hay cargos oficiales para esta plantilla y carrera.")


def mostrar_descuentos(descuentos):
    imprimir_titulo("DESCUENTOS / CONVENIOS DISPONIBLES")
    for d in descuentos:
        if d.get("estado") == "Activo":
            simbolo = "%" if d.get("tipo") == "Porcentaje" else "S/"
            print(f"ID: {d.get('id_descuento')} | {d.get('nombre')} | {d.get('valor')} {simbolo}")


# --- LÓGICA DE ASIGNACIÓN ---

def descuento_ya_asignado(asignaciones, id_alumno, id_cargo_oficial):
    for a in asignaciones:
        if (a.get("estado") == "Activo" and a.get("id_alumno") == id_alumno and a.get(
                "id_cargo_oficial") == id_cargo_oficial):
            return True
    return False


def asignar_descuento_alumno():
    imprimir_titulo("NUEVA ASIGNACIÓN DE DESCUENTO ALUMNO")

    plantillas = leer_json(RUTA_PLANTILLAS) or []
    salones = leer_json(RUTA_SALONES) or []
    alumnos = leer_json(RUTA_ALUMNOS) or []
    asignaciones_alumnos = leer_json(RUTA_ASIGNACIONES) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    descuentos = leer_json(RUTA_DESCUENTOS) or []
    descuentos_alumnos = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []

    if not cargos:
        print("Primero debe crear cargos oficiales.")
        return
    if not descuentos:
        print("Primero debe crear descuentos o convenios base.")
        return

    mostrar_plantillas(plantillas)
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if not plantilla:
        print("Plantilla no válida o inactiva.")
        return

    mostrar_salones(salones, plantilla.get("id_carrera"))
    id_salon = pedir_entero("\nIngrese ID de salón: ")
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if not salon or salon.get("id_carrera") != plantilla.get("id_carrera"):
        print("Salón no válido para la plantilla seleccionada.")
        return

    mostrar_alumnos_salon(alumnos, asignaciones_alumnos, id_salon)
    id_alumno = pedir_entero("\nIngrese ID del alumno: ")
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if not alumno:
        print("Alumno no válido.")
        return

    mostrar_cargos_oficiales(cargos, id_plantilla, plantilla.get("id_carrera"))
    id_cargo = pedir_entero("\nIngrese ID del cargo oficial: ")
    cargo = buscar_por_id(cargos, "id_cargo_oficial", id_cargo)
    if not cargo or cargo.get("id_plantilla") != id_plantilla:
        print("Cargo oficial no válido.")
        return

    if descuento_ya_asignado(descuentos_alumnos, id_alumno, id_cargo):
        print("Este alumno ya tiene un descuento activo para este cargo oficial.")
        return

    mostrar_descuentos(descuentos)
    id_descuento = pedir_entero("\nIngrese ID del descuento/convenio: ")
    descuento = buscar_por_id(descuentos, "id_descuento", id_descuento)
    if not descuento:
        print("Descuento no válido.")
        return

    monto_final = calcular_monto_final(cargo.get("monto", 0), descuento)

    nueva_asignacion = {
        "id_descuento_alumno": generar_id(descuentos_alumnos, "id_descuento_alumno"),
        "id_alumno": alumno.get("id_alumno"),
        "nombre_alumno": f"{alumno.get('nombres', '')} {alumno.get('apellidos', '')}".strip(),
        "dni": alumno.get("dni"),
        "id_plantilla": plantilla.get("id_plantilla"),
        "nombre_plantilla": plantilla.get("nombre_plantilla"),
        "id_carrera": plantilla.get("id_carrera"),
        "nombre_carrera": plantilla.get("nombre_carrera"),
        "id_salon": salon.get("id_salon"),
        "nombre_salon": salon.get("nombre_salon"),
        "turno": salon.get("turno"),
        "id_cargo_oficial": cargo.get("id_cargo_oficial"),
        "nombre_cargo": cargo.get("nombre_cargo"),
        "monto_original": cargo.get("monto"),
        "id_descuento": descuento.get("id_descuento"),
        "nombre_descuento": descuento.get("nombre"),
        "tipo_descuento": descuento.get("tipo"),
        "valor_descuento": descuento.get("valor"),
        "monto_final": monto_final,
        "estado": "Activo"
    }

    descuentos_alumnos.append(nueva_asignacion)
    guardar_json(RUTA_DESCUENTOS_ALUMNOS, descuentos_alumnos)

    print("\nDescuento asignado correctamente.")
    print(f"Alumno: {nueva_asignacion['nombre_alumno']}")
    print(f"Cargo: {nueva_asignacion['nombre_cargo']} (Original: S/ {nueva_asignacion['monto_original']})")
    print(f"Descuento aplicado: {nueva_asignacion['nombre_descuento']}")
    print(f"Nuevo monto a pagar: S/ {nueva_asignacion['monto_final']}")


def ver_descuentos_asignados():
    imprimir_titulo("DESCUENTOS ASIGNADOS A ALUMNOS")
    asignaciones = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []

    if not asignaciones:
        print("No hay descuentos asignados en el sistema.")
        return False

    for a in asignaciones:
        print("\n-----------------------------")
        print(f"ID Asignación: {a.get('id_descuento_alumno')} | Estado: {a.get('estado')}")
        print(f"Alumno: {a.get('nombre_alumno')} | DNI: {a.get('dni')}")
        print(f"Cargo: {a.get('nombre_cargo')} | Monto original: S/ {a.get('monto_original')}")
        print(f"Descuento: {a.get('nombre_descuento')} ({a.get('valor_descuento')} {a.get('tipo_descuento')})")
        print(f"Monto final: S/ {a.get('monto_final')}")

    return True


def modificar_descuento_asignado():
    imprimir_titulo("MODIFICAR DESCUENTO ASIGNADO")
    asignaciones = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    descuentos = leer_json(RUTA_DESCUENTOS) or []

    if not ver_descuentos_asignados():
        return

    id_asignacion = pedir_entero("\nIngrese el ID de la asignación que desea modificar: ")

    asignacion = next((a for a in asignaciones if a.get("id_descuento_alumno") == id_asignacion), None)

    if not asignacion:
        print("Error: No se encontró la asignación.")
        return

    if asignacion.get("estado") != "Activo":
        print("Error: No se puede modificar una asignación inactiva. Restáurela primero.")
        return

    print(f"\nAlumno: {asignacion.get('nombre_alumno')} | Cargo: {asignacion.get('nombre_cargo')}")
    print("Seleccione el NUEVO descuento que desea aplicar:")

    mostrar_descuentos(descuentos)
    id_nuevo_desc = pedir_entero("\nIngrese el ID del nuevo descuento: ")

    nuevo_descuento = buscar_por_id(descuentos, "id_descuento", id_nuevo_desc)
    if not nuevo_descuento:
        print("Error: Descuento no válido o inactivo.")
        return

    nuevo_monto_final = calcular_monto_final(asignacion.get("monto_original", 0), nuevo_descuento)

    asignacion["id_descuento"] = nuevo_descuento.get("id_descuento")
    asignacion["nombre_descuento"] = nuevo_descuento.get("nombre")
    asignacion["tipo_descuento"] = nuevo_descuento.get("tipo")
    asignacion["valor_descuento"] = nuevo_descuento.get("valor")
    asignacion["monto_final"] = nuevo_monto_final

    guardar_json(RUTA_DESCUENTOS_ALUMNOS, asignaciones)
    print("\nAsignación actualizada correctamente.")
    print(f"El nuevo monto final a pagar es: S/ {nuevo_monto_final}")



# --- INTERFAZ PRINCIPAL DEL MÓDULO ---

def menu_asignar_descuentos():
    while True:
        imprimir_titulo("GESTIÓN DE DESCUENTOS Y CONVENIOS")
        print("--- Catálogo Base ---")
        print("1. Crear nuevo descuento/convenio base")
        print("2. Ver descuentos/convenios base")
        print("\n--- Operaciones sobre Alumnos ---")
        print("3. Asignar descuento a un alumno")
        print("4. Ver descuentos asignados")
        print("5. Modificar descuento de un alumno")
        print("\n6. Volver al menú anterior")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            crear_descuento_convenio()
        elif opcion == "2":
            ver_descuentos_convenios()
        elif opcion == "3":
            asignar_descuento_alumno()
        elif opcion == "4":
            ver_descuentos_asignados()
        elif opcion == "5":
            modificar_descuento_asignado()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")