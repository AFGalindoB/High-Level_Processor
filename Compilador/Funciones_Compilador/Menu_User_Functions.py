def select_option(options:list, text:str):
    """Muestra un menu de opciones y devuelve el valor seleccionado de la lista. (NO el indice)"""

    while True:
        print(text)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            eleccion = int(input("Ingrese el numero de la opcion: "))
            if 1 <= eleccion <= len(options):
                return options[eleccion - 1]
            else:
                print("Opcion invalida, intente de nuevo.")
        except ValueError:
            print("Entrada invalida. Por favor ingrese un numero.")

def accept(text):
    """
    Pregunta al usuario una pregunta de si/no y devuelve True o False.
    
    :param text: Texto a mostrar al usuario
    :return: True si el usuario responde 's', False si responde 'n'
    """
    while True:
        respuesta = input(f"{text} (s/n): ").lower()
        if respuesta == 's' or respuesta == 'n':
            return True if respuesta == 's' else False
        else:
            print("Respuesta invalida. Por favor ingrese 's' para si o 'n' para no.")