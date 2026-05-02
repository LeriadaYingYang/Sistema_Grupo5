from basedatos_json import leer_json, guardar_json, generar_id

RUTA_ALUMNOS = "datos/alumnos.json"


def crear_alumno():#registra un alumno con sus datos personales.

    print("\n====================================")
    print("          REGISTRAR ALUMNO")
    print("====================================")

    alumnos = leer_json(RUTA_ALUMNOS)

    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    dni = input("DNI: ")
    correo = input("Correo: ")
    celular = input("Celular: ")

    nuevo_alumno = {
        "id_alumno": generar_id(alumnos, "id_alumno"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"
    }

    alumnos.append(nuevo_alumno)
    guardar_json(RUTA_ALUMNOS, alumnos)

    print("\nAlumno registrado correctamente.")
    print(f"ID alumno generado: {nuevo_alumno['id_alumno']}")