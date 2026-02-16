import os
import Funciones_Compilador.Values_Converter as converter
import Funciones_Compilador.Menu_User_Functions as menu
import Funciones_Compilador.Validators as validators

class Compilador:
    def __init__(self):
        self.Length_Data = 52  # bits
        self.Len_Instruction = 60  # bits
        self.Screen_Resolution = (256, 256)  # pixels
        self.alu_data_opernd_length = 24  # bits
        self.BUS_OPTIONS = {
            "FPU":"0000", "ALU_SIMPLE":"0001", "ALU_COMPLEX":"0010",
            "R0": "0011", "R1":        "0100", "R2":         "0101",
            "R3": "0110", "IR":        "0111", "STACK":      "1000"
        }
        self.LOAD_OPTIONS = {
            "NOP":        "0000", "ALU_SIMPLE": "0001", "ALU_COMPLEX":  "0010",
            "R0":         "0011", "R1":         "0100", "R2":           "0101",
            "R3":         "0110", "ADR_STACK":  "0111", "STACK":        "1000", 
            "GPU_INST":   "1001", "PC_0":       "1010", "PC_1":         "1011",
            "SWAP":       "1100", "LOAD_PAGE_N":"1101", "FPU_X":        "1110",
            "FPU_Y_AND_OP":"1111"
        }
        self.ALU_SIMPLE = {
            "ADD":"000", "SUB": "001", "AND":"010", "OR":"011", 
            "XOR":"100", "NOT":"101",
        }
        self.ALU_COMPLEX = {
            "MUL":"00", "DIV": "01", "MOD":"10"
        }
        self.FPU_OP = {
            "FADD":        "000", "FSUB":        "001", 
            "FMUL":        "010", "FDIV":        "011",
            "FLOAT_TO_INT":"100", "INT_TO_FLOAT":"101"
        }
        
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.memory_configuration = self.set_configuration()
        print("Bienvenido al compilador de instrucciones.")
        
        while True:
            opciones = ["Compilar instruccion", "Operar con ALU", "Imprimir recurso"]
            eleccion = menu.select_option(opciones, "¿Que desea hacer?")

            if eleccion == "Imprimir recurso":
                self.instruction_to_GPU()
            elif eleccion == "Operar con ALU":
                self.alu_operation()
            else:
                self.compile_instruction()

            if not menu.accept("Desea compilar otra instruccion?"): break

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

    def compile_instruction(self):
        load = self.get_option("load")
        bus = self.get_option("bus")
        while True :
            try:
                data = validators.check_only_hexadecimal(input(f"Ingrese la instruccion de {self.Length_Data} bits en hexadecimal: "))
                if len(data) > self.Length_Data // 4:
                    raise ValueError(f"Error: La instruccion no puede exceder los {self.Length_Data} bits.")
                else:
                    data = converter.convert_hex_to_bin(data, self.Length_Data)
                    break
            except ValueError as ve:
                print(ve)
                
        instruction = load + bus + data
    
        instruction_hex = converter.convert_bin_to_hex(instruction, self.Len_Instruction)
        print(f"Instruccion compilada: {instruction_hex}")
        self.write_in_ROM(instruction_hex)

    def alu_operation(self):
        BUS = self.BUS_OPTIONS["IR"]
        LOAD_OPTIONS = {
            "ALU_SIMPLE": self.ALU_SIMPLE,
            "ALU_COMPLEX": self.ALU_COMPLEX,
            "FPU": self.FPU_OP
        }
        options = ["ALU_SIMPLE", "ALU_COMPLEX", "FPU"]
        alu_type = menu.select_option(options, "Seleccione el tipo de ALU:")
        
        LOAD_GROUP = LOAD_OPTIONS[alu_type]
        operation = menu.select_option(list(LOAD_GROUP.keys()), "Seleccione la operacion a realizar:")
        
        LOAD = self.LOAD_OPTIONS[LOAD_OPTIONS]
        if operation in ("ADD", "SUB", "MUL", "DIV", "MOD"):
            max_min_value = 2**(self.alu_data_opernd_length - 1)
            x = validators.check_input(
                f"Ingrese el primer operando (entre {-max_min_value} y {max_min_value - 1}): ",
                int, f"Error: Entrada invalida. Ingrese un numero entero entre {-max_min_value} y {max_min_value - 1}.",
                f"-{max_min_value} <= value < {max_min_value}"
            )
            y = validators.check_input(
                f"Ingrese el segundo operando (entre {-max_min_value} y {max_min_value - 1}): ",
                int, f"Error: Entrada invalida. Ingrese un numero entero entre {-max_min_value} y {max_min_value - 1}.",
                f"-{max_min_value} <= value < {max_min_value}"
            )
            x_bin = converter.convert_int_to_bin(x, self.alu_data_opernd_length)
            y_bin = converter.convert_int_to_bin(y, self.alu_data_opernd_length)
            instruction_bin = LOAD + BUS + x_bin + y_bin + operation
            instruction_hex = converter.convert_bin_to_hex(instruction_bin, self.Len_Instruction)
            print(f"Instruccion para ALU: {instruction_hex}")
            self.write_in_ROM(instruction_hex)
        elif operation in ("AND", "OR", "XOR", "NOT"):
            while True:    
                x = validators.check_only_hexadecimal(input(f"Ingrese el operando x {self.alu_data_opernd_length // 4} digitos hexadecimales: "))
                if len(x) > self.alu_data_opernd_length // 4:
                    print(f"Error: El operando no puede exceder los {self.alu_data_opernd_length} bits."); continue
                y = validators.check_only_hexadecimal(input(f"Ingrese el operando y {self.alu_data_opernd_length // 4} digitos hexadecimales: "))
                if len(y) > self.alu_data_opernd_length // 4:
                    print(f"Error: El operando no puede exceder los {self.alu_data_opernd_length} bits."); continue
                break
            x_bin = converter.convert_hex_to_bin(x, self.alu_data_opernd_length)
            y_bin = converter.convert_hex_to_bin(y, self.alu_data_opernd_length)
            instruction_bin = LOAD + BUS + x_bin + y_bin + operation
            instruction_hex = converter.convert_bin_to_hex(instruction_bin, self.Len_Instruction)
            print(f"Instruccion para ALU: {instruction_hex}")
            self.write_in_ROM(instruction_hex)

        else: # FPU operations
            raise NotImplementedError("Operacion de FPU no implementada.")
    
    def get_option(self, options_type):
        """
        Args:
            options_type (str): "bus" o "load"
        Returns:
            str: valor binario correspondiente a la opcion seleccionada
        """
        opciones = self.BUS_OPTIONS if options_type == "bus" else self.LOAD_OPTIONS
        options_keys = list(opciones.keys())
        
        option = menu.select_option(options_keys, f"Seleccione una opcion de {options_type}:")        
        return opciones[option]

    def instruction_to_GPU(self):
        BUS = self.BUS_OPTIONS["CU"]
        LOAD = self.LOAD_OPTIONS["GPU_INST"]

        try:
            op = "00" # Operacion de carga de recurso a frambuffer
            x = int(input(f"Ingrese la coordenada X donde se colocara el recurso en pantalla (0-{self.Screen_Resolution[0] - 1}): "))
            y = int(input(f"Ingrese la coordenada Y donde se colocara el recurso en pantalla (0-{self.Screen_Resolution[1] - 1}): "))
            w = int(input("Ingrese el ancho del recurso (0-7 pixeles): "))
            h = int(input("Ingrese el alto del recurso (0-7 pixeles): "))
            dir_resource = int(input("Ingrese la posicion del recurso (en decimal):" )) * 64  # cada recurso ocupa 64 pixeles (8x8)
        except ValueError:
            print("Error: Entrada invalida. Asegurese de ingresar numeros enteros.")
            return

        coordenadas_bin = converter.convert_int_to_bin(x, 8) + converter.convert_int_to_bin(y, 8)
        dimension_bin = converter.convert_int_to_bin(w, 3) + converter.convert_int_to_bin(h, 3)
        dir_bin = converter.convert_int_to_bin(dir_resource, 24)
        print(converter.convert_bin_to_hex(dir_bin, 24))
        raise NotImplementedError("Carga de recursos a GPU no implementada completamente.")
        instruction_bin = LOAD + BUS + dir_bin + dimension_bin + coordenadas_bin + op
        instruction_hex = converter.convert_bin_to_hex(instruction_bin, self.Len_Instruction)
        print(f"Instruccion para GPU: {instruction_hex}")
        self.write_in_ROM(instruction_hex)

if __name__ == "__main__":
    Compilador()