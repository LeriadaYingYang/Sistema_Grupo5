import datetime
from basedatos_json import leer_json, guardar_json, generar_id

RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"
RUTA_PAGOS_REALIZADOS = "datos/pagos_realizados.json"

def buscar_alumno_por_dni(dni):
    """Busca un alumno activo por su DNI y devuelve su diccionario."""
    alumnos = leer_json(RUTA_ALUMNOS)
    for alu in alumnos:
        if alu["dni"] == dni and alu["estado"] == "Activo":
            return alu
    return None

def obtener_deudas_y_pagos(id_alumno):
    """
    Calcula de manera detallada los cargos, descuentos y pagos de un alumno.
    Retorna un diccionario con los saldos netos por concepto (Con retorno).
    """
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    cargos_oficiales = leer_json(RUTA_CARGOS_OFICIALES)
    descuentos_alumnos = leer_json(RUTA_DESCUENTOS_ALUMNOS)
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS)
    pagos_realizados = leer_json(RUTA_PAGOS_REALIZADOS)

    # 1. Encontrar asignación académica del alumno para saber su carrera y plantilla
    asig_alumno = None
    for asig in asignaciones:
        if asig["id_alumno"] == id_alumno and asig["estado"] == "Activo":
            asig_alumno = asig
            break

    lista_deudas = []

    if asig_alumno:
        # 2. Cargar Cargos Oficiales aplicables a su plantilla y carrera
        for co in cargos_oficiales:
            if co["id_plantilla"] == asig_alumno["id_plantilla"] and co["id_carrera"] == asig_alumno["id_carrera"] and co["estado"] == "Activo":
                monto_final = co["monto"]
                
                # Buscar si este alumno tiene un descuento asignado para ESTE cargo oficial
                for da in descuentos_alumnos:
                    if da["id_alumno"] == id_alumno and da["id_cargo_oficial"] == co["id_cargo_oficial"] and da["estado"] == "Activo":
                        monto_final = da["monto_final"]
                        break
                
                lista_deudas.append({
                    "id_concepto": co["id_cargo_oficial"],
                    "tipo": "Oficial",
                    "nombre": co["nombre_cargo"],
                    "monto_original": co["monto"],
                    "monto_con_descuento": monto_final,
                    "pagado": 0.0,
                    "saldo_pendiente": monto_final
                })

    # 3. Cargar Cargos Extras asignados específicamente a este alumno, su salón o carrera
    for ce in cargos_extras:
        if ce["estado"] == "Activo":
            aplica = False
            if ce.get("id_alumno") == id_alumno:
                aplica = True
            elif ce.get("id_salon") == (asig_alumno["id_salon"] if asig_alumno else None) and not ce.get("id_alumno"):
                aplica = True
            elif ce.get("id_carrera") == (asig_alumno["id_carrera"] if asig_alumno else None) and not ce.get("id_salon") and not ce.get("id_alumno"):
                aplica = True

            if aplica:
                lista_deudas.append({
                    "id_concepto": ce["id_cargo_extra"],
                    "tipo": "Extra",
                    "nombre": ce["nombre"],
                    "monto_original": ce["monto"],
                    "monto_con_descuento": ce["monto"],
                    "pagado": 0.0,
                    "saldo_pendiente": ce["monto"]
                })

    # 4. Cruzar y restar los pagos realizados acumulados en el historial
    for pago in pagos_realizados:
        if pago["id_alumno"] == id_alumno and pago["estado"] == "Activo":
            for deuda in lista_deudas:
                if deuda["id_concepto"] == pago["id_concepto"] and deuda["tipo"] == pago["tipo_concepto"]:
                    deuda["pagado"] += pago["monto_pagado"]
                    deuda["saldo_pendiente"] = round(deuda["monto_con_descuento"] - deuda["pagado"], 2)
                    if deuda["saldo_pendiente"] < 0:
                        deuda["saldo_pendiente"] = 0.0

    return lista_deudas

def registrar_amortizacion(id_alumno, nombre_alumno, id_concepto, tipo_concepto, nombre_concepto, monto_a_pagar):
    """Registra una amortización de pago en el archivo JSON."""
    pagos = leer_json(RUTA_PAGOS_REALIZADOS)
    
    nuevo_pago = {
        "id_pago": generar_id(pagos, "id_pago"),
        "id_alumno": id_alumno,
        "nombre_alumno": nombre_alumno,
        "id_concepto": id_concepto,
        "tipo_concepto": tipo_concepto,
        "nombre_concepto": nombre_concepto,
        "monto_pagado": round(monto_a_pagar, 2),
        "fecha_pago": str(datetime.date.today()),
        "estado": "Activo"
    }
    
    pagos.append(nuevo_pago)
    guardar_json(RUTA_PAGOS_REALIZADOS, pagos)
    return nuevo_pago