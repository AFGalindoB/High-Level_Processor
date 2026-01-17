import os
import Funciones_Compilador.Values_Converter as converter
import Funciones_Compilador.Menu_User_Functions as menu
import Funciones_Compilador.Validators as validators

class Compilador:
    def __init__(self):
        self.Length_Data = 48  # bits
        self.Len_Instruction = 56  # bits
        self.Screen_Resolution = (256, 256)  # pixels
        self.BUS_OPTIONS = {
            "ALU_R": "000",
            "R0":    "001", "R1":       "010", "R2":   "011", "R3": "100",
            "CU":    "101", "VAR_CACHE":"110", "INPUT":"111"
        }
        self.LOAD_OPTIONS = {
            "NOP":            "00000", "ALU_X":          "00001", "ALU_Y":            "00010",
            "R0":             "00011", "R1":             "00100", "R2":               "00101",
            "R3":             "00110", "IF_WH_CONDITION":"00111", "IF_WH_ADR":        "01000", 
            "CACHE_PC":       "01001", "PC":             "01010", "ALU_OP":           "01011",
            "PC_JM_OP":       "01100", "GPU_INST":       "01101"
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
        BUS = self.BUS_OPTIONS["CU"]
        LOAD1 = self.LOAD_OPTIONS["ALU_X"]
        LOAD2 = self.LOAD_OPTIONS["ALU_Y"]
        LOAD3 = self.LOAD_OPTIONS["ALU_OP"]

        opciones = ["Enteros", "Decimales", "Logicos"]
        tipo_de_dato = menu.select_option(opciones, "Seleccione el tipo de dato a operar:")

        if tipo_de_dato == "Enteros":
            while True:
                try:
                    max_value = (1 << self.Length_Data) - 1

                    x_bin = int(input(f"Ingrese el valor entero de x (Min. 0, Max. {max_value}): "))
                    y_bin = int(input(f"Ingrese el valor entero de y (Min. 0, Max. {max_value}): "))

                    if not (0 <= x_bin <= max_value):
                        raise ValueError(f"Error: x debe estar entre 0 y {max_value}.")
                    if not (0 <= y_bin <= max_value):
                        raise ValueError(f"Error: y debe estar entre 0 y {max_value}.")

                    x_bin = converter.convert_int_to_bin(x_bin, self.Length_Data)
                    y_bin = converter.convert_int_to_bin(y_bin, self.Length_Data)
                    break
                except ValueError as ve:
                    print(ve)
        elif tipo_de_dato == "Decimales":
            raise NotImplementedError("Operacion con decimales no implementada.")
        elif tipo_de_dato == "Logicos":
            while True:
                try:
                    x_bin = validators.check_only_hexadecimal(input(f"Ingrese el valor logico de x (en hexadecimal) (Max. {self.Length_Data // 4} digitos): "))
                    y_bin = validators.check_only_hexadecimal(input(f"Ingrese el valor logico de y (en hexadecimal) (Max. {self.Length_Data // 4} digitos): "))

                    if len(x_bin) > self.Length_Data // 4 or len(y_bin) > self.Length_Data // 4:
                        raise ValueError(f"Error: Los valores logicos no pueden exceder los {self.Length_Data} bits.")
                    
                    x_bin = converter.convert_hex_to_bin(x_bin, self.Length_Data)
                    y_bin = converter.convert_hex_to_bin(y_bin, self.Length_Data)
                    break
                except ValueError as ve:
                    print(ve)
            
        operacion = menu.select_option(list(self.ALU_OP.keys()), "Seleccione la operacion a realizar:")
        alu_op_bin = self.ALU_OP[operacion].zfill(self.Length_Data)
        print(f"{operacion} {x_bin} {y_bin}")
        
        instruction = converter.convert_bin_to_hex(LOAD1 + BUS + x_bin, self.Len_Instruction)
        print(LOAD1 + BUS + x_bin, instruction, sep="\n")
        self.write_in_ROM(instruction)
        
        instruction = converter.convert_bin_to_hex(LOAD2 + BUS + y_bin, self.Len_Instruction)
        print(LOAD2 + BUS + y_bin, instruction, sep="\n")
        self.write_in_ROM(instruction)
        
        instruction = converter.convert_bin_to_hex(LOAD3 + BUS + alu_op_bin, self.Len_Instruction)
        print(LOAD3 + BUS + alu_op_bin, instruction, sep="\n")
        self.write_in_ROM(instruction)
    
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