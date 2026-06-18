from datetime import datetime
from basedatos_json import leer_json,guardar_json,generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"


def cargar_datos(ruta):
    try:
        datos = leer_json(ruta)
        if not isinstance(datos, list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer datos: {e}")
        return []


def validar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor <= 0:
                print("Debe ingresar un número mayor a cero.")
                continue
            return valor
        except ValueError:
            print("Ingrese un número válido.")


def validar_hora(hora):
    try:
        datetime.strptime(hora,"%H:%M")
        return True
    except ValueError:
        return False


def buscar_por_id(lista,campo_id,valor_id):
    if not isinstance(lista, list):
        return None
    for item in lista:
        if (item.get(campo_id) == valor_id
            and item.get("estado") == "Activo"):
            return item
    return None


def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    encontrados = 0
    for plantilla in plantillas:
        if plantilla.get("estado") == "Activo":
            encontrados += 1
            print(
                f"ID: "
                f"{plantilla.get('id_plantilla')} | "
                f"Carrera: "
                f"{plantilla.get('nombre_carrera','N/A')} | "
                f"Plantilla: "
                f"{plantilla.get('nombre_plantilla','N/A')}"
            )
    if encontrados == 0:
        print("No existen plantillas activas.")


def mostrar_carreras(carreras,id_carrera):
    imprimir_titulo("CARRERA")
    for carrera in carreras:
        if (carrera.get("estado") == "Activo"
            and carrera.get("id_carrera") == id_carrera):
            print(f"ID: "
                f"{carrera.get('id_carrera')} | "
                f"{carrera.get('nombre','N/A')}")


def mostrar_salones(salones,id_carrera):
    imprimir_titulo("SALONES DISPONIBLES")
    encontrados = 0
    for salon in salones:
        if (
            salon.get("estado") == "Activo"
            and salon.get("id_carrera") == id_carrera):
            encontrados += 1
            print(
                f"ID: "
                f"{salon.get('id_salon')} | "
                f"Salón: "
                f"{salon.get('nombre_salon','N/A')} | "
                f"Turno: "
                f"{salon.get('turno','N/A')}"
            )
    if encontrados == 0:
        print("No existen salones para esta carrera.")


def horario_ya_existe(horarios,id_plantilla,id_salon):
    for horario in horarios:
        if (
            horario.get("estado")== "Activo"
            and horario.get("id_plantilla")== id_plantilla
            and horario.get("id_salon")== id_salon):
            return True
    return False


def pedir_horarios():
    dias_horas = []
    dias_registrados = set()
    cantidad = validar_entero("¿Cuántos días tendrá el horario?: ")
    for i in range(1,cantidad + 1):
        print(f"\nDÍA {i}")
        while True:
            dia = input("Nombre del día: ").strip().title()
            if not dia:
                print("El día no puede estar vacío.")
                continue
            if dia in dias_registrados:
                print("Ese día ya fue registrado.")
                continue
            dias_registrados.add(dia)
            break
        while True:
            hora_inicio = input("Hora inicio (HH:MM): ").strip()
            if validar_hora(hora_inicio):
                break
            print("Formato inválido.")
        while True:
            hora_fin = input("Hora fin (HH:MM): ").strip()
            if not validar_hora(hora_fin):
                print("Formato inválido.")
                continue
            inicio = datetime.strptime(hora_inicio,"%H:%M")
            fin = datetime.strptime(hora_fin,"%H:%M")
            if fin <= inicio:
                print("La hora fin debe ser mayor que la hora inicio.")
                continue
            break
        dias_horas.append({"orden": i,"dia": dia,
            "hora_inicio":hora_inicio,"hora_fin":hora_fin})
    return dias_horas


def configurar_horarios():
    imprimir_titulo("CONFIGURAR HORARIOS")
    plantillas = cargar_datos(RUTA_PLANTILLAS)
    carreras = cargar_datos(RUTA_CARRERAS)
    salones = cargar_datos(RUTA_SALONES)
    horarios = cargar_datos(RUTA_HORARIOS)
    plantillas_activas = [
        p for p in plantillas
        if p.get("estado") == "Activo"]
    salones_activos = [s for s in salones
        if s.get("estado") == "Activo"]
    if not plantillas_activas:
        print("No existen plantillas activas.")
        return
    if not salones_activos:
        print("No existen salones activos.")
        return
    mostrar_plantillas(plantillas_activas)
    id_plantilla = validar_entero("\nIngrese ID de plantilla: ")
    plantilla = buscar_por_id(plantillas,"id_plantilla",id_plantilla)
    if plantilla is None:
        print("Plantilla no encontrada.")
        return
    mostrar_carreras(carreras,plantilla.get("id_carrera"))
    mostrar_salones(salones,plantilla.get("id_carrera"))
    id_salon = validar_entero("\nIngrese ID del salón: ")
    salon = buscar_por_id(salones,"id_salon",id_salon)
    if salon is None:
        print("Salón no encontrado.")
        return
    if (salon.get("id_carrera")!= plantilla.get("id_carrera")):
        print("El salón no pertenece a la carrera de la plantilla.")
        return
    if horario_ya_existe(horarios,id_plantilla,id_salon):
        print("Ya existe un horario para esta plantilla y salón.")
        return
    dias_horas = pedir_horarios()
    try:
        nuevo_horario = {
            "id_horario":generar_id(horarios,"id_horario"),
            "id_plantilla":plantilla.get("id_plantilla"),
            "nombre_plantilla":plantilla.get("nombre_plantilla"),
            "id_carrera":plantilla.get("id_carrera"),
            "nombre_carrera":plantilla.get("nombre_carrera"),
            "id_salon":salon.get("id_salon"),
            "nombre_salon":salon.get("nombre_salon"),
            "turno":salon.get("turno"),
            "dias_horas": dias_horas,
            "estado":"Activo"}
        horarios.append(nuevo_horario)
        guardar_json(RUTA_HORARIOS,horarios)
        print("\nHorario registrado correctamente.")
    except Exception as e:
        print(f"Error al guardar "
            f"el horario: {e}")