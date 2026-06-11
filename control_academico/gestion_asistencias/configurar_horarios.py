from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id
from control_academico.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"

DIAS_VALIDOS = ["Lunes", "Martes", "Miércoles",
    "Jueves", "Viernes", "Sábado", "Domingo"]

def cargar_datos():
    return (leer_json(RUTA_PLANTILLAS), leer_json(RUTA_CARRERAS),
        leer_json(RUTA_SALONES), leer_json(RUTA_HORARIOS))

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def buscar_por_id(lista, campo_id, valor_id):
    return next((item for item in lista
            if item[campo_id] == valor_id and item["estado"] == "Activo"), None)

def validar_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

def pedir_hora(mensaje):
    while True:
        hora = input(mensaje).strip()
        if validar_hora(hora):
            return hora
        print("Formato inválido. Use HH:MM.")

def horario_valido(hora_inicio, hora_fin):
    inicio = datetime.strptime(hora_inicio, "%H:%M")
    fin = datetime.strptime(hora_fin, "%H:%M")
    return fin > inicio

def pedir_dia():
    while True:
        dia = input("Día: ").strip().capitalize()
        if dia in DIAS_VALIDOS:
            return dia
        print("Día inválido.")

def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")

def mostrar_carrera(carreras, id_carrera):
    imprimir_titulo("CARRERA DE LA PLANTILLA")
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera:
        print(f"ID: {carrera['id_carrera']} | "
            f"{carrera['nombre']}")

def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES DE LA CARRERA")
    salones_filtrados = [salon for salon in salones
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera]
    if not salones_filtrados:
        print("No hay salones registrados para esta carrera.")
        return
    for salon in salones_filtrados:
        print(f"ID: {salon['id_salon']} | "
            f"Salón: {salon['nombre_salon']} | "
            f"Turno: {salon['turno']}")

def horario_ya_existe(horarios, id_plantilla, id_salon):
    return any(horario["estado"] == "Activo" and horario["id_plantilla"] == id_plantilla and horario["id_salon"] == id_salon for horario in horarios)

def pedir_detalle_horario():
    dias_horas = []
    dias_registrados = set()
    cantidad = pedir_entero("¿Cuántos días tendrá el horario?: ")
    while cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        cantidad = pedir_entero("¿Cuántos días tendrá el horario?: ")
    for i in range(1, cantidad + 1):
        print(f"\n=== DÍA {i} ===")
        while True:
            dia = pedir_dia()
            if dia not in dias_registrados:
                dias_registrados.add(dia)
                break
            print("Ese día ya fue registrado.")
        while True:
            hora_inicio = pedir_hora("Hora de inicio (HH:MM): ")
            hora_fin = pedir_hora("Hora de salida (HH:MM): ")
            if horario_valido(hora_inicio, hora_fin):
                break
            print("La hora de salida debe ser mayor que la hora de inicio.")
        dias_horas.append({"orden": i, "dia": dia, "hora_inicio": hora_inicio, "hora_fin": hora_fin})
    return dias_horas

def crear_horario(horarios, plantilla, carrera, salon, dias_horas):
    return {"id_horario": generar_id(horarios,"id_horario"),
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"], "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"], "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"], "turno": salon["turno"], "dias_horas": dias_horas,"estado": "Activo"}

def configurar_horarios():
    imprimir_titulo("=== CONFIGURAR HORARIOS ===")
    (plantillas,carreras,salones,horarios) = cargar_datos()
    if not plantillas:
        print("Primero debe crear plantillas académicas.")
        return
    if not salones:
        print("Primero debe registrar salones.")
        return
    mostrar_plantillas(plantillas)
    id_plantilla = pedir_entero("\nIngrese ID de plantilla: ")
    plantilla = buscar_por_id(plantillas,"id_plantilla",id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return
    mostrar_carrera(carreras,plantilla["id_carrera"])
    id_carrera = pedir_entero("\nIngrese ID de carrera: ")
    if id_carrera != plantilla["id_carrera"]:
        print("La carrera no pertenece a la plantilla seleccionada.")
        return
    carrera = buscar_por_id(carreras,"id_carrera",id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        return
    mostrar_salones(salones,id_carrera)
    id_salon = pedir_entero("\nIngrese ID del salón: ")
    salon = buscar_por_id(salones,"id_salon",id_salon)
    if (salon is None or salon["id_carrera"] != id_carrera):
        print("Salón no válido.")
        return
    if horario_ya_existe(horarios,id_plantilla,id_salon):
        print("Este salón ya tiene horario configurado para esta plantilla.")
        return
    dias_horas = pedir_detalle_horario()
    nuevo_horario = crear_horario(horarios,plantilla,carrera,salon,dias_horas)
    horarios.append(nuevo_horario)
    guardar_json(RUTA_HORARIOS,horarios)
    print("\nHorario configurado correctamente.")