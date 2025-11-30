import re
import struct
from pathlib import Path

def bin_to_hex(binary_string):
    # Eliminar espacios y saltos de línea
    binary_string = binary_string.replace(" ", "").replace("\n", "")
    
    # Asegurar que la longitud sea múltiplo de 8 (1 byte = 8 bits)
    if len(binary_string) % 8 != 0:
        padding = 8 - (len(binary_string) % 8)
        binary_string = ("0" * padding) + binary_string

    # Dividir en bytes de 8 bits
    hex_result = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        valor = int(byte, 2)
        hex_result += f"{valor:02X}"

    return hex_result.strip()

# Archivo fuente
entrada = Path("New Piskel.c")
salida_dir = Path("frames_bin")
tiles = ""
salida_dir.mkdir(exist_ok=True)

# Leer el archivo completo
with open(entrada, "r", encoding="utf-8") as f:
    contenido = f.read()

# Extraer los bloques de datos dentro de llaves { ... }
bloques = re.findall(r'\{([^{}]+)\}', contenido, re.DOTALL)

print(f"Se encontraron {len(bloques)} frames")

# Procesar cada bloque como un frame independiente
for i, bloque in enumerate(bloques):
    # Extraer los valores hexadecimales del bloque
    pixeles = re.findall(r'0x[0-9a-fA-F]+', bloque)
    
    # Convertir cada color a 1 (blanco) o 0 (negro)
    bits =""
    for px in pixeles:
        if px.lower() == "0xffffffff":
            bits += "1"
        else:
            bits += "0"
    
    bits = bits[::-1]
    bits = bin_to_hex(bits)
    tiles += (bits + "\n")
    # Guardar binario del frame
salida = salida_dir / f"frames.txt"
with open(salida, "w") as f:
        f.write(tiles)

print("✅ Conversión completa.")
print(f"Los binarios están en: {salida_dir.resolve()}")

