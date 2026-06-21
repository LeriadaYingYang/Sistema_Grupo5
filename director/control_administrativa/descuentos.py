from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"


# ====================================================================
# FUNCIONES DE VALIDACIÓN (A PRUEBA DE ERRORES)
# ====================================================================

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: El campo no puede quedar vacío.")
        else:
            return texto


def pedir_monto(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: El valor no puede ser negativo.")
            else:
                return round(valor, 2)
        except ValueError:
            print("Error: Debe ingresar un valor numérico válido.")


# ====================================================================
# LÓGICA DEL MÓDULO
# ====================================================================

def pedir_tipo_descuento():
    while True:
        print("\n--- TIPO DE DESCUENTO ---")
        print("1. Porcentaje")
        print("2. Monto fijo")
        opcion = input("Seleccione tipo: ").strip()
        if opcion == "1":
            return "Porcentaje"
        elif opcion == "2":
            return "Monto fijo"
        else:
            print("Opción inválida.")


def crear_descuento_convenio():
    imprimir_titulo("CREAR DESCUENTO O CONVENIO")

    # El 'or []' evita que el programa colapse si el JSON está vacío
    descuentos = leer_json(RUTA_DESCUENTOS) or []

    nombre = pedir_texto("Nombre del descuento/convenio: ")
    tipo = pedir_tipo_descuento()

    # Se adapta el mensaje dependiendo si es porcentaje o soles
    simbolo = "%" if tipo == "Porcentaje" else "S/"
    valor = pedir_monto(f"Valor del descuento ({simbolo}): ")
    motivo = pedir_texto("Motivo o descripción: ")

    nuevo_descuento = {
        "id_descuento": generar_id(descuentos, "id_descuento"),
        "nombre": nombre,
        "motivo": motivo,
        "tipo": tipo,
        "valor": valor,
        "aplica_a": "Cargo oficial",
        "estado": "Activo"
    }

    descuentos.append(nuevo_descuento)
    guardar_json(RUTA_DESCUENTOS, descuentos)

    print("\nDescuento/convenio creado correctamente.")
    print("Este descuento solo aplica a cargos oficiales.")