```

### 📄 scripts/install_esp32.bat (Windows)
```batch
@echo off
set PORT=%1
if "%PORT%"=="" set PORT=COM3

echo 🔧 Instalando MicroPython en ESP32...
echo Puerto: %PORT%

REM Verificar esptool
python -c "import esptool" 2>nul
if errorlevel 1 (
    echo ❌ esptool no encontrado. Instalando...
    pip install esptool
)

REM Verificar ampy
python -c "import ampy" 2>nul
if errorlevel 1 (
    echo ❌ ampy no encontrado. Instalando...
    pip install adafruit-ampy
)

REM Limpiar flash
echo 🗑️ Limpiando flash...
esptool.py --chip esp32 --port %PORT% erase_flash

REM Flashear MicroPython
echo 📡 Flasheando MicroPython...
esptool.py --chip esp32 --port %PORT% write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

REM Esperar un momento
timeout /t 3 /nobreak >nul

REM Subir archivos
echo 📤 Subiendo archivos...
ampy --port %PORT% put esp32\main.py
ampy --port %PORT% put esp32\config.py
ampy --port %PORT% put esp32\sensor_server.py
ampy --port %PORT% put esp32\boot.py

echo ✅ ESP32 configurado!
echo.
echo Para conectar usar:
echo - PuTTY: %PORT%, 115200 baud
echo - Python: python -m serial.tools.miniterm %PORT% 115200
echo.
echo En REPL ejecutar:
echo exec(open('main.py').read())
pause
```
