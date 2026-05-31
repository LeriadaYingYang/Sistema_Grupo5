from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

#===========================================
# Archivo: crear_profesor.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

RUTA_PROFESORES = "datos/profesores.json"

def crear_profesor():  #Registra un nuevo profesor y guarda sus datos personales en el sistema
    imprimir_titulo("REGISTRAR PROFESOR")
    profesores = leer_json(RUTA_PROFESORES)  #Carga la lista actual de profesores registrados
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

    profesores.append(nuevo_profesor)  # Agrega el nuevo profesor a la lista de registros
    guardar_json(RUTA_PROFESORES, profesores)  # Guarda el nuevo registro en el archivo json
    print("\nProfesor registrado correctamente.")
    print(f"ID profesor generado: {nuevo_profesor['id_profesor']}")