import os

class Compilador:
    def __init__(self):
        self.BUS_OPTIONS = {
            "ALU_RESULT": "0000",
            "R0":         "0001", "R1":           "0010", "R2": "00011", "R3": "0100",
            "R4":         "0101", "R5":           "0110", "R6": "00111", "R7": "1000",
            "CU":         "1001"
        }
        self.LOAD_OPTIONS = {
            "ALU_X":              "00000", "ALU_Y":          "00001", "ALU_RESULT":       "00010",
            "R0":                 "00011", "R1":             "00100", "R2":               "00101",
            "R3":                 "00110", "R4":             "00111", "R5":               "01000", 
            "R6":                 "01001", "R7":             "01010", "GPU_INSTRUCTIONS": "01011",
            "IF-WHILE_CONDITION": "01100", "IF-WHILE_START": "01101", "IF-WHILE_END":     "01110",
            "JUMP_DATA":          "01111", "IN_STACK":       "10000", "PC_JUMP": "10001",
            "ALU_OP":             "10010", "PC_JUMP_OP":     "10011", "GPU_INSTRUCTION_ADDRESS":"10100",
            "STAC_ADDRESS":        "10101"
        }
        self.ALU_OP = {
            "ADD":"0000", "SUB":"0001", "MUL":"0010", "DIV":"0011",
            "AND":"0100", "NAND":"0101","OR":"0110", "NOR":"0111",
            "XOR":"1000", "XNOR":"1001", "GTR":"1010", "LSS":"1011",
            "EQL":"1100"
        }
        
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.memory_configuration = self.set_configuration()
        print("Bienvenido al compilador de instrucciones.")
        
        TARGET_BITS = 42
        while True:
            load = self.get_option("load")
            bus = self.get_option("bus")
            data = self.get_data()
            instruction = load + bus + data
            
            instruction_hex = hex(int(instruction, 2))[2:].upper().zfill((TARGET_BITS + 3) // 4)
            print(f"Instruccion compilada: {instruction_hex}")
            self.write_memory(instruction_hex)
            opcion = input("Desea compilar otra instruccion? (s/n): ").lower()
            if opcion == 'n': break

    def write_memory(self, instruction):
        memory_path = os.path.join(self.root_path, "ROM.txt")
        with open(memory_path, "a") as f:
            f.write(instruction + "\n")

    def set_configuration(self):
        memory_path = os.path.join(self.root_path, "ROM.txt")
        if not os.path.exists(memory_path):
            with open(memory_path, "w") as f:
                f.write("")
        print(f"Archivo de configuracion de memoria en: {memory_path}")

    def get_data(self):
        while True :
            data = input("Ingrese la instruccion de 32 bits en hexadecimal: ")
            if len(data) <= 8:
                # Convertir de hexadecimal a binario manteniendo como string
                data_binary = bin(int(data, 16))[2:].zfill(32)
                return data_binary
            else:
                print("Instruccion invalida, intente de nuevo.")
    
    def get_option(self, options_type):
        if options_type == "bus":
            options_keys = list(self.BUS_OPTIONS.keys())
            opciones = self.BUS_OPTIONS
        elif options_type == "load":
            options_keys = list(self.LOAD_OPTIONS.keys())
            opciones = self.LOAD_OPTIONS
        else:
            raise ValueError("Tipo de opcion invalido.")
        
        while True:
            print(f"Opciones de {options_type} disponibles:")
            for i in options_keys:
                print(i)
            
            option = input(f"Ingrese la opcion de {options_type}: ").upper()
            if option in options_keys:
                if options_type == "load":
                    cargar = input("Desea cargar la opcion? (s/n): ").lower()
                    if cargar == 's':
                        carga = "1"
                    else:
                        carga = "0"
                    opcion_elegida = opciones[option] + carga
                else:
                    opcion_elegida = opciones[option]
                print(f"Opcion elegida de {options_type}: {opcion_elegida}")
                return opcion_elegida
            else:
                print("Opcion invalida, intente de nuevo.")

if __name__ == "__main__":
    Compilador()