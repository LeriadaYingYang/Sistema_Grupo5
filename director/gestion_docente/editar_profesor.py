from basedatos_json import leer_json, guardar_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"


def mostrar_profesor(profesor):
    """Muestra la información de un profesor."""
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(f"Nombres: {profesor['nombres']}")
    print(f"Apellidos: {profesor['apellidos']}")
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")


def buscar_por_nombre(profesores):
    """Busca profesores activos por nombre o apellido."""
    texto = input(
        "Ingrese nombre o apellido aproximado: "
    ).strip().lower()

    return [
        profesor
        for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and texto in (
                f"{profesor['nombres']} "
                f"{profesor['apellidos']}"
            ).lower()
        )
    ]


def buscar_por_dni(profesores):
    """Busca profesores activos por DNI."""
    dni = input("Ingrese DNI: ").strip()

    return [
        profesor
        for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and profesor.get("dni") == dni
        )
    ]


def solicitar_id(mensaje):
    """Solicita un ID numérico."""
    try:
        return int(input(mensaje))
    except ValueError:
        print("Debe ingresar un número.")
        return None


def elegir_profesor(encontrados):
    """Permite seleccionar un profesor."""
    if not encontrados:
        print("No se encontraron profesores.")
        return None

    imprimir_titulo("PROFESORES ENCONTRADOS")

    for profesor in encontrados:
        mostrar_profesor(profesor)

    id_profesor = solicitar_id(
        "\nIngrese ID del profesor que desea editar: "
    )

    if id_profesor is None:
        return None

    for profesor in encontrados:
        if profesor["id_profesor"] == id_profesor:
            return profesor

    print("ID no válido.")
    return None


def dni_duplicado(profesores, dni, id_actual):
    """Verifica si el DNI pertenece a otro profesor."""
    return any(
        profesor.get("dni") == dni
        and profesor.get("id_profesor") != id_actual
        for profesor in profesores
    )


def editar_campos(profesor, profesores):
    """Permite editar los datos del profesor."""
    while True:
        print(f"""
Profesor seleccionado:
{profesor['nombres']} {profesor['apellidos']}

¿Qué dato desea editar?

1. Nombres:      {profesor['nombres']}
2. Apellidos:    {profesor['apellidos']}
3. DNI:          {profesor['dni']}
4. Correo:       {profesor['correo']}
5. Celular:      {profesor['celular']}
6. Salir
""")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":
            nuevo = input(
                "Nuevo nombre: "
            ).strip()

            if nuevo:
                profesor["nombres"] = nuevo
                print("\nNombre actualizado.")

        elif opcion == "2":
            nuevo = input(
                "Nuevo apellido: "
            ).strip()

            if nuevo:
                profesor["apellidos"] = nuevo
                print("\nApellido actualizado.")

        elif opcion == "3":
            nuevo_dni = input(
                "Nuevo DNI: "
            ).strip()

            if (
                not nuevo_dni.isdigit()
                or len(nuevo_dni) != 8
            ):
                print(
                    "El DNI debe tener "
                    "exactamente 8 dígitos."
                )
                continue

            if dni_duplicado(
                profesores,
                nuevo_dni,
                profesor["id_profesor"]
            ):
                print(
                    "Ese DNI ya está "
                    "registrado."
                )
                continue

            profesor["dni"] = nuevo_dni
            print("\nDNI actualizado.")

        elif opcion == "4":
            nuevo = input(
                "Nuevo correo: "
            ).strip()

            if nuevo:
                profesor["correo"] = nuevo
                print("\nCorreo actualizado.")

        elif opcion == "5":
            nuevo_celular = input(
                "Nuevo celular: "
            ).strip()

            if (
                not nuevo_celular.isdigit()
                or len(nuevo_celular) != 9
            ):
                print(
                    "El celular debe tener "
                    "9 dígitos."
                )
                continue

            profesor["celular"] = nuevo_celular
            print("\nCelular actualizado.")

        elif opcion == "6":
            break

        else:
            print("Opción inválida.")
            continue

        continuar = input(
            "\n¿Desea cambiar otro dato? "
            "(si/no): "
        ).strip().lower()

        if continuar != "si":
            break


def editar_profesor():
    """Busca un profesor y guarda sus cambios."""
    imprimir_titulo(
        "EDITAR DATOS DE PROFESOR"
    )

    profesores = leer_json(
        RUTA_PROFESORES
    )

    if not any(
        profesor.get("estado") == "Activo"
        for profesor in profesores
    ):
        print(
            "No hay profesores "
            "activos registrados."
        )
        return

    print("""
Buscar profesor por:

1. Nombre o apellido
2. DNI
3. Volver
""")

    opcion = input(
        "Seleccione una opción: "
    ).strip()

    if opcion == "1":
        encontrados = buscar_por_nombre(
            profesores
        )

    elif opcion == "2":
        encontrados = buscar_por_dni(
            profesores
        )

    elif opcion == "3":
        return

    else:
        print("Opción inválida.")
        return

    profesor = elegir_profesor(
        encontrados
    )

    if profesor is None:
        return

    editar_campos(
        profesor,
        profesores
    )

    guardar_json(
        RUTA_PROFESORES,
        profesores
    )

    print(
        "\nProfesor actualizado "
        "correctamente."
    )