from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"
RUTA_PAGOS_REALIZADOS = "datos/pagos_realizados.json"


# --- FUNCIONES DE VALIDACIÓN (ANTI-ERRORES) ---

def pedir_entero(mensaje):
    """Asegura que el input sea numérico y evita que el programa colapse."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: No se permiten números negativos.")
            else:
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras).")


# --- FUNCIONES DE BÚSQUEDA SEGURA ---

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
                f"ID: {plantilla.get('id_plantilla')} | {plantilla.get('nombre_plantilla')} | Carrera: {plantilla.get('nombre_carrera')}")

def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES")
    for salon in salones:
        if salon.get("estado") == "Activo" and salon.get("id_carrera") == id_carrera:
            print(f"ID: {salon.get('id_salon')} | {salon.get('nombre_salon')} | Turno: {salon.get('turno')}")

def obtener_alumnos_salon(alumnos, asignaciones, id_salon):
    resultado = []
    for asignacion in asignaciones:
        if asignacion.get("estado") == "Activo" and asignacion.get("id_salon") == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion.get("id_alumno"))
            if alumno:
                resultado.append(alumno)
    return resultado

def obtener_cargos_oficiales(cargos, id_plantilla, id_carrera):
    resultado = []
    for cargo in cargos:
        if (cargo.get("estado") == "Activo"
                and cargo.get("id_plantilla") == id_plantilla
                and cargo.get("id_carrera") == id_carrera):
            resultado.append(cargo)
    return resultado

def obtener_descuento_alumno(descuentos, id_alumno, id_cargo_oficial):
    for descuento in descuentos:
        if (descuento.get("estado") == "Activo"
                and descuento.get("id_alumno") == id_alumno
                and descuento.get("id_cargo_oficial") == id_cargo_oficial):
            return descuento
    return None

def obtener_cargos_extras_alumno(cargos_extras, id_plantilla, id_carrera, id_salon, id_alumno):
    resultado = []
    for cargo in cargos_extras:
        if cargo.get("estado") != "Activo":
            continue
        # Aplica a todo el mundo (General) o coincide la plantilla
        if cargo.get("aplica_a") == "General":
            resultado.append(cargo)
            continue

        if cargo.get("id_plantilla") != id_plantilla:
            continue

        if cargo.get("aplica_a") == "Carrera" and cargo.get("id_carrera") == id_carrera:
            resultado.append(cargo)
        elif cargo.get("aplica_a") == "Salón" and cargo.get("id_salon") == id_salon:
            resultado.append(cargo)
        elif cargo.get("aplica_a") == "Alumno" and cargo.get("id_alumno") == id_alumno:
            resultado.append(cargo)
    return resultado

def obtener_total_pagado(pagos, id_alumno, id_plantilla):
    total = 0
    for pago in pagos:
        if (pago.get("estado") == "Activo"
                and pago.get("id_alumno") == id_alumno
                and pago.get("id_plantilla") == id_plantilla):
            total += pago.get("monto_pagado", 0.0)
    return round(total, 2)


# --- LÓGICA FINANCIERA CENTRAL ---

def calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos):
    total_oficial = 0
    total_descuentos = 0
    total_extra = 0
    detalle_oficial = []
    detalle_extra = []

    # Procesar Cargos Oficiales y sus Descuentos
    for cargo in cargos_oficiales:
        descuento = obtener_descuento_alumno(descuentos, alumno.get("id_alumno"), cargo.get("id_cargo_oficial"))
        monto_original = cargo.get("monto", 0.0)
        monto_final = monto_original

        if descuento:
            monto_final = descuento.get("monto_final", monto_original)
            total_descuentos += monto_original - monto_final

        total_oficial += monto_final
        detalle_oficial.append({
            "cargo": cargo.get("nombre_cargo", "Desconocido"),
            "monto_original": monto_original,
            "monto_final": monto_final,
            "descuento": descuento.get("nombre_descuento") if descuento else "Sin descuento"})

    # Procesar Cargos Extras
    extras = obtener_cargos_extras_alumno(
        cargos_extras,
        plantilla.get("id_plantilla"),
        plantilla.get("id_carrera"),
        salon.get("id_salon"),
        alumno.get("id_alumno")
    )
    for extra in extras:
        monto_extra = extra.get("monto", 0.0)
        total_extra += monto_extra
        detalle_extra.append({
            "cargo": extra.get("nombre", "Extra Desconocido"),
            "monto": monto_extra,
            "aplica_a": extra.get("aplica_a", "N/A")})

    total_debe = round(total_oficial + total_extra, 2)
    total_pagado = obtener_total_pagado(pagos, alumno.get("id_alumno"), plantilla.get("id_plantilla"))
    deuda = round(total_debe - total_pagado, 2)

    return {
        "alumno": f"{alumno.get('nombres', '')} {alumno.get('apellidos', '')}".strip(),
        "dni": alumno.get("dni", "N/A"),
        "total_oficial": round(total_oficial, 2),
        "total_descuentos": round(total_descuentos, 2),
        "total_extra": round(total_extra, 2),
        "total_debe": total_debe,
        "total_pagado": total_pagado,
        "deuda": deuda,
        "detalle_oficial": detalle_oficial,
        "detalle_extra": detalle_extra}

def mostrar_resumen_alumno(resumen):
    print("\n------------------------------------")
    print(f"Alumno: {resumen['alumno']}")
    print(f"DNI: {resumen['dni']}")

    print("\nCARGOS OFICIALES:")
    if not resumen["detalle_oficial"]:
        print("- Sin cargos oficiales asignados")
    for item in resumen["detalle_oficial"]:
        print(
            f"- {item['cargo']} | Original: S/ {item['monto_original']} | Descuento: {item['descuento']} | Final: S/ {item['monto_final']}")

    print("\nCARGOS EXTRAS:")
    if not resumen["detalle_extra"]:
        print("- Sin cargos extras")
    else:
        for item in resumen["detalle_extra"]:
            print(f"- {item['cargo']} | S/ {item['monto']} | Aplica a: {item['aplica_a']}")

    print("\nRESUMEN:")
    print(f"Total cargos oficiales: S/ {resumen['total_oficial']}")
    print(f"Total descuentos aplicados: S/ {resumen['total_descuentos']}")
    print(f"Total cargos extras: S/ {resumen['total_extra']}")
    print(f"Total a pagar: S/ {resumen['total_debe']}")
    print(f"Total pagado: S/ {resumen['total_pagado']}")
    print(f"Deuda pendiente: S/ {resumen['deuda']}")


def seleccionar_plantilla_salon():
    plantillas = leer_json(RUTA_PLANTILLAS) or []
    salones = leer_json(RUTA_SALONES) or []

    if not plantillas:
        print("No hay plantillas registradas en el sistema.")
        return None, None

    mostrar_plantillas(plantillas)
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if not plantilla:
        print("Plantilla no válida o inactiva.")
        return None, None

    mostrar_salones(salones, plantilla.get("id_carrera"))
    id_salon = pedir_entero("\nIngrese ID de salón: ")

    salon = buscar_por_id(salones, "id_salon", id_salon)
    if not salon or salon.get("id_carrera") != plantilla.get("id_carrera"):
        print("Salón no válido para esta plantilla.")
        return None, None

    return plantilla, salon



# --- MÓDULOS DEL MENÚ ---

def resumen_por_salon():
    alumnos = leer_json(RUTA_ALUMNOS) or []
    asignaciones = leer_json(RUTA_ASIGNACIONES) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS) or []
    pagos = leer_json(RUTA_PAGOS_REALIZADOS) or []

    plantilla, salon = seleccionar_plantilla_salon()
    if not plantilla or not salon:
        return

    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon.get("id_salon"))
    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla.get("id_plantilla"), plantilla.get("id_carrera"))

    if not alumnos_salon:
        print("No hay alumnos en este salón.")
        return

    imprimir_titulo("RESUMEN FINANCIERO POR SALÓN")
    print(f"Plantilla: {plantilla.get('nombre_plantilla')}")
    print(f"Carrera: {plantilla.get('nombre_carrera')}")
    print(f"Salón: {salon.get('nombre_salon')} | Turno: {salon.get('turno')}")

    total_general_debe = 0
    total_general_pagado = 0
    total_general_deuda = 0

    for alumno in alumnos_salon:
        resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
        mostrar_resumen_alumno(resumen)
        total_general_debe += resumen["total_debe"]
        total_general_pagado += resumen["total_pagado"]
        total_general_deuda += resumen["deuda"]

    print("\n====================================")
    print("      TOTAL GENERAL DEL SALÓN       ")
    print("====================================")
    print(f"Total general a cobrar: S/ {round(total_general_debe, 2)}")
    print(f"Total general recaudado: S/ {round(total_general_pagado, 2)}")
    print(f"Total general en deuda: S/ {round(total_general_deuda, 2)}")


def resumen_por_alumno():
    alumnos = leer_json(RUTA_ALUMNOS) or []
    asignaciones = leer_json(RUTA_ASIGNACIONES) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS) or []
    pagos = leer_json(RUTA_PAGOS_REALIZADOS) or []

    plantilla, salon = seleccionar_plantilla_salon()
    if not plantilla or not salon:
        return

    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon.get("id_salon"))
    if not alumnos_salon:
        print("No hay alumnos en este salón.")
        return

    imprimir_titulo("ALUMNOS DEL SALÓN")
    for alumno in alumnos_salon:
        print(
            f"ID: {alumno.get('id_alumno')} | {alumno.get('nombres')} {alumno.get('apellidos')} | DNI: {alumno.get('dni')}")

    id_alumno = pedir_entero("\nIngrese ID del alumno: ")
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)

    if not alumno:
        print("Alumno no válido.")
        return

    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla.get("id_plantilla"), plantilla.get("id_carrera"))
    resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
    imprimir_titulo("RESUMEN FINANCIERO INDIVIDUAL")
    mostrar_resumen_alumno(resumen)


def alumnos_con_deuda():
    alumnos = leer_json(RUTA_ALUMNOS) or []
    asignaciones = leer_json(RUTA_ASIGNACIONES) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS) or []
    pagos = leer_json(RUTA_PAGOS_REALIZADOS) or []

    plantilla, salon = seleccionar_plantilla_salon()
    if not plantilla or not salon:
        return

    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon.get("id_salon"))
    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla.get("id_plantilla"), plantilla.get("id_carrera"))

    imprimir_titulo("ALUMNOS CON DEUDA PENDIENTE")
    encontrados = 0

    for alumno in alumnos_salon:
        resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
        if resumen["deuda"] > 0:
            encontrados += 1
            print("\n-----------------------------")
            print(f"Alumno: {resumen['alumno']} | DNI: {resumen['dni']}")
            print(f"Total facturado: S/ {resumen['total_debe']}")
            print(f"Monto abonado: S/ {resumen['total_pagado']}")
            print(f"Deuda actual: S/ {resumen['deuda']}")

    if encontrados == 0:
        print("\n¡Excelente! No hay alumnos con deuda en este salón.")


def menu_resumen_pagos():
    while True:
        imprimir_titulo("RESUMEN DE PAGOS Y DEUDAS")
        print("1. Resumen financiero general por salón")
        print("2. Resumen financiero detallado por alumno")
        print("3. Listar alumnos con deuda")
        print("4. Volver al menú de gestión")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            resumen_por_salon()
        elif opcion == "2":
            resumen_por_alumno()
        elif opcion == "3":
            alumnos_con_deuda()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")