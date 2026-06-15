from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"


def solicitar_texto(mensaje):
    """Solicita un texto no vacío."""
    dato = input(mensaje).strip()

    if dato == "":
        print("Este campo no puede estar vacío.")
        return None

    return dato


def existe_dni(profesores, dni):
    """Verifica si el DNI ya está registrado."""
    return any(
        profesor.get("dni") == dni
        for profesor in profesores
    )


def crear_profesor():
    """Registra un nuevo profesor."""
    imprimir_titulo("REGISTRAR PROFESOR")

    profesores = leer_json(RUTA_PROFESORES)

    nombres = solicitar_texto("Nombres: ")
    if nombres is None:
        return

    apellidos = solicitar_texto("Apellidos: ")
    if apellidos is None:
        return

    dni = solicitar_texto("DNI: ")
    if dni is None:
        return

    if not dni.isdigit() or len(dni) != 8:
        print("El DNI debe contener exactamente 8 dígitos.")
        return

    if existe_dni(profesores, dni):
        print("Ya existe un profesor registrado con ese DNI.")
        return

    correo = solicitar_texto("Correo: ")
    if correo is None:
        return

    celular = solicitar_texto("Celular: ")
    if celular is None:
        return

    if not celular.isdigit() or len(celular) != 9:
        print("El celular debe contener exactamente 9 dígitos.")
        return

    nuevo_profesor = {
        "id_profesor": generar_id(
            profesores,
            "id_profesor"
        ),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"
    }

    profesores.append(nuevo_profesor)

    guardar_json(
        RUTA_PROFESORES,
        profesores
    )

    print("\nProfesor registrado correctamente.")
    print(
        f"ID profesor generado: "
        f"{nuevo_profesor['id_profesor']}"
    )