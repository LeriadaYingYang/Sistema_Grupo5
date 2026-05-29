from basedatos_json import leer_json, guardar_json, generar_id

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):  #muestra las plantillas disponibles
    print("\n--- PLANTILLAS DISPONIBLES ---")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(f"ID: {plantilla['id_plantilla']} | Carrera: {plantilla['nombre_carrera']} | Plantilla: {plantilla['nombre_plantilla']}")

def mostrar_carreras(carreras, id_carrera_plantilla):  #muestra la carrera de la plantilla
    print("\n--- CARRERA DE LA PLANTILLA ---")
    for carrera in carreras:
        if carrera["estado"] == "Activo" and carrera["id_carrera"] == id_carrera_plantilla:
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones de la carrera
    print("\n--- SALONES DE LA CARRERA ---")
    encontrados = 0
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            encontrados += 1
            print(f"ID: {salon['id_salon']} | Salón: {salon['nombre_salon']} | Turno: {salon['turno']}")
    if encontrados == 0:
        print("No hay salones registrados para esta carrera.")

def horario_ya_existe(horarios, id_plantilla, id_salon):  #verifica si ya existe un horario
    for horario in horarios:
        if (horario["estado"] == "Activo"
            and horario["id_plantilla"] == id_plantilla
            and horario["id_salon"] == id_salon):
            return True
    return False

def pedir_detalle_horario():  #solicita los días y horarios
    dias_horas = []
    while True:
        try:
            cantidad = int(input("¿Cuántos días tendrá el horario?: "))
            if cantidad > 0:
                break
            print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")
    for i in range(1, cantidad + 1):
        print(f"\n--- DÍA {i} ---")
        dia = input("Día: ")
        hora_inicio = input("Hora de inicio (08:00): ")
        hora_fin = input("Hora de salida (12:00): ")
        dias_horas.append({
            "orden": i,
            "dia": dia,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin})
    return dias_horas

def configurar_horarios():  #configura horarios para una plantilla y salón
    print("\n--- CONFIGURAR HORARIOS ---")
    plantillas = leer_json(RUTA_PLANTILLAS)
    carreras = leer_json(RUTA_CARRERAS)
    salones = leer_json(RUTA_SALONES)
    horarios = leer_json(RUTA_HORARIOS)
    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        return
    if len(salones) == 0:
        print("Primero debe registrar salones.")
        return
    mostrar_plantillas(plantillas)
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return
    mostrar_carreras(carreras, plantilla["id_carrera"])
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    if id_carrera != plantilla["id_carrera"]:
        print("La carrera no pertenece a la plantilla seleccionada.")
        return
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        return
    mostrar_salones(salones, id_carrera)
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido.")
        return
    if horario_ya_existe(horarios, id_plantilla, id_salon):
        print("Este salón ya tiene horario configurado para esta plantilla.")
        return
    dias_horas = pedir_detalle_horario()
    nuevo_horario = {
        "id_horario": generar_id(horarios, "id_horario"),
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "dias_horas": dias_horas,
        "estado": "Activo"}
    horarios.append(nuevo_horario)  #agrega el horario
    guardar_json(RUTA_HORARIOS, horarios)  #guarda el horario
    print("\nHorario configurado correctamente.")