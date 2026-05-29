from basedatos_json import leer_json, guardar_json, generar_id

RUTA_ALUMNOS = "datos/alumnos.json"

def crear_alumno():  #registra un alumno con sus datos personales
    print("\n--- REGISTRAR ALUMNO ---")
    alumnos = leer_json(RUTA_ALUMNOS)  #carga los alumnos registrados
    nombres = input("Nombres: ")  #solicita los nombres del alumno
    apellidos = input("Apellidos: ")  #solicita los apellidos del alumno
    dni = input("DNI: ")  #solicita el dni del alumno
    correo = input("Correo: ")  #solicita el correo del alumno
    celular = input("Celular: ")  #solicita el celular del alumno
    nuevo_alumno = {  #crea el diccionario con los datos del nuevo alumno
        "id_alumno": generar_id(alumnos, "id_alumno"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"}
    alumnos.append(nuevo_alumno)  # agrega el alumno a la lista
    guardar_json(RUTA_ALUMNOS,alumnos) # guarda la lista actualizada en el archivo json
    print("\nAlumno registrado correctamente.")
    print(f"ID alumno generado: {nuevo_alumno['id_alumno']}")