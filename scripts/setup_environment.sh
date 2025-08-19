#!/bin/bash
# Setup script para Wally DAQ System

echo "🔬 Configurando entorno Wally DAQ System..."

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv wally_env
source wally_env/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data
mkdir -p logs

# Descargar firmware ESP32 si no existe
if [ ! -f "esp32-20230426-v1.20.0.bin" ]; then
    echo "📡 Descargando firmware ESP32..."
    wget https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin
fi

echo "✅ Entorno configurado exitosamente!"
echo ""
echo "Para activar el entorno:"
echo "source wally_env/bin/activate"
echo ""
echo "Para ejecutar la aplicación:"
echo "cd pc_controller && python main.py"