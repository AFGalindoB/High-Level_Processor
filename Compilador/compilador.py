import os
import Funciones_Compilador.Values_Converter as converter

class Compilador:
    def __init__(self):
        self.BUS_OPTIONS = {
            "ALU_RESULT": "0000",
            "R0":         "0001", "R1":   "0010", "R2": "00011", "R3": "0100",
            "R4":         "0101", "R5":   "0110", "R6": "00111", "R7": "1000",
            "CU":         "1001"
        }
        self.LOAD_OPTIONS = {
            "ALU_X":               "00000", "ALU_Y":          "00001", "ALU_R":            "00010",
            "R0":                  "00011", "R1":             "00100", "R2":               "00101",
            "R3":                  "00110", "R4":             "00111", "R5":               "01000", 
            "R6":                  "01001", "R7":             "01010", "GPU_INST":         "01011",
            "IF-WH_CONDITION":     "01100", "IF-WH_START":    "01101", "IF-WH_END":        "01110",
            "PC_JM_DTA":           "01111", "IN_STACK":       "10000", "PC_JUMP":          "10001",
            "ALU_OP":              "10010", "PC_JM_OP":     "10011", "GPU_INST_ADRS":    "10100",
            "STAC_ADDRESS":        "10101"
        }
        self.ALU_OP = {
            "ADD":"0000", "SUB": "0001", "MUL":"0010", "DIV":"0011",
            "AND":"0100", "NAND":"0101", "OR": "0110", "NOR":"0111",
            "XOR":"1000", "XNOR":"1001", "GTR":"1010", "LSS":"1011",
            "EQL":"1100"
        }
        
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.memory_configuration = self.set_configuration()
        print("Bienvenido al compilador de instrucciones.")
        
        while True:
            opciones = ["Compilar instruccion", "Operar con ALU", "Imprimir palabra en hardware"]
            eleccion = self.select_option(opciones, "¿Que desea hacer?")

            if eleccion == "Imprimir palabra en hardware":
                self.print_hardware()
            elif eleccion == "Operar con ALU":
                self.alu_operation()
            else:
                self.compile_instruction()
            
            opcion = input("Desea compilar otra instruccion? (s/n): ").lower()
            if opcion == 'n': break

    def set_configuration(self):
        memory_path = os.path.join(self.root_path, "ROM.txt")
        if not os.path.exists(memory_path):
            with open(memory_path, "w") as f:
                f.write("")
        print(f"Archivo de configuracion de memoria en: {memory_path}")

    def write_in_ROM(self, instruction):
        memory_path = os.path.join(self.root_path, "ROM.txt")
        with open(memory_path, "a") as f:
            f.write(instruction + "\n")

    def select_option(self, options:list, text:str):
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

    def accept(self, text):
        while True:
            respuesta = input(f"{text} (s/n): ").lower()
            if respuesta == 's' or respuesta == 'n':
                return respuesta
            else:
                print("Respuesta invalida. Por favor ingrese 's' para si o 'n' para no.")

    def check_only_binary(self, value:str):
        if not all(ch in '01' for ch in value):
            raise ValueError("Entrada invalida: solo se admiten 0 y 1 en el input.")
        else:
            return value

    def check_only_hexadecimal(self, value:str):
        hex_digits = set("0123456789abcdefABCDEF")
        if not all(ch in hex_digits for ch in value):
            raise ValueError("Entrada invalida: solo se admiten digitos hexadecimales en el input.")
        else:
            return value

    def compile_instruction(self):
        load = self.get_option("load")
        bus = self.get_option("bus")
        while True :
            try:
                data = self.check_only_hexadecimal(input("Ingrese la instruccion de 32 bits en hexadecimal: "))
                if len(data) > 8:
                    raise ValueError("Error: La instruccion no puede exceder los 32 bits.")
                else:
                    data = converter.convert_hex_to_bin(data, 32)
                    break
            except ValueError as ve:
                print(ve)
                
        instruction = load + bus + data
    
        instruction_hex = converter.convert_bin_to_hex(instruction, 42)
        print(f"Instruccion compilada: {instruction_hex}")
        self.write_in_ROM(instruction_hex)

    def alu_operation(self):
        BUS = "1001" # CU
        LOAD1 = "000001" # ALU_X
        LOAD2 = "000011" # ALU_Y
        LOAD3 = "100101" # ALU_OP
        LOAD4 = "000101" # ALU_R

        opciones = ["Enteros", "Decimales", "Logicos"]
        tipo_de_dato = self.select_option(opciones, "Seleccione el tipo de dato a operar:")

        if tipo_de_dato == "Enteros":
            while True:
                try:
                    x_bin = int(input("Ingrese el valor entero de x (Min. 0, Max. 4.294.967.295): "))
                    y_bin = int(input("Ingrese el valor entero de y (Min. 0, Max. 4.294.967.295): "))
                    if not (0 <= x_bin <= 4294967295) or not (0 <= y_bin <= 4294967295):
                        raise ValueError("Error: Los valores enteros deben estar entre 0 y 4.294.967.295.")
                    x_bin = converter.convert_int_to_bin(x_bin, 32)
                    y_bin = converter.convert_int_to_bin(y_bin, 32)
                    break
                except ValueError as ve:
                    print(ve)
        elif tipo_de_dato == "Decimales":
            raise NotImplementedError("Operacion con decimales no implementada.")
        elif tipo_de_dato == "Logicos":
            while True:
                try:
                    x_bin = self.check_only_hexadecimal(input("Ingrese el valor logico de x (en hexadecimal) (Max. 8 digitos): "))
                    y_bin = self.check_only_hexadecimal(input("Ingrese el valor logico de y (en hexadecimal) (Max. 8 digitos): "))
                    if len(x_bin) > 8 or len(y_bin) > 8:
                        raise ValueError("Error: Los valores logicos no pueden exceder los 32 bits.")
                    x_bin = converter.convert_hex_to_bin(x_bin, 32)
                    y_bin = converter.convert_hex_to_bin(y_bin, 32)
                    break
                except ValueError as ve:
                    print(ve)
            
        operacion = self.select_option(list(self.ALU_OP.keys()), "Seleccione la operacion a realizar:")
        alu_op_bin = self.ALU_OP[operacion].zfill(32)
        print(f"{operacion} {x_bin} {y_bin}")
        
        instruction = LOAD1 + BUS + x_bin
        self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))
        instruction = LOAD2 + BUS + y_bin
        self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))
        instruction = LOAD3 + BUS + alu_op_bin
        self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))
        instruction = LOAD4 + BUS + "0"*32
        self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))

    def print_hardware(self):    
        palabra = []
        BUS = "1001"  # CU
        LOAD1 = "101001"  # GPU_INSTRUCTION_ADDRESS
        LOAD2 = "010111"  # GPU_INSTRUCTIONS
        letras = {" ":"0000000", "A":"0000001", "B":"0000010", "C":"0000011", "D":"0000100", "E":"0000101", 
                  "F":"0000110", "G":"0000111", "H":"0001000", "I":"0001001", "J":"0001010", "K":"0001011", 
                  "L":"0001100", "M":"0001101", "N":"0001110", "Ñ":"0001111", "O":"0010000", "P":"0010001", 
                  "Q":"0010010", "R":"0010011", "S":"0010100", "T":"0010101", "U":"0010110", "V":"0010111", 
                  "W":"0011000", "X":"0011001", "Y":"0011010", "Z":"0011011", "a":"0011100", "b":"0011101", 
                  "c":"0011110", "d":"0011111", "e":"0100000", "f":"0100001", "g":"0100010", "h":"0100011", 
                  "i":"0100100", "j":"0100101", "k":"0100110", "l":"0100111", "m":"0101000", "n":"0101001",
                  "ñ":"0101010", "o":"0101011", "p":"0101100", "q":"0101101", "r":"0101110", "s":"0101111",
                  "t":"0110000", "u":"0110001", "v":"0110010", "w":"0110011", "x":"0110100", "y":"0110101", 
                  "z":"0110110", "1":"0110111", "2":"0111000", "3":"0111001", "4":"0111010", "5":"0111011",
                  "6":"0111100", "7":"0111101", "8":"0111110", "9":"0111111", "0":"1000000", "+":"1000001",
                  "-":"1000010", "*":"1000011", "/":"1000100", ".":"1000101", ",":"1000110", ":":"1000111",
                  ";":"1001000", "!":"1001001", "¡":"1001010", "?":"1001011", "¿":"1001100", '"':'1001101',
                  "'":"1001110", "#":"1001111", "$":"1010000", "=":"1010001", "<":"1010010", ">":"1010011",
                  "(":"1010100", ")":"1010101", "[":"1010110", "]":"1010111", "%":"1011000", "°":"1011001",
                  "_":"1011010", "~":"1011011", "@":"1011100", "{":"1011101", "}":"1011110", "^":"1011111",
                 "\\":"1100000", "&":"1100001", "|":"1100010"}
        
        entrada = input("Ingrese la palabra a imprimir: ")
        for char in entrada:
            if char in letras:
                palabra.append(letras[char])
                print(f"Caracter {char} agregado.")
            else:
                print(f"Caracter {char} no valido, se omite.")

        for i in range(len(palabra)):
            data = bin(i)[2:].zfill(32)
            instruction = LOAD1 + BUS + data
            self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))
            letra = palabra[i].zfill(32)
            instruction = LOAD2 + BUS + letra
            self.write_in_ROM(converter.convert_bin_to_hex(instruction, 42))
    
    def get_option(self, options_type):
        """
        Args:
            options_type (str): "bus" o "load"
        Returns:
            str: valor binario correspondiente a la opcion seleccionada
        """
        opciones = self.BUS_OPTIONS if options_type == "bus" else self.LOAD_OPTIONS
        options_keys = list(opciones.keys())
        
        while True:
            option = self.select_option(options_keys, f"Seleccione una opcion de {options_type}:")
            if options_type == "load":
                carga = "1" if self.accept("Desea cargar el valor?") == 's' else "0"
                return opciones[option] + carga
            else:
                return opciones[option]

if __name__ == "__main__":
    Compilador()