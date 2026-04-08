@echo off

python descargar_imagenes.py

echo.
echo 📂 Clasificando imagenes...
python clasificar.py

echo.
echo 🔄 Renombrando imagenes...
python reiniciar_contador.py

echo.
echo =========================
echo ✅ PROCESO TERMINADO
echo =========================

pause