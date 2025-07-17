import json
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO

# === Configuración inicial ===
url = "https://sites.google.com/view/catalogo-alma-rosa/inicio"
output_folder = "imagenes_descargadas"
os.makedirs(output_folder, exist_ok=True)

# === Configurar Selenium con Chrome ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

# === Cargar cookies ===
with open("cookies.json", "r") as f:
    cookies = json.load(f)

# Visita google.com primero para cookies .google.com
driver.get("https://www.google.com")
time.sleep(2)
for cookie in cookies:
    if ".google.com" in cookie["domain"]:
        try:
            cookie_copy = {k: v for k, v in cookie.items() if k != "domain"}
            driver.add_cookie(cookie_copy)
        except Exception as e:
            print(f"❌ No se pudo agregar cookie (google.com): {cookie['name']} → {e}")

# Visita sites.google.com para cookies específicas
driver.get("https://sites.google.com")
time.sleep(2)
for cookie in cookies:
    if "sites.google.com" in cookie["domain"]:
        try:
            cookie_copy = {k: v for k, v in cookie.items() if k != "domain"}
            driver.add_cookie(cookie_copy)
        except Exception as e:
            print(f"❌ No se pudo agregar cookie (sites.google.com): {cookie['name']} → {e}")

# Finalmente carga la página del catálogo
driver.get(url)
time.sleep(5)

# Hacer scroll para cargar imágenes dinámicas
for _ in range(6):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# === Guardar HTML de la página ===
html_path = "pagina_catalogo.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print(f"💾 HTML guardado en {html_path}")

# === Extraer y descargar imágenes ===
images = driver.find_elements(By.TAG_NAME, "img")
print(f"🔍 Detectadas {len(images)} imágenes")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": url
}

descargadas = 0
imagenes_src_map = {}

for idx, img in enumerate(images):
    src = img.get_attribute("src")
    if not src or not src.startswith("http"):
        continue

    try:
        res = requests.get(src, headers=headers, cookies={c['name']: c['value'] for c in cookies}, timeout=10)
        img_bytes = res.content

        try:
            im = Image.open(BytesIO(img_bytes))
            ext = im.format.lower() or "jpg"
            filename = f"imagen_{idx+1}.{ext}"
            file_path = os.path.join(output_folder, filename)
            im.save(file_path)
            descargadas += 1
            imagenes_src_map[filename] = src
            print(f"[{descargadas}] ✅ {filename} → {src}")
        except Exception as e:
            print(f"[{idx+1}] ❌ Imagen inválida o corrupta: {src} → {e}")
            continue

    except Exception as e:
        print(f"[{idx+1}] ❌ Error al descargar {src} → {e}")

# === Guardar mapa de imágenes ===
with open("mapa_imagenes.json", "w", encoding="utf-8") as f:
    json.dump(imagenes_src_map, f, indent=2)

print("🧭 Mapa de imágenes guardado en mapa_imagenes.json")
driver.quit()
print(f"\n🎉 Proceso finalizado: {descargadas} imágenes guardadas correctamente.")
