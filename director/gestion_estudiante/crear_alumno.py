from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, validar_no_vacio, pausa

RUTA_ALUMNOS = "datos/alumnos.json"

def _dni_ya_existe(alumnos, dni):
    return any(a["dni"] == dni and a["estado"] == "Activo" for a in alumnos)

def _validar_dni(dni):
    if not dni.isdigit():
        print("Error: el DNI solo debe contener números.")
        return False
    if len(dni) != 8:
        print("Error: el DNI debe tener exactamente 8 dígitos.")
        return False
    return True

def _validar_celular(celular):
    if not celular.isdigit():
        print("Error: el celular solo debe contener números.")
        return False
    if len(celular) != 9:
        print("Error: el celular debe tener exactamente 9 dígitos.")
        return False
    return True

def _validar_gmail(correo):
    if not correo.endswith("@gmail.com"):
        print("Error: el correo debe tener formato ejemplo@gmail.com")
        return False
    parte_local = correo[: -len("@gmail.com")]
    if not parte_local:
        print("Error: el correo no puede estar vacío antes del @.")
        return False
    return True

def _pedir_campo(prompt, nombre_campo):
    while True:
        valor = input(prompt).strip()
        if not validar_no_vacio(valor, nombre_campo):
            continue
        tiene_simbolos = False
        for c in valor:
            if not (c.isalpha() or c.isspace()):
                tiene_simbolos = True
                break
        if tiene_simbolos:
            print(f"Error: el campo '{nombre_campo}' solo debe contener letras.")
            continue
        return valor

def _pedir_campo_validado(prompt, nombre_campo, fn_validar):
    while True:
        valor = input(prompt).strip()
        if not validar_no_vacio(valor, nombre_campo):
            continue
        if fn_validar(valor):
            return valor

def crear_alumno():
    print("--- NUEVO REGISTRO DE ALUMNO ---")
    print("Complete los siguientes datos del alumno.\n")
    pausa()
    imprimir_titulo("REGISTRAR ALUMNOS")
    alumnos = leer_json(RUTA_ALUMNOS)

    nombres   = _pedir_campo("Nombres: ", "nombres")
    apellidos = _pedir_campo("Apellidos: ", "apellidos")

    dni = _pedir_campo_validado("DNI: ", "dni", _validar_dni)
    if _dni_ya_existe(alumnos, dni):
        print("Error: ya existe un alumno activo con ese DNI.")
        pausa()
        return

    correo  = _pedir_campo_validado("Correo (ejemplo@gmail.com): ", "correo", _validar_gmail)
    celular = _pedir_campo_validado("Celular: ", "celular", _validar_celular)

    nuevo_alumno = {
        "id_alumno": generar_id(alumnos, "id_alumno"),
        "nombres":   nombres,
        "apellidos": apellidos,
        "dni":       dni,
        "correo":    correo,
        "celular":   celular,
        "estado":    "Activo",
    }

    alumnos.append(nuevo_alumno)
    guardar_json(RUTA_ALUMNOS, alumnos)

    print(f"\nAlumno registrado correctamente.")
    print(f"ID alumno generado: {nuevo_alumno['id_alumno']}")
    pausa()
