from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"

def crear_alumno():  #Registra un alumno con sus datos personales
    imprimir_titulo("=== REGISTRAR ALUMNOS ===")
    alumnos = leer_json(RUTA_ALUMNOS)  #Carga los alumnos registrados
    nombres = input("Nombres: ")  #Solicita los nombres del alumno
    apellidos = input("Apellidos: ")  #Solicita los apellidos del alumno
    dni = input("DNI: ")  #Solicita el DNI del alumno
    correo = input("Correo: ")  #Solicita el correo del alumno
    celular = input("Celular: ")  #Solicita el celular del alumno
    nuevo_alumno = {  #Crea el diccionario con los datos del nuevo alumno
        "id_alumno": generar_id(alumnos, "id_alumno"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"}
    alumnos.append(nuevo_alumno)  # Agrega el alumno a la lista
    guardar_json(RUTA_ALUMNOS,alumnos) # Guarda la lista actualizada en el archivo json
    print("\n=== ALUMNO REGISTRADO CORRECTAMENTE ===")
    print(f"ID alumno generado: {nuevo_alumno['id_alumno']}")