import re
from datetime import datetime
# Importaciones originales (asumimos que existen en tu proyecto)
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, pausa

# =============================================================================
# ── 1. FUNCIONES DE VALIDACIÓN REUTILIZABLES (Para todo el sistema) ──────────
# =============================================================================

def pedir_dni(mensaje="Ingrese DNI: "):
    """Valida que el DNI tenga exactamente 8 dígitos, sin letras ni espacios."""
    while True:
        dni = input(mensaje).strip()
        if re.fullmatch(r'\d{8}', dni):
            return dni
        print("Error: El DNI debe contener exactamente 8 números.")

def pedir_nombres(mensaje="Ingrese nombres/apellidos: "):
    """Valida letras y espacios, no permite vacío y devuelve formato Título."""
    while True:
        texto = input(mensaje).strip()
        # Solo permite letras (incluyendo acentos y ñ) y espacios
        if re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+', texto):
            # Elimina espacios múltiples entre palabras y pone mayúscula inicial
            return ' '.join(texto.split()).title()
        print("Error: Solo se permiten letras y espacios. No puede estar vacío.")

def pedir_correo(mensaje="Ingrese correo electrónico: "):
    """Valida formato estándar de correo usando expresiones regulares."""
    while True:
        correo = input(mensaje).strip()
        # Patrón básico para validar estructura local@dominio.extensión
        if re.fullmatch(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', correo):
            return correo
        print("Error: Formato de correo inválido. Ejemplo válido: usuario@dominio.com")

def pedir_contrasena(mensaje="Ingrese contraseña: "):
    """Valida mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula y 1 número."""
    while True:
        pwd = input(mensaje).strip()
        if len(pwd) >= 8 and re.search(r'[A-Z]', pwd) and re.search(r'[a-z]', pwd) and re.search(r'\d', pwd):
            return pwd
        print("Error: La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.")

def pedir_telefono(mensaje="Ingrese teléfono: "):
    """Valida que el teléfono tenga exactamente 9 dígitos."""
    while True:
        tel = input(mensaje).strip()
        if re.fullmatch(r'\d{9}', tel):
            return tel
        print("Error: El teléfono debe contener exactamente 9 números.")

def pedir_edad(mensaje="Ingrese edad: "):
    """Valida que sea un entero positivo en un rango lógico (1-120)."""
    while True:
        try:
            edad = int(input(mensaje).strip())
            if 1 <= edad <= 120:
                return edad
            print("Error: La edad debe estar entre 1 y 120 años.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def pedir_fecha(mensaje="Ingrese fecha (DD/MM/AAAA): "):
    """Valida que el formato sea correcto y la fecha exista en el calendario."""
    while True:
        fecha_str = input(mensaje).strip()
        try:
            # Si la conversión es exitosa, la fecha es real y válida
            fecha_valida = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            return fecha_valida.strftime("%d/%m/%Y")
        except ValueError:
            print("Error: Formato inválido o fecha inexistente. Use DD/MM/AAAA.")

def pedir_id_entero(mensaje="Ingrese ID: "):
    """Valida que el ID ingresado sea un número entero, eliminando espacios."""
    while True:
        try:
            valor = input(mensaje).strip()
            if not valor:
                print("Error: El campo no puede estar vacío.")
                continue
            return int(valor)
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def pedir_opcion_menu(mensaje, opciones_validas):
    """Valida que la entrada sea un entero y se encuentre en la lista de opciones."""
    while True:
        try:
            opcion = int(input(mensaje).strip())
            if opcion in opciones_validas:
                return opcion
            print(f"Error: Opción inválida. Elija una opción entre: {opciones_validas}")
        except ValueError:
            print("Error: Ingrese un número entero válido.")


# =============================================================================
# ── 2. FUNCIONES AUXILIARES (Específicas del módulo de notas) ────────────────
# =============================================================================

# Rutas de archivos JSON
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_TABLILLAS = "datos/tablillas_notas.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_NOTAS = "datos/notas_alumnos.json"

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item.get("estado") == "Activo":
            return item
    return None

def obtener_tablilla(tablillas, id_unidad, id_modulo):
    for t in tablillas:
        if (t["id_unidad"] == id_unidad and t["id_modulo"] == id_modulo and t["estado"] == "Activo"):
            return t
    return None

def buscar_nota_existente(notas, id_alumno, id_unidad, id_modulo):
    for r in notas:
        if (r["id_alumno"] == id_alumno and r["id_unidad"] == id_unidad and r["id_modulo"] == id_modulo and r["estado"] == "Activo"):
            return r
    return None

def calcular_promedio(lista_notas):
    validas = [n["nota"] for n in lista_notas if n["nota"] != ""]
    if not validas:
        return None
    return round(sum(validas) / len(validas), 2)

def obtener_condicion(promedio):
    if promedio is None:
        return "Sin promedio"
    if promedio >= 18: return "A - Excelente"
    elif promedio >= 15: return "B - Bueno"
    elif promedio >= 13: return "C - Regular"
    elif promedio >= 11: return "D - Deficiente"
    else: return "DESAPROBADO"

def pedir_nota(nombre_nota):
    """Solicita y valida una nota flotante entre 0 y 20."""
    while True:
        try:
            # Eliminamos espacios en blanco
            entrada = input(f"  Nota para '{nombre_nota}' (0-20): ").strip()
            if not entrada:
                print("Error: La nota no puede estar vacía.")
                continue

            nota = float(entrada)
            if 0 <= nota <= 20:
                return nota
            print("Error: La nota debe estar en un rango de 0 a 20.")
        except ValueError:
            print("Error: Ingrese un número válido (ej. 15 o 15.5).")

def crear_registro_notas(notas_guardadas, alumno, unidad, modulo, tablilla):
    entradas = [{"orden": n["orden"], "nombre_nota": n["nombre_nota"], "nota": ""} for n in tablilla["notas"]]
    nuevo = {
        "id_registro_nota": generar_id(notas_guardadas, "id_registro_nota"),
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": f"{alumno['nombres']} {alumno['apellidos']}",
        "id_carrera": unidad["id_carrera"],
        "id_salon": unidad["id_salon"],
        "id_unidad": unidad["id_unidad"],
        "id_modulo": modulo["id_modulo"],
        "notas": entradas,
        "promedio_modulo": None,
        "estado": "Activo"
    }
    notas_guardadas.append(nuevo)
    return nuevo


# =============================================================================
# ── 3. FUNCIÓN PRINCIPAL (Refactorizada) ─────────────────────────────────────
# =============================================================================

def registrar_notas_profesor(profesor):
    imprimir_titulo("REGISTRAR NOTAS")

    profesores_salones = leer_json(RUTA_PROFESORES_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)
    tablillas = leer_json(RUTA_TABLILLAS)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    notas = leer_json(RUTA_NOTAS)

    # 1. Salones del profesor
    salones_profesor = [ps for ps in profesores_salones if ps["id_profesor"] == profesor["id_profesor"] and ps["estado"] == "Activo"]
    if not salones_profesor:
        print("\nNo tiene salones asignados para registrar notas.")
        pausa()
        return

    # 2. Seleccionar salón
    imprimir_titulo("SUS SALONES")
    for ps in salones_profesor:
        print(f"  ID Salón: {ps['id_salon']} | {ps['nombre_salon']} | {ps['nombre_carrera']} | Turno: {ps['turno']}")

    # Uso de la función validadora de enteros para IDs
    id_salon = pedir_id_entero("\nIngrese ID del salón: ")
    salon_elegido = next((ps for ps in salones_profesor if ps["id_salon"] == id_salon), None)

    if salon_elegido is None:
        print("Error: Salón no encontrado o no asignado a usted.")
        pausa()
        return

    # 3. Seleccionar unidad del salón
    unidades_salon = [u for u in unidades if u["id_salon"] == id_salon and u["estado"] == "Activo"]
    if not unidades_salon:
        print("\nNo hay unidades registradas en este salón.")
        pausa()
        return

    imprimir_titulo("UNIDADES DISPONIBLES")
    for u in unidades_salon:
        print(f"  ID: {u['id_unidad']} | {u['nombre_unidad']}")

    try:
        id_unidad = int(input("\nIngrese ID de la unidad: "))
    except ValueError:
        print("ID inválido.")
        pausa()
        return

    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)
    if unidad is None or unidad["id_salon"] != id_salon:
        print("Unidad no encontrada en este salón.")
        pausa()
        return

    # 4. Seleccionar módulo
    modulos_unidad = [
        m for m in modulos
        if m["id_unidad"] == id_unidad and m["estado"] == "Activo"
    ]

    if not modulos_unidad:
        print("\nNo hay módulos registrados en esta unidad.")
        pausa()
        return

    imprimir_titulo("MÓDULOS DE LA UNIDAD")
    for m in sorted(modulos_unidad, key=lambda x: x.get("orden", 0)):
        print(f"  ID: {m['id_modulo']} | Módulo {m['orden']}: {m['nombre_modulo']}")

    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("ID inválido.")
        pausa()
        return

    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)
    if modulo is None or modulo["id_unidad"] != id_unidad:
        print("Módulo no encontrado en esta unidad.")
        pausa()
        return

    # 5. Verificar tablilla
    tablilla = obtener_tablilla(tablillas, id_unidad, id_modulo)
    if tablilla is None:
        print("\nNo existe tablilla de notas para este módulo.")
        print("Solicite al director que cree la tablilla primero.")
        pausa()
        return

    # 6. Seleccionar alumno
    alumnos_salon = [
        a for a in asignaciones
        if a["id_salon"] == id_salon and a["estado"] == "Activo"
    ]

    if not alumnos_salon:
        print("\nNo hay alumnos inscritos en este salón.")
        pausa()
        return

    imprimir_titulo("ALUMNOS DEL SALÓN")
    for a in alumnos_salon:
        print(f"  ID: {a['id_alumno']} | {a['nombre_alumno']} | DNI: {a['dni']}")

    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
    except ValueError:
        print("ID inválido.")
        pausa()
        return

    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no encontrado.")
        pausa()
        return

    # Verificar que el alumno pertenece al salón
    en_salon = any(a["id_alumno"] == id_alumno and a["id_salon"] == id_salon for a in alumnos_salon)
    if not en_salon:
        print("El alumno no está inscrito en este salón.")
        pausa()
        return

    # 7. Obtener o crear registro de notas
    registro = buscar_nota_existente(notas, id_alumno, id_unidad, id_modulo)
    if registro is None:
        registro = crear_registro_notas(notas, alumno, unidad, modulo, tablilla)
        print(f"\nSe creó un registro nuevo para {alumno['nombres']} {alumno['apellidos']}.")

    # 8. Ingresar notas en bucle
    while True:
        imprimir_titulo(f"NOTAS - {alumno['nombres']} {alumno['apellidos']}")
        print(f"  Módulo: {modulo['nombre_modulo']} | Unidad: {unidad['nombre_unidad']}\n")

        for nota in registro["notas"]:
            valor = nota["nota"] if nota["nota"] != "" else "Sin nota"
            print(f"  {nota['orden']}. {nota['nombre_nota']:<25} -> {valor}")

        prom_actual = registro.get("promedio_modulo")
        if prom_actual is not None:
            print(f"\n  Promedio actual: {prom_actual} | {obtener_condicion(prom_actual)}")
        else:
            print("\n  Promedio actual: Pendiente")

        print("\n  0. Guardar y salir")

        try:
            orden = int(input("\n  Seleccione número de nota a ingresar/modificar: "))
        except ValueError:
            print("  Ingrese un número válido.")
            continue

        if orden == 0:
            # Guardar
            registro["promedio_modulo"] = calcular_promedio(registro["notas"])
            guardar_json(RUTA_NOTAS, notas)
            print(f"\n  Notas guardadas correctamente.")
            if registro["promedio_modulo"] is not None:
                print(f"  Promedio final: {registro['promedio_modulo']} | {obtener_condicion(registro['promedio_modulo'])}")
            pausa()
            break

        nota_obj = next((n for n in registro["notas"] if n["orden"] == orden), None)
        if nota_obj is None:
            print("  Número de nota inválido.")
            continue

        nota_obj["nota"] = pedir_nota(nota_obj["nombre_nota"])
        registro["promedio_modulo"] = calcular_promedio(registro["notas"])
        guardar_json(RUTA_NOTAS, notas)
        print(f"  ✓ Nota guardada. Promedio actualizado: {registro['promedio_modulo']}")