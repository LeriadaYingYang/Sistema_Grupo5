from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, validar_no_vacio

RUTA_ALUMNOS = "datos/alumnos.json"

def _dni_ya_existe(alumnos, dni):  # verifica si el dni ya está registrado en un alumno activo
    return any(a["dni"] == dni and a["estado"] == "Activo" for a in alumnos)

def _pedir_campo(prompt, nombre_campo):  # solicita un campo de texto validando que no esté vacío
    while True:
        valor = input(prompt).strip()
        if validar_no_vacio(valor, nombre_campo):
            return valor

def crear_alumno():  # registra un alumno con sus datos personales
    imprimir_titulo("REGISTRAR ALUMNOS")
    alumnos = leer_json(RUTA_ALUMNOS)  # carga los alumnos registrados

    nombres   = _pedir_campo("Nombres: ", "nombres")
    apellidos = _pedir_campo("Apellidos: ", "apellidos")

    dni = _pedir_campo("DNI: ", "dni")
    if _dni_ya_existe(alumnos, dni):
        print("Error: ya existe un alumno activo con ese DNI.")
        return

    correo  = _pedir_campo("Correo: ", "correo")
    celular = _pedir_campo("Celular: ", "celular")

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
