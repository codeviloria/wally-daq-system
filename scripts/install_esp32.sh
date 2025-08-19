#!/bin/bash
# Script para flashear ESP32 con MicroPython

PORT=${1:-/dev/ttyUSB0}

echo "🔧 Instalando MicroPython en ESP32..."
echo "Puerto: $PORT"

# Verificar que esptool esté instalado
if ! command -v esptool.py &> /dev/null; then
    echo "❌ esptool.py no encontrado. Instalando..."
    pip install esptool
fi

# Limpiar flash
echo "🗑️ Limpiando flash..."
esptool.py --chip esp32 --port $PORT erase_flash

# Flashear MicroPython
echo "📡 Flasheando MicroPython..."
esptool.py --chip esp32 --port $PORT write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

# Subir archivos
echo "📤 Subiendo archivos al ESP32..."
ampy --port $PORT put esp32/main.py
ampy --port $PORT put esp32/config.py
ampy --port $PORT put esp32/sensor_server.py
ampy --port $PORT put esp32/boot.py

echo "✅ ESP32 configurado exitosamente!"
echo ""
echo "Para conectar al ESP32:"
echo "screen $PORT 115200"
echo ""
echo "En el REPL de MicroPython ejecutar:"
echo "exec(open('main.py').read())"