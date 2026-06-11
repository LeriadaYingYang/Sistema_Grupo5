from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa
from secretaria.logica_pagos import buscar_alumno_por_dni, obtener_deudas_y_pagos, registrar_amortizacion

def login_secretaria():
    limpiar_pantalla()
    imprimir_titulo("LOGIN SECRETARÍA")
    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ")

    # Credenciales de acceso para la simulación
    if usuario == "secretaria" and password == "secre2026":
        print("\n Acceso concedido.")
        pausa()
        menu_secretaria()
    else:
        print("\n Credenciales incorrectas.")
        pausa()

def menu_secretaria():
    while True:
        limpiar_pantalla()
        imprimir_titulo("CONTROL ADMINISTRATIVO - VENTANILLA")
        imprimir_menu([
            "Buscar deudas del alumno (Ver Estado)",
            "Amortizar o pagar deuda (Registrar Pago)",
            "Ver historial de pagos de un alumno",
            "Volver al menú principal"
        ])
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            imprimir_titulo("5.4.1. BUSCAR DEUDAS DEL ALUMNO")
            dni = input("Ingrese DNI del alumno: ").strip()
            alumno = buscar_alumno_por_dni(dni)
            
            if alumno:
                print(f"\nAlumno: {alumno['nombres'].upper()} {alumno['apellidos'].upper()}")
                deudas = obtener_deudas_y_pagos(alumno["id_alumno"])
                
                hay_deudas = False
                for d in deudas:
                    print(f"\nConcepto [{d['tipo']}]: {d['nombre']}")
                    print(f"  Monto Total : S/ {d['monto_con_descuento']}")
                    print(f"  Amortizado  : S/ {d['pagado']}")
                    print(f"  Saldo Neto  : S/ {d['saldo_pendiente']}")
                    if d['saldo_pendiente'] > 0:
                        hay_deudas = True
                
                if not hay_deudas:
                    print("\n El alumno no registra saldos pendientes.")
            else:
                print("\n Alumno no encontrado o DNI inválido.")
            pausa()

        elif opcion == "2":
            limpiar_pantalla()
            imprimir_titulo("5.4.2. AMORTIZAR O PAGAR DEUDA")
            dni = input("Ingrese DNI del alumno: ").strip()
            alumno = buscar_alumno_por_dni(dni)
            
            if alumno:
                print(f"\nAlumno: {alumno['nombres'].upper()} {alumno['apellidos'].upper()}")
                deudas = obtener_deudas_y_pagos(alumno["id_alumno"])
                
                deudas_pendientes = [d for d in deudas if d["saldo_pendiente"] > 0]
                
                if len(deudas_pendientes) == 0:
                    print("\nEl alumno no tiene deudas pendientes por pagar.")
                else:
                    print("\nCargos con saldo pendiente:")
                    for i, d in enumerate(deudas_pendientes, start=1):
                        print(f"{i}. {d['nombre']} ({d['tipo']}) - Pendiente: S/ {d['saldo_pendiente']}")
                    
                    try:
                        idx = int(input("\nSeleccione el número de concepto a pagar: ")) - 1
                        if 0 <= idx < len(deudas_pendientes):
                            seleccionada = deudas_pendientes[idx]
                            monto_pago = float(input(f"Monto a abonar (Máx S/ {seleccionada['saldo_pendiente']}): S/ "))
                            
                            if 0 < monto_pago <= seleccionada["saldo_pendiente"]:
                                registrar_amortizacion(
                                    alumno["id_alumno"],
                                    alumno["nombres"] + " " + alumno["apellidos"],
                                    seleccionada["id_concepto"],
                                    seleccionada["tipo"],
                                    seleccionada["nombre"],
                                    monto_pago
                                )
                                print("\n Pago registrado con éxito.")
                            else:
                                print("\n Monto inválido o excede el saldo pendiente.")
                        else:
                            print("\n Selección fuera de rango.")
                    except ValueError:
                        print("\n Error de entrada: Ingrese valores numéricos.")
            else:
                print("\n Alumno no encontrado.")
            pausa()

        elif opcion == "3":
            limpiar_pantalla()
            imprimir_titulo("5.4.3. HISTORIAL DE PAGOS DEL ALUMNO")
            dni = input("Ingrese DNI del alumno: ").strip()
            alumno = buscar_alumno_por_dni(dni)
            
            if alumno:
                print(f"\nHistorial de caja de: {alumno['nombres'].upper()} {alumno['apellidos'].upper()}")
                from basedatos_json import leer_json
                todos_los_pagos = leer_json("datos/pagos_realizados.json")
                
                encontrados = 0
                for p in todos_los_pagos:
                    if p["id_alumno"] == alumno["id_alumno"] and p["estado"] == "Activo":
                        print(f"🔹 [{p['fecha_pago']}] Recibo #{p['id_pago']} - {p['nombre_concepto']}: S/ {p['monto_pagado']}")
                        encontrados += 1
                if encontrados == 0:
                    print("\nNo se registran transacciones previas en el sistema para este alumno.")
            else:
                print("\n Alumno no encontrado.")
            pausa()

        elif opcion == "4":
            print("\nVolviendo al menú principal...")
            break