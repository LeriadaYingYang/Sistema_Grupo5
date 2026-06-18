from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


def convertir_hora(hora):
    if hora is None:
        return None
    try:
        hora = str(hora).strip().lower()
        if not hora:
            return None
        if ":" in hora:
            return datetime.strptime(hora, "%H:%M")
        if "a" in hora:
            inicio = hora.split("a")[0].strip()
            if inicio.isdigit():
                valor = int(inicio)
                if 0 <= valor <= 23:
                    return datetime.strptime(f"{valor:02d}:00","%H:%M")
        if hora.isdigit():
            valor = int(hora)
            if 0 <= valor <= 23:
                return datetime.strptime(f"{valor:02d}:00","%H:%M")
    except ValueError:
        return None
    return None


def calcular_horas_programadas(horarios):
    if not isinstance(horarios, list):
        return 0
    total = 0
    for horario in horarios:
        if not isinstance(horario, dict):
            continue
        if horario.get("estado") != "Activo":
            continue
        dias_horas = horario.get("dias_horas", [])
        if not isinstance(dias_horas, list):
            continue
        for dia in dias_horas:
            if not isinstance(dia, dict):
                continue
            inicio = convertir_hora(dia.get("hora_inicio"))
            fin = convertir_hora(dia.get("hora_fin"))
            if inicio is None or fin is None:
                continue
            horas = (fin - inicio).total_seconds() / 3600
            if horas > 0:
                total += horas
    return round(total, 2)


def control_carga_horaria():
    imprimir_titulo("CONTROL DE CARGA HORARIA DOCENTE")
    try:
        profesores = leer_json(RUTA_PROFESORES)
        asistencias = leer_json(RUTA_ASISTENCIA)
        horarios = leer_json(RUTA_HORARIOS)
    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
        return
    except PermissionError as e:
        print(f"Sin permisos para acceder: {e}")
        return
    except Exception as e:
        print(f"Error al leer archivos: {e}")
        return
    if not isinstance(profesores, list):
        print("Error: profesores.json debe contener una lista.")
        return
    if not isinstance(asistencias, list):
        print("Advertencia: asistencia inválida.")
        asistencias = []
    if not isinstance(horarios, list):
        print("Advertencia: horarios inválidos.")
        horarios = []


    profesores_activos = []
    for profesor in profesores:
        if not isinstance(profesor, dict):
            continue
        if profesor.get("estado") != "Activo":
            continue
        if "id_profesor" not in profesor:
            continue
        profesores_activos.append(profesor)
    if not profesores_activos:
        print("No existen profesores activos.")
        return

    print("\nPROFESORES")
    ids_mostrados = set()
    for profesor in profesores_activos:
        id_profesor = profesor.get("id_profesor")
        if id_profesor in ids_mostrados:
            continue
        ids_mostrados.add(id_profesor)
        print(f"{id_profesor} - "
            f"{profesor.get('nombres', '')} "
            f"{profesor.get('apellidos', '')}")


    while True:
        id_ingresado = input("\nIngrese ID del profesor: ").strip()
        if not id_ingresado:
            print("El ID no puede estar vacío.")
            continue
        if not id_ingresado.isdigit():
            print("Debe ingresar un número entero.")
            continue
        id_profesor = int(id_ingresado)
        existe = any(p.get("id_profesor") == id_profesor for p in profesores_activos)
        if not existe:
            print("El ID no existe.")
            continue
        break
    profesor = next(
        (p for p in profesores_activos if p.get("id_profesor") == id_profesor),None)
    if profesor is None:
        print("Profesor no encontrado.")
        return


    horas_trabajadas = 0
    for asistencia in asistencias:
        if not isinstance(asistencia,dict):
            continue
        if (asistencia.get("id_profesor")!= id_profesor):
            continue
        try:
            horas = float(asistencia.get("horas_trabajadas",0))
            if horas < 0:
                continue
            horas_trabajadas += horas
        except (ValueError,TypeError):
            continue

    try:
        horas_programadas = (calcular_horas_programadas(horarios))
        if not isinstance(horas_programadas,(int, float)):
            horas_programadas = 0
        if horas_programadas < 0:
            horas_programadas = 0
    except Exception as e:
        print(f"Error al calcular horas programadas: {e}")
        return

    if horas_programadas > 0:
        cumplimiento = round(
            (horas_trabajadas/ horas_programadas) * 100,2)
    else:
        cumplimiento = 0

    imprimir_titulo("RESULTADO")
    nombre = (f"{profesor.get('nombres', '')} "
        f"{profesor.get('apellidos', '')}").strip()
    print(f"\nProfesor: {nombre}")
    print(f"Horas programadas: "
        f"{horas_programadas:.2f}")
    print(f"Horas trabajadas: "
        f"{horas_trabajadas:.2f}")
    print(f"Cumplimiento: "
        f"{cumplimiento:.2f}%")
    if cumplimiento >= 90:
        print("Estado: Excelente")
    elif cumplimiento >= 70:
        print("Estado: Bueno")
    else:
        print("Estado: Bajo")