from basedatos_json import leer_json, guardar_json, generar_id
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

def modulo_ya_tiene_unidad(unidades, id_modulo):  #verifica si el módulo ya tiene una unidad
    for unidad in unidades:
        if unidad["estado"] == "Activo" and unidad["id_modulo"] == id_modulo:
            return True
    return False

def mostrar_modulos_sin_unidad(modulos, unidades):  #muestra módulos que aún no tienen unidad
    imprimir_titulo("MÓDULOS DISPONIBLES SIN UNIDAD")
    encontrados = 0
    for modulo in modulos:
        if modulo["estado"] == "Activo":
            if not modulo_ya_tiene_unidad(unidades, modulo["id_modulo"]):
                encontrados += 1
                print(
                    f"ID: {modulo['id_modulo']} | "
                    f"Módulo: {modulo['nombre_modulo']} | "
                    f"Salón: {modulo['nombre_salon']}")
    if encontrados == 0:
        print("No hay módulos disponibles. Todos ya tienen unidad.")

    return encontrados

def mostrar_unidades(unidades):  #muestra las unidades activas
    imprimir_titulo("UNIDADES DISPONIBLES")
    encontrados = 0
    for unidad in unidades:
        if unidad["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {unidad['id_unidad']} | "
                f"Unidad: {unidad['nombre_unidad']} | "
                f"Módulo: {unidad['nombre_modulo']}")

    return encontrados

def registrar_unidad():  #crea una unidad para un módulo
    imprimir_titulo("CREAR UNIDAD")

    modulos = leer_json(RUTA_MODULOS)
    unidades = leer_json(RUTA_UNIDADES)

    if len(modulos) == 0:
        print("Primero debe registrar módulos.")
        input()
        return
    if mostrar_modulos_sin_unidad(modulos, unidades) == 0:
        input()
        return

    id_modulo = leer_entero_positivo("\nIngrese ID del módulo: ")
    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    if modulo is None:
        print("Módulo no encontrado.")
        input()
        return
    if modulo_ya_tiene_unidad(unidades, id_modulo):
        print("Este módulo ya tiene una unidad registrada.")
        input()
        return

    nombre_unidad = leer_texto("Nombre de la unidad: ")
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
        "estado": "Activo"}

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
        print(f"ID: {unidad['id_unidad']}")
        print(f"Carrera: {unidad['nombre_carrera']}")
        print(f"Plantilla: {unidad['nombre_plantilla']}")
        print(f"Salón: {unidad['nombre_salon']}")
        print(f"Módulo: {unidad['nombre_modulo']}")
        print(f"Unidad: {unidad['nombre_unidad']}")
        print(f"Descripción: {unidad['descripcion']}")

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
        if unidad["estado"] == "Activo":
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {unidad['id_unidad']}")
            print(f"Carrera: {unidad['nombre_carrera']}")
            print(f"Plantilla: {unidad['nombre_plantilla']}")
            print(f"Salón: {unidad['nombre_salon']}")
            print(f"Módulo: {unidad['nombre_modulo']}")
            print(f"Unidad: {unidad['nombre_unidad']}")
            print(f"Descripción: {unidad['descripcion']}")
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
        id_unidad = leer_entero_positivo("\nIngrese ID de la unidad a ocultar: ")

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