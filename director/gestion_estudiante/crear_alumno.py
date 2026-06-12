from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, validar_no_vacio

RUTA_ALUMNOS = "datos/alumnos.json"

def _dni_ya_existe(alumnos, dni):  # verifica si el dni ya está registrado en un alumno activo
    return any(a["dni"] == dni and a["estado"] == "Activo" for a in alumnos)

def _validar_dni(dni):  # valida que el dni tenga exactamente 8 dígitos numéricos
    if not dni.isdigit():
        print("Error: el DNI solo debe contener números.")
        return False
    if len(dni) != 8:
        print("Error: el DNI debe tener exactamente 8 dígitos.")
        return False
    return True

def _validar_celular(celular):  # valida que el celular tenga exactamente 9 dígitos numéricos
    if not celular.isdigit():
        print("Error: el celular solo debe contener números.")
        return False
    if len(celular) != 9:
        print("Error: el celular debe tener exactamente 9 dígitos.")
        return False
    return True

def _validar_gmail(correo):  # valida que el correo tenga formato ...@gmail.com
    if not correo.endswith("@gmail.com"):
        print("Error: el correo debe tener formato ejemplo@gmail.com")
        return False
    parte_local = correo[: -len("@gmail.com")]
    if not parte_local:
        print("Error: el correo no puede estar vacío antes del @.")
        return False
    return True

def _pedir_campo(prompt, nombre_campo):  # solicita un campo de texto validando que no esté vacío
    while True:
        valor = input(prompt).strip()
        if validar_no_vacio(valor, nombre_campo):
            return valor

def _pedir_campo_validado(prompt, nombre_campo, fn_validar):  # solicita un campo y aplica una validación adicional, reintentando si falla
    while True:
        valor = input(prompt).strip()
        if not validar_no_vacio(valor, nombre_campo):
            continue
        if fn_validar(valor):
            return valor

def crear_alumno():  # registra un alumno con sus datos personales
    imprimir_titulo("REGISTRAR ALUMNOS")
    alumnos = leer_json(RUTA_ALUMNOS)  # carga los alumnos registrados

    nombres   = _pedir_campo("Nombres: ", "nombres")
    apellidos = _pedir_campo("Apellidos: ", "apellidos")

    dni = _pedir_campo_validado("DNI: ", "dni", _validar_dni)
    if _dni_ya_existe(alumnos, dni):
        print("Error: ya existe un alumno activo con ese DNI.")
        return

    correo  = _pedir_campo_validado("Correo (ejemplo@gmail.com): ", "correo", _validar_gmail)
    celular = _pedir_campo_validado("Celular: ", "celular", _validar_celular)

    nuevo_alumno = {  # crea el diccionario con los datos del nuevo alumno
        "id_alumno": generar_id(alumnos, "id_alumno"),
        "nombres":   nombres,
        "apellidos": apellidos,
        "dni":       dni,
        "correo":    correo,
        "celular":   celular,
        "estado":    "Activo",
    }

    alumnos.append(nuevo_alumno)  # agrega el alumno a la lista
    guardar_json(RUTA_ALUMNOS, alumnos)  # guarda la lista actualizada en el archivo json

    print(f"\nAlumno registrado correctamente.")
    print(f"ID alumno generado: {nuevo_alumno['id_alumno']}")
