import re
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"


# ==========================================
# FUNCIONES REUTILIZABLES DE VALIDACIÓN
# ==========================================

def solicitar_nombre_apellido(mensaje):
    """
    Solicita nombres o apellidos.
    Solo permite letras (incluyendo tildes y ñ) y espacios.
    Capitaliza la primera letra de cada palabra (.title()) y elimina espacios extra.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: Este campo no puede estar vacío.")
            continue
        if len(dato) > 60:
            print(" Error: El texto es demasiado largo (máximo 60 caracteres).")
            continue
        # Expresión regular: solo letras y espacios intermedios
        if re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", dato):
            # Formatea con la primera letra de cada palabra en mayúscula
            return dato.title()
        print(" Error: Solo se permiten letras y espacios. Sin números ni caracteres especiales.")


def solicitar_dni(profesores, mensaje):
    """
    Solicita un DNI de exactamente 8 dígitos numéricos.
    No permite espacios, letras, caracteres especiales ni duplicados.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: El DNI no puede estar vacío.")
            continue
        # Expresión regular: exactamente 8 dígitos numéricos del 0 al 9
        if not re.fullmatch(r"\d{8}", dato):
            print(" Error: El DNI debe contener exactamente 8 dígitos numéricos, sin letras ni espacios.")
            continue
        # Validación de duplicidad
        if existe_dni(profesores, dato):
            print(" Error: Ya existe un profesor registrado con ese DNI. Ingrese otro.")
            continue
        return dato


def solicitar_correo(mensaje):
    """
    Solicita un correo electrónico con formato válido empleando expresiones regulares.
    Asegura la presencia de '@' y un dominio, rechazando espacios.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: El correo electrónico no puede estar vacío.")
            continue
        # Expresión regular estándar para correos electrónicos
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.fullmatch(patron, dato):
            return dato.lower()  # Se almacena en minúsculas por buena práctica
        print(" Error: Formato de correo inválido (ejemplo: usuario@dominio.com). No incluya espacios.")


def solicitar_celular(mensaje):
    """
    Solicita un número telefónico/celular de exactamente 9 dígitos.
    Solo permite números, sin espacios ni caracteres especiales.
    """
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print(" Error: El celular no puede estar vacío.")
            continue
        # Expresión regular: exactamente 9 dígitos numéricos
        if re.fullmatch(r"\d{9}", dato):
            return dato
        print(" Error: El celular debe contener exactamente 9 dígitos numéricos.")


# ==========================================
# FUNCIONES LÓGICAS DEL SISTEMA
# ==========================================

def existe_dni(profesores, dni):
    """Verifica si el DNI ya está registrado en la lista."""
    return any(
        profesor.get("dni") == dni
        for profesor in profesores
    )


def crear_profesor():
    """Registra un nuevo profesor en el sistema aplicando validaciones robustas."""
    imprimir_titulo("REGISTRAR PROFESOR")

    # Carga de la base de datos JSON
    profesores = leer_json(RUTA_PROFESORES)

    # El uso de las nuevas funciones garantiza que el flujo no continúe con datos corruptos
    # ni requiera salir prematuramente con 'return' ante equivocaciones del usuario.
    nombres = solicitar_nombre_apellido("Nombres: ")
    apellidos = solicitar_nombre_apellido("Apellidos: ")
    
    # Pasamos la lista 'profesores' para verificar la duplicidad del DNI inmediatamente
    dni = solicitar_dni(profesores, "DNI: ")
    
    correo = solicitar_correo("Correo: ")
    celular = solicitar_celular("Celular: ")

    # Construcción del diccionario del nuevo profesor con datos limpios y validados
    nuevo_profesor = {
        "id_profesor": generar_id(profesores, "id_profesor"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"
    }

    # Adjuntar y guardar en persistencia JSON
    profesores.append(nuevo_profesor)
    guardar_json(RUTA_PROFESORES, profesores)

    print("\n Profesor registrado correctamente.")
    print(f"ID profesor generado: {nuevo_profesor['id_profesor']}")