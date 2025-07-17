import os
import json
import shutil
from bs4 import BeautifulSoup

# === Configuración inicial ===
html_file = "pagina_catalogo.html"
mapa_file = "mapa_imagenes.json"
carpeta_imagenes = "imagenes_descargadas"
salida_por_seccion = "imagenes_por_seccion"
os.makedirs(salida_por_seccion, exist_ok=True)

# === Cargar HTML y mapa de imágenes descargadas ===
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

with open(mapa_file, "r", encoding="utf-8") as f:
    mapa = json.load(f)

# === Recorrer HTML en orden y asociar imágenes a la última sección vista ===
asociaciones = {}
ultima_seccion = "SIN_SECCION"

for elem in soup.find_all(True):  # recorre todos los tags en orden
    # Si es un título de sección
    if elem.name == "span" and "FdCeP" in elem.get("class", []):
        texto = elem.get_text().strip()
        if texto:
            ultima_seccion = texto.upper().replace(" ", "_")

    # Si es imagen
    elif elem.name == "img":
        src = elem.get("src", "")
        if src:
            for filename, original_src in mapa.items():
                if src in original_src:
                    asociaciones[filename] = ultima_seccion
                    break

# === Mover imágenes a carpetas ===
for filename in os.listdir(carpeta_imagenes):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    seccion = asociaciones.get(filename, "SIN_SECCION")
    destino = os.path.join(salida_por_seccion, seccion)
    os.makedirs(destino, exist_ok=True)

    origen = os.path.join(carpeta_imagenes, filename)
    shutil.copy2(origen, os.path.join(destino, filename))
    print(f"✅ {filename} → {seccion}")

print(f"\n🎉 Clasificación completa: {len(os.listdir(carpeta_imagenes))} imágenes distribuidas en carpetas.")
