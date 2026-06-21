from datetime import datetime
from basedatos_json import leer_json,guardar_json
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


def validar_hora(hora):
    try:
        datetime.strptime(hora,"%H:%M")
        return True
    except ValueError:
        return False


def hora_fin_valida(hora_inicio,hora_fin):
    try:
        inicio = datetime.strptime(hora_inicio,"%H:%M")
        fin = datetime.strptime(hora_fin,"%H:%M")
        return fin > inicio
    except ValueError:
        return False


def buscar_por_id(lista,campo_id,valor_id):
    if not isinstance(lista,list):
        return None
    for item in lista:
        if (item.get(campo_id) == valor_id
            and item.get("estado") == "Activo"):
            return item
    return None


def mostrar_horarios(horarios):
    imprimir_titulo("HORARIOS DISPONIBLES")
    encontrados = 0
    for horario in horarios:
        if horario.get("estado") == "Activo":
            encontrados += 1
            print(
                f"ID Horario: "
                f"{horario.get('id_horario','N/A')} | "
                f"Plantilla: "
                f"{horario.get('nombre_plantilla','N/A')} | "
                f"Carrera: "
                f"{horario.get('nombre_carrera','N/A')} | "
                f"Salón: "
                f"{horario.get('nombre_salon','N/A')} | "
                f"Turno: "
                f"{horario.get('turno','N/A')}"
            )
    if encontrados == 0:
        print("No existen horarios activos.")


def mostrar_detalle_horario(horario):
    imprimir_titulo("DETALLE DEL HORARIO")
    dias_horas = horario.get("dias_horas",[])
    if not dias_horas:
        print("No existen días configurados.")
        return
    for dia in dias_horas:
        print(
            f"{dia.get('orden','?')}. "
            f"{dia.get('dia','N/A')} | "
            f"{dia.get('hora_inicio','N/A')} - "
            f"{dia.get('hora_fin','N/A')}"
        )


def modificar_horarios():
    imprimir_titulo("MODIFICAR HORARIOS")
    horarios = cargar_horarios()
    if not horarios:
        print("No existen horarios registrados.")
        return
    horarios_activos = [
        h for h in horarios
        if h.get("estado") == "Activo"]
    if not horarios_activos:
        print("No existen horarios activos.")
        return
    mostrar_horarios(horarios_activos)
    id_horario = validar_entero("\nIngrese ID del horario: ")
    horario = buscar_por_id(horarios,"id_horario",id_horario)
    if horario is None:
        print("Horario no encontrado.")
        return
    while True:
        mostrar_detalle_horario(horario)
        print("\nOPCIONES")
        print("1. Modificar día")
        print("2. Modificar hora inicio")
        print("3. Modificar hora fin")
        print("4. Guardar cambios")
        print("5. Cancelar")
        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            orden = validar_entero("Número de día a modificar: ")
            encontrado = False
            for dia in horario.get("dias_horas",[]):
                if dia.get("orden") == orden:
                    while True:
                        nuevo_dia = input("Nuevo nombre del día: ").strip().title()
                        if not nuevo_dia:
                            print("El nombre del día no puede estar vacío.")
                            continue
                        dia["dia"] = nuevo_dia
                        print("Día actualizado correctamente.")
                        encontrado = True
                        break
                    break
            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "2":
            orden = validar_entero("Número de día a modificar: ")
            encontrado = False
            for dia in horario.get("dias_horas",[]):
                if dia.get("orden") == orden:
                    while True:
                        nueva_hora = input("Nueva hora inicio (HH:MM): ").strip()
                        if not validar_hora(nueva_hora):
                            print("Formato inválido.")
                            continue
                        if not hora_fin_valida(
                            nueva_hora,
                            dia.get("hora_fin","00:00")):
                            print("La hora inicio debe ser menor que la hora fin.")
                            continue
                        dia["hora_inicio"] = nueva_hora
                        print("Hora inicio actualizada.")
                        encontrado = True
                        break
                    break
            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "3":
            orden = validar_entero("Número de día a modificar: ")
            encontrado = False
            for dia in horario.get("dias_horas",[]):
                if dia.get("orden") == orden:
                    while True:
                        nueva_hora = input("Nueva hora fin (HH:MM): ").strip()
                        if not validar_hora(nueva_hora):
                            print("Formato inválido.")
                            continue
                        if not hora_fin_valida(
                            dia.get("hora_inicio","00:00"),nueva_hora):
                            print("La hora fin debe ser mayor que la hora inicio.")
                            continue
                        dia["hora_fin"] = nueva_hora
                        print("Hora fin actualizada.")
                        encontrado = True
                        break
                    break
            if not encontrado:
                print("Día no encontrado.")

        elif opcion == "4":
            try:
                guardar_json(RUTA_HORARIOS,horarios)
                print("\nHorario modificado correctamente.")
                break
            except Exception as e:
                print(f"Error al guardar: {e}")

        elif opcion == "5":
            print("\nOperación cancelada.")
            break
        else:
            print("Opción inválida.")