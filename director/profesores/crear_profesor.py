from basedatos_json import leer_json, guardar_json, generar_id

RUTA_PROFESORES = "datos/profesores.json"

def crear_profesor():#registra un nuevo profesor en el archivo profesores.json.

    print("\n====================================")
    print("        REGISTRAR PROFESOR")
    print("====================================")

    profesores = leer_json(RUTA_PROFESORES)

    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    dni = input("DNI: ")
    correo = input("Correo: ")
    celular = input("Celular: ")

    nuevo_profesor = {
        "id_profesor": generar_id(profesores, "id_profesor"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"}

    profesores.append(nuevo_profesor)
    guardar_json(RUTA_PROFESORES, profesores)

    print("\nProfesor registrado correctamente.")
    print(f"ID profesor generado: {nuevo_profesor['id_profesor']}")