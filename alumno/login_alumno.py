from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa
from secretaria.logica_pagos import buscar_alumno_por_dni, obtener_deudas_y_pagos

def login_alumno():
    limpiar_pantalla()
    imprimir_titulo("PORTAL DEL ESTUDIANTE - IISEM")
    print("Nota: Por disposición institucional, ingrese su DNI como credencial.")
    dni_ingresado = input("\nIngrese su número de DNI: ").strip()

    print("\nValidando acceso de alumno...")
    alumno = buscar_alumno_por_dni(dni_ingresado)

    if alumno:
        print(f"\n Acceso Autorizado. ¡Bienvenido/a, {alumno['nombres'].upper()}!")
        pausa()
        menu_alumno_financiero(alumno)  # Pasamos el diccionario por referencia de forma segura
    else:
        print("\n Error: El DNI no corresponde a un estudiante activo o es incorrecto.")
        pausa()

def menu_alumno_financiero(alumno_actual):
    """Muestra el estado financiero personal del alumno autenticado (Encapsulado)."""
    while True:
        limpiar_pantalla()
        imprimir_titulo(f"ESTADO FINANCIERO: {alumno_actual['nombres'].upper()}")
        imprimir_menu([
            "Ver mis deudas pendientes (Saldos Netos)",
            "Ver mi historial de pagos realizados (Recibos)",
            "Salir del portal estudiantil"
        ])
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            imprimir_titulo("5.5.1. MIS DEUDAS PENDIENTES")
            # Invocamos la función con retorno para obtener el cálculo en tiempo real
            deudas = obtener_deudas_y_pagos(alumno_actual["id_alumno"])
            
            hay_deudas = False
            print(f"Estudiante: {alumno_actual['nombres']} {alumno_actual['apellidos']}")
            print("-" * 40)
            
            for d in deudas:
                if d["saldo_pendiente"] > 0:
                    print(f" {d['nombre']} ({d['tipo']})")
                    print(f"   Monto Base: S/ {d['monto_con_descuento']}")
                    print(f"   Abonado   : S/ {d['pagado']}")
                    print(f"   SALDO NETO: S/ {d['saldo_pendiente']}")
                    print("-" * 40)
                    hay_deudas = True
            
            if not hay_deudas:
                print("\n ¡Felicitaciones! No registras deudas pendientes a la fecha.")
            pausa()

        elif opcion == "2":
            limpiar_pantalla()
            imprimir_titulo("5.5.2. MIS PAGOS REALIZADOS")
            from basedatos_json import leer_json
            todos_los_pagos = leer_json("datos/pagos_realizados.json")
            
            print(f"Comprobantes emitidos a: {alumno_actual['nombres']} {alumno_actual['apellidos']}")
            print("-" * 40)
            
            encontrados = 0
            for pago in todos_los_pagos:
                # El alumno solo puede ver las transacciones asociadas a su ID único (Restricción de alcance)
                if pago["id_alumno"] == alumno_actual["id_alumno"] and pago["estado"] == "Activo":
                    print(f" Recibo N° {pago['id_pago']} | Fecha: {pago['fecha_pago']}")
                    print(f"   Concepto: {pago['nombre_concepto']}")
                    print(f"   Monto   : S/ {pago['monto_pagado']}")
                    print("-" * 40)
                    encontrados += 1
                    
            if encontrados == 0:
                print("\nNo se registran transacciones de pago en el sistema.")
            pausa()

        elif opcion == "3":
            print("\nCerrando sesión del estudiante...")
            break
        else:
            print("\n Opción inválida.")
            pausa()