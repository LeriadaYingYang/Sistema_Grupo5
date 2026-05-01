from basedatos_json import leer_json, guardar_json, generar_id

# ruta donde se guardan las carreras
RUTA = "datos/carreras.json"

def registrar_carrera():# función para registrar una carrera en JSON.

    print("\n====================================")
    print("        REGISTRAR NUEVA CARRERA")
    print("====================================")

    carreras = leer_json(RUTA)    # carga carreras existentes

    # salones Pide datos al usuario
    nombre = input("Nombre de la carrera: ")
    descripcion = input("Descripción: ")

    # Validar que sea número
    while True:
        try:
            duracion = int(input("Duración en meses: "))
            break
        except:
            print("Error: ingrese un número válido")

    nueva_carrera = {    #  crear nueva carrera
        "id_carrera": generar_id(carreras, "id_carrera"),
        "nombre": nombre,
        "descripcion": descripcion,
        "duracion_meses": duracion,
        "estado": "Activo"
    }

    carreras.append(nueva_carrera)    # agregar a la lista

    guardar_json(RUTA, carreras)    # guardar en JSON

    print("\nCarrera registrada correctamente")
    print(f"ID generado: {nueva_carrera['id_carrera']}")
    input()
