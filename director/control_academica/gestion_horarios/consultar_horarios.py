from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_HORARIOS = "datos/horarios.json"


def cargar_horarios():
    try:
        datos = leer_json(RUTA_HORARIOS)
        if not isinstance(datos,list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer horarios: {e}")
        return []


def consultar_horarios():
    imprimir_titulo("CONSULTAR HORARIOS")
    horarios = cargar_horarios()
    if not horarios:
        print("No existen horarios registrados.")
        return
    horarios_activos = [h for h in horarios
        if h.get("estado")== "Activo"]
    if not horarios_activos:
        print("No existen horarios activos.")
        return
    print("\n1. Ver todos")
    print("2. Filtrar por plantilla")
    print("3. Filtrar por carrera")
    print("4. Filtrar por salón")
    opcion = input("\nSeleccione opción: ").strip()

    if opcion == "1":
        mostrar_horarios(horarios_activos)

    elif opcion == "2":
        nombre = input("Nombre de plantilla: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrados = [
            h for h in horarios_activos
            if nombre in str(h.get("nombre_plantilla","")).lower()]
        mostrar_horarios(filtrados)

    elif opcion == "3":
        nombre = input("Nombre de carrera: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrados = [
            h for h in horarios_activos
            if nombre in str(h.get("nombre_carrera","")).lower()]
        mostrar_horarios(filtrados)

    elif opcion == "4":
        nombre = input("Nombre de salón: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrados = [
            h for h in horarios_activos
            if nombre in str(h.get("nombre_salon","")).lower()]
        mostrar_horarios(filtrados)
    else:
        print("Opción inválida.")


def mostrar_horarios(lista):
    imprimir_titulo("RESULTADOS")
    if not lista:
        print("No se encontraron registros.")
        return
    print(f"\nTotal encontrados: "
        f"{len(lista)}")
    for horario in lista:
        print(
            f"\nID Horario: "
            f"{horario.get('id_horario','N/A')}"
            f"\nPlantilla: "
            f"{horario.get('nombre_plantilla','N/A')}"
            f"\nCarrera: "
            f"{horario.get('nombre_carrera','N/A')}"
            f"\nSalón: "
            f"{horario.get('nombre_salon','N/A')}"
            f"\nTurno: "
            f"{horario.get('turno','N/A')}"
        )
        print("\nDÍAS Y HORARIOS:")
        dias_horas = horario.get("dias_horas",[])
        if not isinstance(dias_horas,list) or not dias_horas:
            print("No existen horarios registrados.")
        else:
            for dia in dias_horas:
                print(f"  {dia.get('orden','?')}. "
                    f"{dia.get('dia','N/A')} | "
                    f"{dia.get('hora_inicio','N/A')} - "
                    f"{dia.get('hora_fin','N/A')}")
        print("\n" + "-" * 40)