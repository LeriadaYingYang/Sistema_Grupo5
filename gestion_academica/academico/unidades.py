from basedatos_json import leer_json, guardar_json, generar_id
from gestion_academica.utilidades import imprimir_titulo

RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_UNIDADES = "datos/unidades.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_carreras_desde_salones(salones):  #muestra las carreras disponibles a partir de los salones
    imprimir_titulo("CARRERAS DISPONIBLES")
    carreras_mostradas = []  #almacena las carreras ya mostradas
    for salon in salones:
        if salon["estado"] == "Activo":
            carrera = {
                "id_carrera": salon["id_carrera"],
                "nombre_carrera": salon["nombre_carrera"]}
            if carrera not in carreras_mostradas:
                carreras_mostradas.append(carrera)
                print(
                    f"ID: {carrera['id_carrera']} | "
                    f"Carrera: {carrera['nombre_carrera']}")

def mostrar_plantillas_por_carrera(plantillas, id_carrera):  #muestra las plantillas de una carrera
    imprimir_titulo("PLANTILLA DE LA CARRERA")
    encontrados = 0  #cuenta cuántas plantillas fueron encontradas
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            encontrados += 1
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")
    if encontrados == 0:
        print("No hay plantillas para esta carrera.")

def salon_ya_tiene_unidades(unidades, id_salon, id_plantilla):  #verifica si un salón ya tiene unidades registradas
    for unidad in unidades:
        if (unidad["estado"] == "Activo"
            and unidad.get("id_salon") == id_salon
            and unidad.get("id_plantilla") == id_plantilla):
            return True
    return False

def mostrar_salones_disponibles(salones,unidades,id_carrera,id_plantilla):  #muestra los salones que aún no tienen unidades registradas
    imprimir_titulo("SALONES DISPONIBLES SIN UNIDADES")
    encontrados = 0  #cuenta cuántos salones están disponibles
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            if not salon_ya_tiene_unidades(
                unidades,
                salon["id_salon"],
                id_plantilla):
                encontrados += 1
                print(
                    f"ID: {salon['id_salon']} | "
                    f"Salón: {salon['nombre_salon']} | "
                    f"Turno: {salon['turno']}")
    if encontrados == 0:
        print("No hay salones disponibles. "
            "Todos ya tienen unidades para esta plantilla.")

def registrar_unidad():  #registra unidades o ciclos para un salón y plantilla
    imprimir_titulo("REGISTRAR UNIDADES / CICLOS")
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    unidades = leer_json(RUTA_UNIDADES)  #carga las unidades registradas
    if len(salones) == 0: #valida si existen salones
        print("Primero debe registrar salones.")
        return
    if len(plantillas) == 0:  #valida si existen plantillas
        print("Primero debe crear una plantilla académica.")
        return
    mostrar_carreras_desde_salones(salones)  #muestra las carreras disponibles
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))  #solicita el id de la carrera
    except ValueError:
        print("Debe ingresar un número.")
        return
    mostrar_plantillas_por_carrera(plantillas,id_carrera)  #muestra las plantillas de la carrera
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))  #solicita el id de la plantilla
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas,"id_plantilla",id_plantilla)  # busca la plantilla seleccionada
    if plantilla is None or plantilla["id_carrera"] != id_carrera:
        print("Plantilla no válida para esta carrera.")
        return
    mostrar_salones_disponibles(salones,unidades,id_carrera,id_plantilla)  #muestra los salones disponibles
    try:
        id_salon = int(input("\nIngrese ID del salón: "))  #solicita el id del salón
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones,"id_salon",id_salon)  #busca el salón seleccionado
    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido para esta carrera.")
        return
    if salon_ya_tiene_unidades(unidades, id_salon, id_plantilla):
        print("Este salón ya tiene unidades creadas para esta plantilla.")
        return
    while True:  #solicita la cantidad de unidades a registrar
        try:
            cantidad = int(input("¿Cuántas unidades/ciclos desea crear?: "))
            if cantidad > 0:
                break
            print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")
    for i in range(1, cantidad + 1):  #registra las unidades indicadas
        print(f"\n--- UNIDAD/CICLO {i} ---")
        nombre_unidad = input("Nombre de la unidad/ciclo: ")
        descripcion = input("Descripción: ")
        nueva_unidad = {
            "id_unidad": generar_id(unidades, "id_unidad"),
            "id_salon": salon["id_salon"],
            "nombre_salon": salon["nombre_salon"],
            "turno": salon["turno"],
            "id_plantilla": plantilla["id_plantilla"],
            "id_carrera": salon["id_carrera"],
            "nombre_carrera": salon["nombre_carrera"],
            "nombre_plantilla": plantilla["nombre_plantilla"],
            "nombre_unidad": nombre_unidad,
            "descripcion": descripcion,
            "orden": i,
            "estado": "Activo"}
        unidades.append(nueva_unidad)  #agrega la unidad a la lista
        print(f"Unidad agregada: {nombre_unidad}")
    guardar_json(RUTA_UNIDADES,unidades)  # guarda las unidades en el archivo json
    print("\nUnidades/ciclos registrados correctamente.")

def ver_unidades():  #muestra las unidades registradas
    imprimir_titulo("VER UNIDADES / CICLOS")
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    unidades = leer_json(RUTA_UNIDADES)  #carga las unidades registradas
    if len(salones) == 0:
        print("No hay salones registrados.")
        return
    if len(unidades) == 0:
        print("No hay unidades registradas.")
        return
    mostrar_carreras_desde_salones(salones)  #muestra las carreras disponibles
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    mostrar_plantillas_por_carrera(plantillas,id_carrera)  # muestra las plantillas de la carrera
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas,"id_plantilla",id_plantilla)  # busca la plantilla seleccionada
    if plantilla is None or plantilla["id_carrera"] != id_carrera:
        print("Plantilla no válida.")
        return
    imprimir_titulo("SALONES DE LA CARRERA")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Turno: {salon['turno']}")
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones,"id_salon",id_salon)  # busca el salón seleccionado
    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido.")
        return
    imprimir_titulo("UNIDADES DEL SALON Y PLANTILLA")
    encontrados = 0  #cuenta las unidades encontradas
    for unidad in unidades:
        if (unidad["estado"] == "Activo"
            and unidad.get("id_salon") == id_salon
            and unidad.get("id_plantilla") == id_plantilla):
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {unidad['id_unidad']}")
            print(f"Carrera: {unidad['nombre_carrera']}")
            print(f"Plantilla: {unidad['nombre_plantilla']}")
            print(f"Salón: {unidad['nombre_salon']}")
            print(f"Turno: {unidad['turno']}")
            print(f"Unidad: {unidad['nombre_unidad']}")
            print(f"Orden: {unidad['orden']}")
            print(f"Descripción: {unidad['descripcion']}")
    input()  #pausa la pantalla antes de volver al menú
    if encontrados == 0:
        print("No hay unidades para este salón y plantilla.")