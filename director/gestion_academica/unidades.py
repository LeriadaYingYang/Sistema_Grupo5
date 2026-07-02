from database.basedatos import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"

def leer_texto(mensaje):  #valida que el texto no esté vacío
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Este campo no puede estar vacío.")

def leer_entero_positivo(mensaje):  #valida que el número sea entero positivo
    while True:
        try:
            numero = int(input(mensaje))
            if numero > 0:
                return numero
            print("El número debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None
def mostrar_modulos(modulos):  #muestra todos los módulos activos
    imprimir_titulo("MÓDULOS DISPONIBLES")
    encontrados = 0

    for modulo in modulos:
        if modulo["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {modulo['id_modulo']} | "
                f"Módulo: {modulo['nombre_modulo']} | "
                f"Salón: {modulo['nombre_salon']}"
            )

    return encontrados
def mostrar_unidades(unidades):  #muestra las unidades activas
    imprimir_titulo("UNIDADES DISPONIBLES")
    encontrados = 0

    for unidad in unidades:
        if unidad.get("estado") == "Activo":
            encontrados += 1
            print(
                f"ID: {unidad.get('id_unidad', 'Sin ID')} | "
                f"Unidad: {unidad.get('nombre_unidad', 'Sin nombre')} | "
                f"Módulo: {unidad.get('nombre_modulo', 'Sin módulo')}"
            )

    return encontrados

def leer_entero_no_negativo(mensaje):  #permite ingresar 0 para volver
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= 0:
                return numero
            print("El número debe ser 0 o mayor.")
        except ValueError:
            print("Ingrese un número válido.")

def registrar_unidad():  #crea una unidad para un módulo
    imprimir_titulo("CREAR UNIDAD")

    modulos = leer_json(RUTA_MODULOS)
    unidades = leer_json(RUTA_UNIDADES)

    if len(modulos) == 0:
        print("Primero debe registrar módulos.")
        input()
        return

    if mostrar_modulos(modulos) == 0:
        print("No hay módulos activos.")
        input()
        return

    id_modulo = leer_entero_positivo("\nIngrese ID del módulo: ")
    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    if modulo is None:
        print("Módulo no encontrado.")
        input()
        return

    nombre_unidad = leer_texto("Nombre de la unidad: ")

    for unidad in unidades:
        if (
            unidad["estado"] == "Activo"
            and unidad["id_modulo"] == id_modulo
            and unidad["nombre_unidad"].lower() == nombre_unidad.lower()
        ):
            print("Ya existe una unidad activa con ese nombre en este módulo.")
            input()
            return

    descripcion = leer_texto("Descripción: ")

    nueva_unidad = {
        "id_unidad": generar_id(unidades, "id_unidad"),
        "id_modulo": modulo["id_modulo"],
        "nombre_modulo": modulo["nombre_modulo"],
        "id_salon": modulo["id_salon"],
        "nombre_salon": modulo["nombre_salon"],
        "turno": modulo["turno"],
        "id_plantilla": modulo["id_plantilla"],
        "nombre_plantilla": modulo["nombre_plantilla"],
        "id_carrera": modulo["id_carrera"],
        "nombre_carrera": modulo["nombre_carrera"],
        "nombre_unidad": nombre_unidad,
        "descripcion": descripcion,
        "estado": "Activo"
    }

    unidades.append(nueva_unidad)

    guardar_json(RUTA_UNIDADES, unidades)

    print("\nUnidad registrada correctamente.")
    print(f"ID generado: {nueva_unidad['id_unidad']}")
    input()

def editar_unidad():  #edita una unidad registrada por opciones
    imprimir_titulo("EDITAR UNIDAD")

    unidades = leer_json(RUTA_UNIDADES)
    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return
    if mostrar_unidades(unidades) == 0:
        print("No hay unidades activas para editar.")
        input()
        return

    id_unidad = leer_entero_positivo("\nIngrese ID de la unidad: ")
    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)

    if unidad is None:
        print("Unidad no encontrada.")
        input()
        return
    while True:
        imprimir_titulo("DATOS DE LA UNIDAD")
        print(f"ID: {unidad.get('id_unidad', 'Sin ID')}")
        print(f"Carrera: {unidad.get('nombre_carrera', 'Sin carrera')}")
        print(f"Plantilla: {unidad.get('nombre_plantilla', 'Sin plantilla')}")
        print(f"Salón: {unidad.get('nombre_salon', 'Sin salón')}")
        print(f"Módulo: {unidad.get('nombre_modulo', 'Sin módulo')}")
        print(f"Unidad: {unidad.get('nombre_unidad', 'Sin nombre')}")
        print(f"Descripción: {unidad.get('descripcion', 'Sin descripción')}")

        print("\n¿Qué desea editar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Guardar y volver")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            unidad["nombre_unidad"] = leer_texto("Nuevo nombre de la unidad: ")
            print("Nombre actualizado correctamente.")
        elif opcion == "2":
            unidad["descripcion"] = leer_texto("Nueva descripción: ")
            print("Descripción actualizada correctamente.")
        elif opcion == "3":
            guardar_json(RUTA_UNIDADES, unidades)
            print("\nUnidad actualizada correctamente.")
            input()
            break
        else:
            print("Opción inválida.")

def asignar_unidad_salon():  #mantiene compatibilidad con el menú anterior
    print("La unidad ahora se asigna directamente al módulo al momento de crearla.")
    input()

def ver_unidades():  #muestra las unidades registradas
    imprimir_titulo("VER UNIDADES")

    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return

    encontrados = 0

    for unidad in unidades:
        if unidad.get("estado") == "Activo":
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {unidad.get('id_unidad', 'Sin ID')}")
            print(f"Carrera: {unidad.get('nombre_carrera', 'Sin carrera')}")
            print(f"Plantilla: {unidad.get('nombre_plantilla', 'Sin plantilla')}")
            print(f"Salón: {unidad.get('nombre_salon', 'Sin salón')}")
            print(f"Módulo: {unidad.get('nombre_modulo', 'Sin módulo')}")
            print(f"Unidad: {unidad.get('nombre_unidad', 'Sin nombre')}")
            print(f"Descripción: {unidad.get('descripcion', 'Sin descripción')}")

    if encontrados == 0:
        print("No hay unidades activas.")

    input()

def desactivar_unidad():  #oculta una unidad activa
    imprimir_titulo("OCULTAR UNIDAD")
    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return
    while True:
        if mostrar_unidades(unidades) == 0:
            print("No hay unidades activas para ocultar.")
            input()
            return
        print("0. Volver")
        id_unidad = leer_entero_no_negativo("\nIngrese ID de la unidad a ocultar: ")

        if id_unidad == 0:
            break

        unidad = buscar_por_id(unidades, "id_unidad", id_unidad)

        if unidad is None:
            print("Unidad no encontrada.")
            continue

        confirmar = input(f"¿Desea ocultar {unidad['nombre_unidad']}? (s/n): ").lower()

        if confirmar == "s":
            unidad["estado"] = "Oculto"
            guardar_json(RUTA_UNIDADES, unidades)
            print("\nUnidad ocultada correctamente.")
            input()
            break
        print("Operación cancelada.")

def mostrar_unidades_ocultas():  #muestra las unidades ocultas
    unidades = leer_json(RUTA_UNIDADES)
    imprimir_titulo("UNIDADES OCULTAS")
    encontrados = 0

    for unidad in unidades:
        if unidad.get("estado") == "Oculto":
            encontrados += 1
            print(
                f"ID: {unidad.get('id_unidad', 'Sin ID')} | "
                f"Unidad: {unidad.get('nombre_unidad', 'Sin nombre')} | "
                f"Módulo: {unidad.get('nombre_modulo', 'Sin módulo')}"
            )

    return encontrados

def activar_unidad():  #activa una unidad oculta
    imprimir_titulo("ACTIVAR UNIDAD")

    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return

    while True:
        if mostrar_unidades_ocultas() == 0:
            print("No hay unidades ocultas para activar.")
            input()
            return

        print("0. Volver")
        id_unidad = leer_entero_no_negativo("\nIngrese ID de la unidad a activar: ")

        if id_unidad == 0:
            break

        unidad_encontrada = None

        for unidad in unidades:
            if (
                unidad.get("id_unidad") == id_unidad
                and unidad.get("estado") == "Oculto"
            ):
                unidad_encontrada = unidad
                break

        if unidad_encontrada is None:
            print("Unidad oculta no encontrada.")
            continue

        confirmar = input(
            f"¿Desea activar {unidad_encontrada.get('nombre_unidad', 'Sin nombre')}? (s/n): "
        ).lower()

        if confirmar == "s":
            unidad_encontrada["estado"] = "Activo"
            guardar_json(RUTA_UNIDADES, unidades)
            print("\nUnidad activada correctamente.")
            input()
            break

        print("Operación cancelada.")