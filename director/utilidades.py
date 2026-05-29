def imprimir_titulo(texto):  # muestra un título centrado con marcos
    ancho = 40

    print("-" * ancho)
    print(texto.center(ancho))
    print("-" * ancho)

def pausa():  # espera que el usuario presione enter
    input("\nPresione Enter para continuar...")
