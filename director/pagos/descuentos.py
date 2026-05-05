from basedatos_json import leer_json, guardar_json, generar_id

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

def pedir_tipo_descuento():
    while True:
        print("""
Tipo de descuento:

1. Porcentaje
2. Monto fijo
""")

        opcion = input("Seleccione tipo: ")

        if opcion == "1":
            return "Porcentaje"
        elif opcion == "2":
            return "Monto fijo"
        else:
            print("Opción inválida.")

def crear_descuento_convenio():
    print("\n====================================")
    print("     CREAR DESCUENTO O CONVENIO")
    print("====================================")

    descuentos = leer_json(RUTA_DESCUENTOS)

    nombre = input("Nombre del descuento/convenio: ")
    tipo = pedir_tipo_descuento()

    try:
        valor = float(input("Valor del descuento: "))
    except ValueError:
        print("Debe ingresar un valor válido.")
        return

    motivo = input("Motivo o descripción: ")

    nuevo_descuento = {
        "id_descuento": generar_id(descuentos, "id_descuento"),
        "nombre": nombre,
        "tipo": tipo,
        "valor": valor,
        "motivo": motivo,
        "aplica_a": "Cargo oficial",
        "estado": "Activo"}

    descuentos.append(nuevo_descuento)
    guardar_json(RUTA_DESCUENTOS, descuentos)

    print("\nDescuento/convenio creado correctamente.")
    print("Este descuento solo aplica a cargos oficiales.")