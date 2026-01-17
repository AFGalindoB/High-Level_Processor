def check_only_binary(value:str):
    if not all(ch in '01' for ch in value):
        raise ValueError("Entrada invalida: solo se admiten 0 y 1 en el input.")
    else:
        return value

def check_only_hexadecimal(value:str):
    hex_digits = set("0123456789abcdefABCDEF")
    if not all(ch in hex_digits for ch in value):
        raise ValueError("Entrada invalida: solo se admiten digitos hexadecimales en el input.")
    else:
        return value

def check_input(prompt:str, type_input:any, error_msg:str, condicion="True"):
    """Solicita una entrada al usuario y valida su tipo.

    Args:
        prompt (str): Mensaje a mostrar al usuario.
        type_input (any): Tipo de dato esperado (e.g., int, float).
        error_msg (str): Mensaje de error en caso de entrada invalida.

    Returns:
        any: Entrada validada del tipo especificado.
    """
    while True:
        try:
            value = type_input(input(prompt))
            if (not eval(condicion)):
                raise ValueError
            return value
        except ValueError:
            print(error_msg)