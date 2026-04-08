import os
import unicodedata
from bs4 import BeautifulSoup

print("🔥 ACTUALIZANDO INDEX...")

CARPETA = "imagenes_por_seccion"
INDEX = "index.html"
OUTPUT = "index.html"  # sobrescribe el mismo

# =========================
# NORMALIZAR TEXTO
# =========================
def limpiar(texto):
    texto = texto.split("-")[0].strip().upper()
    texto = texto.replace(" ", "_")

    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')

    return texto

# =========================
# BUSCAR CARPETA PARECIDA
# =========================
def buscar_carpeta(nombre):
    for carpeta in os.listdir(CARPETA):
        if nombre in carpeta.upper():
            return carpeta
    return None

# =========================
# CARGAR HTML
# =========================
with open(INDEX, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

log_eliminadas = []
log_ok = []

# =========================
# RECORRER SECCIONES HTML
# =========================
for title in soup.find_all("div", class_="section-title"):

    texto = title.get_text()
    nombre = limpiar(texto)

    carpeta_real = buscar_carpeta(nombre)

    gallery = title.find_next_sibling("div", class_="gallery")

    if not gallery:
        continue

    if not carpeta_real:
        log_eliminadas.append(texto)
        continue

    ruta = os.path.join(CARPETA, carpeta_real)

    # GUARDAR MODELOS
    modelos = []
    for img in gallery.find_all("img"):
        src = img.get("data-src", "")
        if "modelo" in src:
            modelos.append(img)

    # LIMPIAR
    gallery.clear()

    # AGREGAR NUEVAS
    archivos = sorted(os.listdir(ruta))

    for archivo in archivos:
        if not archivo.endswith(".webp"):
            continue

        if "modelo" in archivo.lower():
            continue

        img = soup.new_tag("img")
        img["data-src"] = f"imagenes_por_seccion/{carpeta_real}/{archivo}"
        img["alt"] = texto

        gallery.append(img)

    # VOLVER A AGREGAR MODELOS
    for m in modelos:
        gallery.append(m)

    log_ok.append(texto)

# =========================
# GUARDAR HTML
# =========================
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ INDEX ACTUALIZADO")

# =========================
# LOG
# =========================
with open("log_cambios.txt", "w", encoding="utf-8") as f:
    f.write("=== ACTUALIZADAS ===\n")
    for s in log_ok:
        f.write(f"✔ {s}\n")

    f.write("\n=== ELIMINADAS (ya no existen en Google Sites) ===\n")
    for s in log_eliminadas:
        f.write(f"✖ {s}\n")

print("🧾 LOG generado: log_cambios.txt")