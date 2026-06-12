from basedatos_json import leer_json, guardar_json
from director.utilidades import imprimir_titulo, pedir_entero

RUTA_ALUMNOS = "datos/alumnos.json"

CAMPOS_EDITABLES = [  # Organizacion de los campos que es posible editar
    ("Nombres",   "nombres"),
    ("Apellidos", "apellidos"),
    ("DNI",       "dni"),
    ("Correo",    "correo"),
    ("Celular",   "celular"),
]

def _mostrar_alumno(alumno):  # muestra los datos principales de un alumno
    print("\n-----------------------------")
    print(f"ID      : {alumno['id_alumno']}")
    print(f"Nombres : {alumno['nombres']}")
    print(f"Apellidos: {alumno['apellidos']}")
    print(f"DNI     : {alumno['dni']}")
    print(f"Correo  : {alumno['correo']}")
    print(f"Celular : {alumno['celular']}")

def _buscar_alumnos(alumnos, por_dni=False):  # busca alumnos activos por nombre/apellido o por DNI exacto
    if por_dni:
        valor = input("Ingrese DNI: ")
        return [a for a in alumnos if a["estado"] == "Activo" and a["dni"] == valor]
    else:
        texto = input("Ingrese nombre o apellido aproximado: ").lower()
        return [
            a for a in alumnos
            if a["estado"] == "Activo"
            and texto in f"{a['nombres']} {a['apellidos']}".lower()
        ]

def _elegir_alumno(encontrados):  # muestra los resultados y permite seleccionar uno por ID
    if not encontrados:
        print("No se encontraron alumnos.")
        return None

    imprimir_titulo("ALUMNOS ENCONTRADOS")
    for alumno in encontrados:
        _mostrar_alumno(alumno)

    id_alumno = pedir_entero("\nIngrese el ID del alumno que desea editar: ")
    if id_alumno is None:
        return None

    alumno = next((a for a in encontrados if a["id_alumno"] == id_alumno), None)
    if alumno is None:
        print("ID no válido.")
    return alumno

def _dni_duplicado(alumnos, nuevo_dni, id_alumno_actual):  # verifica si el dni ya pertenece a otro alumno activo
    return any(
        a["dni"] == nuevo_dni and a["estado"] == "Activo" and a["id_alumno"] != id_alumno_actual
        for a in alumnos
    )

def _editar_campo(alumno, alumnos):  # presenta el menú de edición y aplica los cambios al alumno
    while True:
        print(f"\nAlumno: {alumno['nombres']} {alumno['apellidos']} (ID: {alumno['id_alumno']})")
        print("\n¿Qué dato desea editar?")
        for idx, (etiqueta, clave) in enumerate(CAMPOS_EDITABLES, start=1):
            print(f"{idx}. {etiqueta:<10}: {alumno[clave]}")
        print(f"{len(CAMPOS_EDITABLES) + 1}. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == str(len(CAMPOS_EDITABLES) + 1):
            break

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(CAMPOS_EDITABLES)):
            print("Opción inválida.")
            continue

        etiqueta, clave = CAMPOS_EDITABLES[int(opcion) - 1]
        nuevo_valor = input(f"Nuevo {etiqueta.lower()}: ").strip()

        if not nuevo_valor:
            print(f"Error: el campo '{etiqueta}' no puede estar vacío.")
            continue

        if clave == "dni" and _dni_duplicado(alumnos, nuevo_valor, alumno["id_alumno"]):
            print("Error: ese DNI ya pertenece a otro alumno activo.")
            continue

        alumno[clave] = nuevo_valor
        print(f"{etiqueta} actualizado correctamente.")

        if input("¿Desea cambiar otro dato? (si/no): ").strip().lower() != "si":
            break

def editar_alumno():  # permite buscar y editar los datos de un alumno
    imprimir_titulo("EDITAR DATOS DE ALUMNO")
    alumnos = leer_json(RUTA_ALUMNOS)  # carga los alumnos registrados

    if not alumnos:
        print("No hay alumnos registrados.")
        return

    print("\nBuscar alumno por:\n1. Nombre o apellido\n2. DNI\n3. Volver")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        encontrados = _buscar_alumnos(alumnos, por_dni=False)
    elif opcion == "2":
        encontrados = _buscar_alumnos(alumnos, por_dni=True)
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")
        return

    alumno = _elegir_alumno(encontrados)
    if alumno is None:
        return

    _editar_campo(alumno, alumnos)
    guardar_json(RUTA_ALUMNOS, alumnos)  # guarda los cambios en el archivo json
    print("\nAlumno actualizado correctamente.")
