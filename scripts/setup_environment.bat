```

### 📄 scripts/setup_environment.bat (Windows)
```batch
@echo off
echo 🔬 Setup Wally DAQ System...

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv wally_env
call wally_env\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Crear directorios
echo 📁 Creando directorios...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Descargar firmware ESP32
if not exist "esp32-20230426-v1.20.0.bin" (
    echo 📡 Descargando firmware ESP32...
    powershell -Command "Invoke-WebRequest -Uri 'https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin' -OutFile 'esp32-20230426-v1.20.0.bin'"
)

echo ✅ Entorno configurado!
echo.
echo Para activar:
echo wally_env\Scripts\activate.bat
echo.
echo Para ejecutar:
echo cd pc_controller && python main.py
pause
```
