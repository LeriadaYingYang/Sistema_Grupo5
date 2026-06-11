from basedatos_json import leer_json, guardar_json
from control_academico.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"

def cargar_notas():
    return leer_json(RUTA_NOTAS)

def obtener_notas_activas(notas):
    return [nota for nota in notas
        if nota["estado"] == "Activo"]

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def buscar_registro(notas, id_registro):
    return next((nota for nota in notas
            if nota["id_registro_nota"] == id_registro and nota["estado"] == "Activo"),None)

def mostrar_registro(registro):
    print(f"\nID Registro: "
        f"{registro['id_registro_nota']}")
    print(f"Alumno: "
        f"{registro['nombre_alumno']}")
    print(f"Carrera ID: "
        f"{registro['id_carrera']}")
    print(f"Salón ID: "
        f"{registro['id_salon']}")
    print(f"Unidad ID: "
        f"{registro['id_unidad']}")
    print(f"Módulo ID: "
        f"{registro['id_modulo']}")
    print(f"Promedio: "
        f"{registro['promedio_modulo']}")

def mostrar_notas(registro):
    print("\n=== NOTAS REGISTRADAS ===")
    for nota in registro["notas"]:
        print(f"{nota['orden']}. "
            f"{nota['nombre_nota']} | "
            f"Nota: {nota['nota']}")

def recalcular_promedio(registro):
    notas = registro["notas"]
    if not notas:
        registro["promedio_modulo"] = 0
        return
    promedio = (sum(nota["nota"] for nota in notas)/ len(notas))
    registro["promedio_modulo"] = round(promedio,2)

def reordenar_notas(registro):
    for indice, nota in enumerate(registro["notas"],start=1):
        nota["orden"] = indice

def eliminar_nota_especifica(notas):
    imprimir_titulo("=== ELIMINAR NOTA ESPECÍFICA ===")
    id_registro = pedir_entero("Ingrese ID del registro: ")
    registro = buscar_registro(notas,id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    if not registro["notas"]:
        print("El registro no tiene notas.")
        return
    mostrar_registro(registro)
    mostrar_notas(registro)
    orden = pedir_entero("\nIngrese orden de la nota a eliminar: ")
    nota_encontrada = next(
        (nota for nota in registro["notas"]
            if nota["orden"] == orden),None)
    if nota_encontrada is None:
        print("Nota no encontrada.")
        return
    confirmacion = input(f"¿Eliminar "
        f"{nota_encontrada['nombre_nota']}? "
        f"(S/N): ").upper().strip()
    if confirmacion != "S":
        print("Operación cancelada.")
        return
    registro["notas"].remove(nota_encontrada)
    reordenar_notas(registro)
    recalcular_promedio(registro)
    guardar_json(RUTA_NOTAS,notas)
    print("\nNota eliminada correctamente.")

def eliminar_registro_completo(notas):
    imprimir_titulo("=== ELIMINAR REGISTRO COMPLETO ===")
    id_registro = pedir_entero("Ingrese ID del registro: ")
    registro = buscar_registro(notas,id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    mostrar_registro(registro)
    confirmacion = input(
        "\n¿Desea eliminar todo el registro? (S/N): ").upper().strip()
    if confirmacion != "S":
        print("Operación cancelada.")
        return
    registro["estado"] = "Inactivo"
    guardar_json(RUTA_NOTAS,notas)
    print("\nRegistro eliminado correctamente.")

def menu_eliminar_notas():
    notas = leer_json(RUTA_NOTAS)
    while True:
        imprimir_titulo("=== ELIMINAR NOTAS ===")
        print("1. Eliminar nota específica")
        print("2. Eliminar registro completo")
        print("3. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":eliminar_nota_especifica(notas)
        elif opcion == "2":eliminar_registro_completo(notas)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.")

def eliminar_notas():
    notas = cargar_notas()
    registros_activos = (obtener_notas_activas(notas))
    if not registros_activos:
        print("No existen notas registradas.")
        return
    menu_eliminar_notas(notas)