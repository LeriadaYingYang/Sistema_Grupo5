from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def cargar_notas():
    try:
        datos = leer_json(RUTA_NOTAS)
        if not isinstance(datos, list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer las notas: {e}")
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


def convertir_float(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def ver_notas_unidad():
    imprimir_titulo("VER NOTAS POR UNIDAD")
    notas = cargar_notas()
    if not notas:
        print("No existen registros de notas.")
        return
    unidades = sorted(
        {nota.get("id_unidad")
            for nota in notas
            if (isinstance(nota, dict)
                and nota.get("estado") == "Activo"
                and nota.get("id_unidad") is not None)})
    if not unidades:
        print("No existen unidades con registros activos.")
        return
    print("\nUNIDADES DISPONIBLES")
    for unidad in unidades:
        print(f"Unidad ID: {unidad}")
    id_unidad = validar_entero("\nIngrese ID de la unidad: ")
    resultados = [
        nota for nota in notas
        if (isinstance(nota, dict)
            and nota.get("estado") == "Activo"
            and nota.get("id_unidad") == id_unidad)]
    if not resultados:
        print("No existen notas para esta unidad.")
        return
    imprimir_titulo("NOTAS DE LA UNIDAD")
    suma = 0
    cantidad = 0
    for registro in resultados:
        promedio = convertir_float(registro.get("promedio_modulo"))
        if promedio is None:
            continue
        suma += promedio
        cantidad += 1
        print(
            f"\nAlumno: "
            f"{registro.get('nombre_alumno', 'N/A')}"
            f"\nID Módulo: "
            f"{registro.get('id_modulo', 'N/A')}"
            f"\nPromedio: "
            f"{promedio}"
        )
        print("\nDETALLE DE ACTIVIDADES")
        grupos = registro.get("grupos",[])
        if not isinstance(grupos, list) or not grupos:
            print("Sin grupos registrados.")
        else:
            for grupo in grupos:
                if not isinstance(grupo, dict):
                    continue
                print(f"\nGrupo: "
                    f"{grupo.get('nombre_grupo', 'N/A')}")
                print(f"Promedio Grupo: "
                    f"{grupo.get('promedio_grupo', 'N/A')}")
                actividades = grupo.get("actividades",[])
                if (not isinstance(actividades,list)or not actividades):
                    print("Sin actividades registradas.")
                else:
                    for actividad in actividades:
                        if not isinstance(actividad,dict):
                            continue
                        print(f"  - "
                            f"{actividad.get('nombre_actividad', 'N/A')}: "
                            f"{actividad.get('nota', 'N/A')}")
        print("\n" + "-" * 40)
    if cantidad == 0:
        print("\nNo existen promedios válidos para calcular.")
        return
    promedio_general = round(suma / cantidad,2)
    print(f"\nPROMEDIO GENERAL DE LA UNIDAD: "
        f"{promedio_general}")
    print(f"TOTAL REGISTROS ANALIZADOS: "
        f"{cantidad}")