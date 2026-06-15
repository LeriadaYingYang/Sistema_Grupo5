from basedatos_json import leer_json
from director.utilidades import imprimir_titulo
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa
from datetime import datetime

R_ALUMNOS = "datos/alumnos.json"
R_ASIG_ALUMNOS = "datos/alumnos_asignaciones.json"
R_C_OFICIALES = "datos/cargos_oficiales.json"
R_C_EXTRAS = "datos/cargos_extras.json"
R_D_ALUMNOS = "datos/descuentos_alumnos.json"
R_D_CONVENIOS = "datos/descuentos_convenios.json"
R_PAGOS = "datos/pagos_realizados.json"

def obtener_datos_alumno_por_dni(dni):
    alumnos = leer_json(R_ALUMNOS)
    asignaciones = leer_json(R_ASIG_ALUMNOS)
    
    alumno_encontrado = None
    for a in alumnos:
        if a.get("dni") == dni.strip():
            alumno_encontrado = a
            break
    if not alumno_encontrado:
        return None, None, None
    id_alum = alumno_encontrado["id_alumno"]
    id_carrera = None
    id_salon = None
    
    # Buscar su carrera y salón en el arreglo paralelo de asignaciones
    for asig in asignaciones:
        if asig.get("id_alumno") == id_alum and asig.get("estado") == "Activo":
            id_carrera = asig.get("id_carrera")
            id_salon = asig.get("id_salon")
            break
    return alumno_encontrado, id_carrera, id_salon

def calcular_estado_financiero(id_alum, id_carrera, id_salon):
    total_cargos = 0.0
    total_descuentos = 0.0
    total_pagado = 0.0
    
    # 1. Sumar Cargos Oficiales (por carrera)
    for co in leer_json(R_C_OFICIALES):
        if co.get("estado") == "Activo":
            if co.get("id_carrera") is None or co.get("id_carrera") == id_carrera:
                total_cargos += co.get("monto", 0.0)
    # 2. Sumar Cargos Extras (jerárquico)
    for ce in leer_json(R_C_EXTRAS):
        if ce.get("estado") == "Activo":
            aplica = False
            if ce.get("id_alumno") == id_alum: aplica = True
            elif ce.get("id_salon") == id_salon and id_salon is not None: aplica = True
            elif ce.get("id_carrera") == id_carrera and id_carrera is not None: aplica = True
            elif not ce.get("id_alumno") and not ce.get("id_salon") and not ce.get("id_carrera"): aplica = True
            
            if aplica:
                total_cargos += ce.get("monto", 0.0)
    # 3. Aplicar Descuentos asignados
    convenios = leer_json(R_D_CONVENIOS)
    for da in leer_json(R_D_ALUMNOS):
        if da.get("id_alumno") == id_alum and da.get("estado") == "Activo":
            # Buscar el convenio en el arreglo paralelo
            for conv in convenios:
                if conv.get("id_descuento") == da.get("id_descuento") and conv.get("estado") == "Activo":
                    if conv.get("tipo") == "Fijo":
                        total_descuentos += conv.get("valor", 0.0)
                    elif conv.get("tipo") == "Porcentaje":
                        total_descuentos += total_cargos * (conv.get("valor", 0.0) / 100)
    # 4. Sumar Pagos Realizados
    for p in leer_json(R_PAGOS):
        if p.get("id_alumno") == id_alum and p.get("estado") == "Activo":
            total_pagado += p.get("monto", 0.0)
    # Matemática final
    deuda_bruta = total_cargos - total_descuentos
    if deuda_bruta < 0: deuda_bruta = 0.0
    saldo_neto = deuda_bruta - total_pagado
    
    return total_cargos, total_descuentos, total_pagado, saldo_neto
def mostrar_estado_cuenta():
    imprimir_titulo("CONSULTA DE ESTADO DE CUENTA")
    dni = input("Ingrese el DNI del alumno: ").strip()
    
    alumno, id_carrera, id_salon = obtener_datos_alumno_por_dni(dni)
    
    if not alumno:
        print("\nAlumno no encontrado.")
        return
    print(f"\nAlumno: {alumno['nombres'].title()} {alumno['apellidos'].title()}")
    print("Calculando estructuras financieras...\n")
    
    t_cargos, t_descuentos, t_pagado, saldo_neto = calcular_estado_financiero(alumno["id_alumno"], id_carrera, id_salon)
    
    print("-" * 40)
    print(f"Total Cargos (Oficiales + Extras) : S/ {t_cargos:.2f}")
    print(f"Total Descuentos Aplicados        : S/ -{t_descuentos:.2f}")
    print(f"Deuda Total a Pagar               : S/ {(t_cargos - t_descuentos):.2f}")
    print(f"Total Amortizado (Pagado)         : S/ -{t_pagado:.2f}")
    print("-" * 40)
    
    if saldo_neto <= 0:
        print(f"SALDO NETO PENDIENTE: S/ 0.00 (AL DÍA)")
    else:
        print(f"SALDO NETO PENDIENTE: S/ {saldo_neto:.2f}")
def registrar_nuevo_pago():
    imprimir_titulo("REGISTRAR PAGO DE ALUMNO")
    dni = input("Ingrese el DNI del alumno: ").strip()
    
    alumno, id_carrera, id_salon = obtener_datos_alumno_por_dni(dni)
    if not alumno:
        print("\nAlumno no encontrado.")
        return
    t_cargos, t_descuentos, t_pagado, saldo_neto = calcular_estado_financiero(alumno["id_alumno"], id_carrera, id_salon)
    
    if saldo_neto <= 0:
        print(f"\nEl alumno {alumno['nombres'].title()} no presenta deudas pendientes.")
        return
    print(f"\nDeuda actual pendiente: S/ {saldo_neto:.2f}")
    
    try:
        monto_pago = float(input("Ingrese el monto a amortizar (S/): "))
        if monto_pago <= 0:
            print("El pago debe ser mayor a 0.")
            return
        if monto_pago > saldo_neto:
            print("El monto ingresado es mayor a la deuda pendiente.")
            return
    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
        return
    pagos = leer_json(R_PAGOS)
    
    nuevo_pago = {
        "id_pago": generar_id(pagos, "id_pago"),
        "id_alumno": alumno["id_alumno"],
        "monto": round(monto_pago, 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "Activo"
    }
    
    pagos.append(nuevo_pago)
    guardar_json(R_PAGOS, pagos)
    
    print(f"\nPago de S/ {monto_pago:.2f} registrado exitosamente para {alumno['nombres'].title()}.")

def menu_resumen_pagos():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE PAGOS Y ESTADO DE CUENTA")
        imprimir_menu([
            "Consultar Estado de Cuenta (Reporte)",
            "Registrar Nuevo Pago (Amortización)",
            "Volver al submenú anterior"
        ])
        
        opc = input("\nSeleccione una opción: ").strip()
        
        if opc == "1":
            limpiar_pantalla()
            mostrar_estado_cuenta()
            pausa()
        elif opc == "2":
            limpiar_pantalla()
            registrar_nuevo_pago()
            pausa()
        elif opc == "3":
            break
        else:
            print("\nOpción no válida.")
            pausa()