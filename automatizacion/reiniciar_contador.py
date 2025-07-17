import os

# Ruta a la carpeta donde están las imágenes por sección
carpeta = r"C:\Users\Personal\Documents\Visual studio code\Catalogo_encanto_rosa\automatizacion\imagenes_por_seccion\TANGAS\TANGA_HILO"  # Cambia esto según la carpeta que quieras procesar

# Obtener lista de archivos de imagen válidos
extensiones_validas = [".jpg", ".jpeg", ".png", ".webp"]
imagenes = sorted([
    f for f in os.listdir(carpeta)
    if os.path.isfile(os.path.join(carpeta, f)) and os.path.splitext(f)[1].lower() in extensiones_validas
])

# Renombrar reiniciando desde 1
for i, nombre in enumerate(imagenes, start=1):
    ext = os.path.splitext(nombre)[1].lower()
    nuevo_nombre = f"{i}{ext}"
    origen = os.path.join(carpeta, nombre)
    destino = os.path.join(carpeta, nuevo_nombre)
    os.rename(origen, destino)
    print(f"✅ {nombre} → {nuevo_nombre}")

print(f"\n🎉 Renombradas {len(imagenes)} imágenes en: {carpeta}")
