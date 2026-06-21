from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"
RUTA_PAGOS_REALIZADOS = "datos/pagos_realizados.json"


def pedir_entero(mensaje):  # valida que se ingrese un número entero positivo
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor <= 0:
                print("Error: ingrese un número mayor que cero.")
            else:
                return valor
        except ValueError:
            print("Error: debe ingresar un número válido.")


def pedir_monto(mensaje, maximo):  # valida que el pago no sea negativo ni supere la deuda
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor <= 0:
                print("Error: el monto debe ser mayor que cero.")
            elif valor > maximo:
                print(f"Error: el monto no puede superar la deuda de S/ {maximo}.")
            else:
                return round(valor, 2)
        except ValueError:
            print("Error: debe ingresar un monto válido.")


def pedir_texto(mensaje):  # valida que el texto no quede vacío
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Error: este campo no puede estar vacío.")


def buscar_por_id(lista, campo_id, valor_id):  # busca un registro activo por id
    for item in lista:
        if item.get(campo_id) == valor_id and item.get("estado") == "Activo":
            return item
    return None


def mostrar_plantillas(plantillas):  # muestra plantillas activas
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for plantilla in plantillas:
        if plantilla.get("estado") == "Activo":
            print(
                f"ID: {plantilla.get('id_plantilla')} | "
                f"{plantilla.get('nombre_plantilla')} | "
                f"Carrera: {plantilla.get('nombre_carrera')}"
            )


def mostrar_salones(salones, id_carrera):  # muestra salones de la carrera seleccionada
    imprimir_titulo("SALONES DISPONIBLES")
    for salon in salones:
        if salon.get("estado") == "Activo" and salon.get("id_carrera") == id_carrera:
            print(
                f"ID: {salon.get('id_salon')} | "
                f"{salon.get('nombre_salon')} | "
                f"Turno: {salon.get('turno')}"
            )


def mostrar_alumnos_salon(alumnos, asignaciones, id_salon):  # muestra alumnos asignados al salón
    imprimir_titulo("ALUMNOS DEL SALÓN")
    encontrados = 0

    for asignacion in asignaciones:
        if asignacion.get("estado") == "Activo" and asignacion.get("id_salon") == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion.get("id_alumno"))
            if alumno:
                encontrados += 1
                print(
                    f"ID: {alumno.get('id_alumno')} | "
                    f"{alumno.get('nombres')} {alumno.get('apellidos')} | "
                    f"DNI: {alumno.get('dni')}"
                )

    if encontrados == 0:
        print("No hay alumnos asignados a este salón.")


def alumno_pertenece_salon(asignaciones, id_alumno, id_salon):  # confirma que el alumno pertenezca al salón elegido
    for asignacion in asignaciones:
        if (
            asignacion.get("estado") == "Activo"
            and asignacion.get("id_alumno") == id_alumno
            and asignacion.get("id_salon") == id_salon
        ):
            return True
    return False


def obtener_cargos_oficiales(cargos, id_plantilla, id_carrera):  # obtiene cargos creados para la plantilla y carrera
    resultado = []
    for cargo in cargos:
        if (
            cargo.get("estado") == "Activo"
            and cargo.get("id_plantilla") == id_plantilla
            and cargo.get("id_carrera") == id_carrera
        ):
            resultado.append(cargo)
    return resultado


def obtener_descuento(descuentos, id_alumno, id_cargo_oficial):  # busca descuento aplicado al alumno para ese cargo
    for descuento in descuentos:
        if (
            descuento.get("estado") == "Activo"
            and descuento.get("id_alumno") == id_alumno
            and descuento.get("id_cargo_oficial") == id_cargo_oficial
        ):
            return descuento
    return None


def obtener_pagado_cargo(pagos, id_alumno, id_plantilla, id_cargo_oficial):  # suma pagos anteriores del mismo cargo
    total = 0
    for pago in pagos:
        if (
            pago.get("estado") == "Activo"
            and pago.get("id_alumno") == id_alumno
            and pago.get("id_plantilla") == id_plantilla
            and pago.get("id_cargo_oficial") == id_cargo_oficial
        ):
            total += pago.get("monto_pagado", 0)
    return round(total, 2)


def mostrar_cargos_pendientes(cargos, descuentos, pagos, alumno, plantilla):  # muestra cargos con saldo pendiente
    imprimir_titulo("CARGOS OFICIALES PENDIENTES")
    encontrados = 0

    for cargo in cargos:
        descuento = obtener_descuento(descuentos, alumno.get("id_alumno"), cargo.get("id_cargo_oficial"))
        monto_final = descuento.get("monto_final") if descuento else cargo.get("monto", 0)
        pagado = obtener_pagado_cargo(
            pagos,
            alumno.get("id_alumno"),
            plantilla.get("id_plantilla"),
            cargo.get("id_cargo_oficial")
        )
        saldo = round(monto_final - pagado, 2)

        if saldo > 0:
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID Cargo: {cargo.get('id_cargo_oficial')}")
            print(f"Cargo: {cargo.get('nombre_cargo')}")
            print(f"Monto original: S/ {cargo.get('monto')}")
            print(f"Descuento: {descuento.get('nombre_descuento') if descuento else 'Sin descuento'}")
            print(f"Monto final: S/ {monto_final}")
            print(f"Pagado: S/ {pagado}")
            print(f"Saldo pendiente: S/ {saldo}")

    if encontrados == 0:
        print("El alumno no tiene cargos oficiales pendientes.")

    return encontrados


def pedir_metodo_pago():  # permite seleccionar el método de pago
    while True:
        print("\n--- MÉTODO DE PAGO ---")
        print("1. Efectivo")
        print("2. Yape")
        print("3. Plin")
        print("4. Transferencia")

        opcion = input("Seleccione método: ").strip()

        if opcion == "1":
            return "Efectivo"
        elif opcion == "2":
            return "Yape"
        elif opcion == "3":
            return "Plin"
        elif opcion == "4":
            return "Transferencia"
        else:
            print("Opción inválida.")


def registrar_pago():  # registra un pago asociado a un cargo oficial creado
    imprimir_titulo("REGISTRAR PAGO DE ALUMNO")

    alumnos = leer_json(RUTA_ALUMNOS) or []
    asignaciones = leer_json(RUTA_ASIGNACIONES) or []
    plantillas = leer_json(RUTA_PLANTILLAS) or []
    salones = leer_json(RUTA_SALONES) or []
    cargos = leer_json(RUTA_CARGOS_OFICIALES) or []
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    pagos = leer_json(RUTA_PAGOS_REALIZADOS) or []

    if not alumnos:
        print("No hay alumnos registrados.")
        return

    if not asignaciones:
        print("No hay alumnos asignados a salones.")
        return

    if not cargos:
        print("No hay cargos oficiales creados.")
        return

    mostrar_plantillas(plantillas)
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no válida.")
        return

    mostrar_salones(salones, plantilla.get("id_carrera"))
    id_salon = pedir_entero("\nIngrese ID de salón: ")

    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None or salon.get("id_carrera") != plantilla.get("id_carrera"):
        print("Salón no válido para esta plantilla.")
        return

    mostrar_alumnos_salon(alumnos, asignaciones, id_salon)
    id_alumno = pedir_entero("\nIngrese ID del alumno: ")

    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no válido.")
        return

    if not alumno_pertenece_salon(asignaciones, id_alumno, id_salon):
        print("El alumno no pertenece al salón seleccionado.")
        return

    cargos_disponibles = obtener_cargos_oficiales(
        cargos,
        plantilla.get("id_plantilla"),
        plantilla.get("id_carrera")
    )

    if not cargos_disponibles:
        print("No hay cargos oficiales creados para esta carrera y plantilla.")
        return

    if mostrar_cargos_pendientes(cargos_disponibles, descuentos, pagos, alumno, plantilla) == 0:
        return

    id_cargo = pedir_entero("\nIngrese ID del cargo que va a pagar: ")
    cargo = buscar_por_id(cargos_disponibles, "id_cargo_oficial", id_cargo)

    if cargo is None:
        print("Cargo no válido.")
        return

    descuento = obtener_descuento(descuentos, id_alumno, id_cargo)
    monto_final = descuento.get("monto_final") if descuento else cargo.get("monto", 0)

    pagado_anterior = obtener_pagado_cargo(
        pagos,
        id_alumno,
        plantilla.get("id_plantilla"),
        id_cargo
    )

    saldo = round(monto_final - pagado_anterior, 2)

    if saldo <= 0:
        print("Este cargo ya está pagado.")
        return

    print("\n--- DETALLE DEL CARGO ---")
    print(f"Alumno: {alumno.get('nombres')} {alumno.get('apellidos')}")
    print(f"Cargo: {cargo.get('nombre_cargo')}")
    print(f"Monto final: S/ {monto_final}")
    print(f"Pagado anterior: S/ {pagado_anterior}")
    print(f"Saldo pendiente: S/ {saldo}")

    monto_pagado = pedir_monto("\nMonto a pagar: S/ ", saldo)
    metodo_pago = pedir_metodo_pago()
    observacion = pedir_texto("Observación del pago: ")

    nuevo_pago = {
        "id_pago": generar_id(pagos, "id_pago"),
        "fecha_pago": datetime.now().strftime("%Y-%m-%d"),
        "id_alumno": alumno.get("id_alumno"),
        "nombre_alumno": f"{alumno.get('nombres')} {alumno.get('apellidos')}",
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
        "monto_cargo": cargo.get("monto"),
        "monto_final": monto_final,
        "monto_pagado": monto_pagado,
        "saldo_restante": round(saldo - monto_pagado, 2),
        "metodo_pago": metodo_pago,
        "observacion": observacion,
        "estado": "Activo"
    }

    pagos.append(nuevo_pago)
    guardar_json(RUTA_PAGOS_REALIZADOS, pagos)

    print("\nPago registrado correctamente.")
    print(f"Alumno: {nuevo_pago['nombre_alumno']}")
    print(f"Cargo pagado: {nuevo_pago['nombre_cargo']}")
    print(f"Monto pagado: S/ {nuevo_pago['monto_pagado']}")
    print(f"Saldo restante: S/ {nuevo_pago['saldo_restante']}")