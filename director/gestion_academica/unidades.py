from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"

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
                    f"Salón: {modulo['nombre_salon']}"
                )

    if encontrados == 0:
        print("No hay módulos disponibles. Todos ya tienen unidad.")

def mostrar_unidades(unidades):  #muestra las unidades activas
    imprimir_titulo("UNIDADES DISPONIBLES")

    for unidad in unidades:
        if unidad["estado"] == "Activo":
            print(
                f"ID: {unidad['id_unidad']} | "
                f"Unidad: {unidad['nombre_unidad']} | "
                f"Módulo: {unidad['nombre_modulo']}")

def registrar_unidad():  #crea una unidad para un módulo
    imprimir_titulo("CREAR UNIDAD")

    modulos = leer_json(RUTA_MODULOS)
    unidades = leer_json(RUTA_UNIDADES)

    if len(modulos) == 0:
        print("Primero debe registrar módulos.")
        input()
        return

    mostrar_modulos_sin_unidad(modulos, unidades)

    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    if modulo is None:
        print("Módulo no encontrado.")
        input()
        return

    if modulo_ya_tiene_unidad(unidades, id_modulo):
        print("Este módulo ya tiene una unidad registrada.")
        input()
        return

    nombre_unidad = input("Nombre de la unidad: ")
    descripcion = input("Descripción: ")

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

def editar_unidad():  #edita una unidad registrada
    imprimir_titulo("EDITAR UNIDAD")

    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return

    mostrar_unidades(unidades)

    try:
        id_unidad = int(input("\nIngrese ID de la unidad: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for unidad in unidades:
        if unidad["id_unidad"] == id_unidad and unidad["estado"] == "Activo":
            nuevo_nombre = input(f"Nombre ({unidad['nombre_unidad']}): ").strip()
            nueva_descripcion = input(f"Descripción ({unidad['descripcion']}): ").strip()

            if nuevo_nombre:
                unidad["nombre_unidad"] = nuevo_nombre

            if nueva_descripcion:
                unidad["descripcion"] = nueva_descripcion

            guardar_json(RUTA_UNIDADES, unidades)

            print("\nUnidad actualizada correctamente.")
            input()
            return

    print("Unidad no encontrada.")
    input()

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

    for unidad in unidades:
        if unidad["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {unidad['id_unidad']}")
            print(f"Carrera: {unidad['nombre_carrera']}")
            print(f"Plantilla: {unidad['nombre_plantilla']}")
            print(f"Salón: {unidad['nombre_salon']}")
            print(f"Módulo: {unidad['nombre_modulo']}")
            print(f"Unidad: {unidad['nombre_unidad']}")
            print(f"Descripción: {unidad['descripcion']}")

    input()

def desactivar_unidad():  #desactiva una unidad
    imprimir_titulo("DESACTIVAR UNIDAD")

    unidades = leer_json(RUTA_UNIDADES)

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return

    mostrar_unidades(unidades)

    try:
        id_unidad = int(input("\nIngrese ID de la unidad: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for unidad in unidades:
        if unidad["id_unidad"] == id_unidad and unidad["estado"] == "Activo":
            unidad["estado"] = "Inactivo"

            guardar_json(RUTA_UNIDADES, unidades)

            print("\nUnidad desactivada correctamente.")
            input()
            return

    print("Unidad no encontrada.")
    input()