import re
from pathlib import Path

# Archivo fuente en C
entrada = Path("New Piskel.c")

# Archivo de salida
salida = Path("frames_rgb.txt")

# Leer todo el archivo
with open(entrada, "r", encoding="utf-8") as f:
    contenido = f.read()

# Extraer todos los colores en formato 0xXXXXXXXX
pixeles = re.findall(r'0x[0-9a-fA-F]{8}', contenido)

print(f"Se encontraron {len(pixeles)} pixeles")

# Procesar y convertir a RGB888
lineas = []
for px in pixeles:
    hex32 = px[2:]          # quitar 0x
    rgb = hex32[2:]         # quitar AA → BB GG RR
    rgb = rgb[-1::-1]       # invertir a RR GG BB
    lineas.append(rgb.lower())

# Guardar archivo
with open(salida, "w") as f:
    for linea in lineas:
        f.write(linea + "\n")

print("✅ Conversión completa.")
print(f"Archivo generado: {salida.resolve()}")
