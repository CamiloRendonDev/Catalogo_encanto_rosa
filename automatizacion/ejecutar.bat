@echo off
echo ==========================
echo Ejecutando descarga total de imagenes...
echo ==========================
python descargar_imagenes.py

echo.
echo ==========================
echo Clasificando imagenes por seccion...
echo ==========================
python clasificar.py

echo.
echo ==========================
echo Proceso terminado.
pause
