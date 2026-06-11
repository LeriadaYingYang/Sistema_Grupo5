from basedatos_json import leer_json, guardar_json
from control_academico.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"

NOTA_MINIMA = 0
NOTA_MAXIMA = 20

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

def pedir_nota():
    while True:
        try:
            nota = float(input("Ingrese nueva nota: "))
            if NOTA_MINIMA <= nota <= NOTA_MAXIMA:
                return nota
            print(f"La nota debe estar entre "
                f"{NOTA_MINIMA} y {NOTA_MAXIMA}.")
        except ValueError:
            print("Ingrese una nota válida.")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El valor no puede estar vacío.")

def buscar_registro(notas, id_registro):
    return next(
        (nota for nota in notas
            if nota["id_registro_nota"] == id_registro and nota["estado"] == "Activo"),None)

def mostrar_registro(registro):
    print(f"\nID Registro: "
        f"{registro['id_registro_nota']}")
    print(f"Alumno: "
        f"{registro['nombre_alumno']}")
    print(f"ID Carrera: "
        f"{registro['id_carrera']}")
    print(f"ID Salón: "
        f"{registro['id_salon']}")
    print(f"ID Unidad: "
        f"{registro['id_unidad']}")
    print(f"ID Módulo: "
        f"{registro['id_modulo']}")
    print(f"Promedio: "
        f"{registro['promedio_modulo']}")

def mostrar_notas(registro):
    print("\n=== NOTAS REGISTRADAS ===")
    for nota in registro["notas"]:
        print(f"{nota['orden']}. "
            f"{nota['nombre_nota']} | "
            f"{nota['nota']}")

def buscar_nota(registro, orden):
    return next(
        (nota
            for nota in registro["notas"]
            if nota["orden"] == orden),None)

def recalcular_promedio(registro):
    notas = registro["notas"]
    if not notas:
        registro["promedio_modulo"] = 0
        return
    promedio = (sum(nota["nota"] for nota in notas)/ len(notas))
    registro["promedio_modulo"] = round(promedio,2)

def guardar_cambios(notas):
    guardar_json(RUTA_NOTAS,notas)
    print("\nCambios guardados correctamente.")

def modificar_nota_especifica(notas):
    imprimir_titulo("=== MODIFICAR NOTA ===")
    id_registro = pedir_entero("Ingrese ID del registro: ")
    registro = buscar_registro(notas,id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    mostrar_registro(registro)
    mostrar_notas(registro)
    orden = pedir_entero("\nSeleccione orden de la nota: ")
    nota = buscar_nota(registro,orden)
    if nota is None:
        print("Nota no encontrada.")
        return
    print(f"\nNota actual: "
        f"{nota['nota']}")
    nota["nota"] = pedir_nota()
    recalcular_promedio(registro)
    guardar_cambios(notas)

def modificar_nombre_nota(notas):
    imprimir_titulo("=== MODIFICAR NOMBRE DE EVALUACIÓN ===")
    id_registro = pedir_entero("Ingrese ID del registro: ")
    registro = buscar_registro(notas,id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    mostrar_notas(registro)
    orden = pedir_entero("\nSeleccione orden de la nota: ")
    nota = buscar_nota(registro,orden)
    if nota is None:
        print("Nota no encontrada.")
        return
    print(f"\nNombre actual: "
        f"{nota['nombre_nota']}")
    nota["nombre_nota"] = pedir_texto("Nuevo nombre: ")
    guardar_cambios(notas)

def modificar_varias_notas(notas):
    imprimir_titulo("=== MODIFICAR VARIAS NOTAS ===")
    id_registro = pedir_entero("Ingrese ID del registro: ")
    registro = buscar_registro(notas,id_registro)
    if registro is None:
        print("Registro no encontrado.")
        return
    print(f"\nAlumno: "
        f"{registro['nombre_alumno']}")
    for nota in registro["notas"]:
        print(f"\n{nota['nombre_nota']}")
        print(f"Nota actual: "
            f"{nota['nota']}")
        nuevo_valor = input("Nueva nota (Enter para conservar): ").strip()
        if nuevo_valor == "":
            continue
        try:
            nueva_nota = float(nuevo_valor)
            if (NOTA_MINIMA<= nueva_nota<= NOTA_MAXIMA):
                nota["nota"] = nueva_nota
            else:
                print(f"Nota ignorada. "
                    f"Debe estar entre "
                    f"{NOTA_MINIMA} y "
                    f"{NOTA_MAXIMA}.")
        except ValueError:
            print("Valor inválido. Se conserva la nota.")
    recalcular_promedio(registro)
    guardar_cambios(notas)

def menu_modificar_notas():
    notas = leer_json(RUTA_NOTAS)
    while True:
        imprimir_titulo("=== MODIFICAR NOTAS ===")
        print("1. Modificar una nota específica")
        print("2. Modificar nombre de evaluación")
        print("3. Modificar varias notas")
        print("4. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":modificar_nota_especifica(notas)
        elif opcion == "2":modificar_nombre_nota(notas)
        elif opcion == "3":modificar_varias_notas(notas)
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

def modificar_notas():
    notas = cargar_notas()
    registros_activos = (obtener_notas_activas(notas))
    if not registros_activos:
        print("No existen notas registradas.")
        return
    menu_modificar_notas(notas)