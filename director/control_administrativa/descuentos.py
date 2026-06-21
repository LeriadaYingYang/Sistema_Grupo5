import re
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: el campo no puede estar vacío.")
        elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]{3,60}", texto):
            print("Error: use solo letras, números y espacios. No se permiten símbolos.")
        else:
            return texto

def pedir_texto_opcional(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return "Sin descripción"
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.]{3,100}", texto):
            print("Error: descripción inválida. Evite símbolos especiales.")
        else:
            return texto

def pedir_tipo_descuento():
    while True:
        print("""
--- TIPO DE DESCUENTO ---
1. Porcentaje
2. Monto fijo
""")
        opcion = input("Seleccione tipo: ").strip()
        if opcion == "1":
            return "Porcentaje"
        elif opcion == "2":
            return "Monto fijo"
        else:
            print("Opción inválida. Ingrese 1 o 2.")

def pedir_valor_descuento(tipo):
    while True:
        entrada = input("Valor del descuento: ").strip()
        if not re.fullmatch(r"\d+(\.\d{1,2})?", entrada):
            print("Error: ingrese solo números positivos. Ejemplo: 10 o 10.50")
            continue
        valor = float(entrada)
        if valor <= 0:
            print("Error: el valor debe ser mayor que 0.")
        elif tipo == "Porcentaje" and valor > 100:
            print("Error: el porcentaje no puede ser mayor a 100.")
        else:
            return round(valor, 2)

def descuento_ya_existe(descuentos, nombre):
    for descuento in descuentos:
        if descuento.get("estado") == "Activo" and descuento.get("nombre", "").lower() == nombre.lower():
            return True
    return False

def crear_descuento_convenio():
    imprimir_titulo("CREAR DESCUENTO O CONVENIO")
    descuentos = leer_json(RUTA_DESCUENTOS) or []

    nombre = pedir_texto("Nombre del descuento/convenio: ")
    if descuento_ya_existe(descuentos, nombre):
        print("Error: ya existe un descuento activo con ese nombre.")
        return

    tipo = pedir_tipo_descuento()
    valor = pedir_valor_descuento(tipo)
    motivo = pedir_texto_opcional("Motivo o descripción: ")

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
