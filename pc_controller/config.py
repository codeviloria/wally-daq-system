"""
Configuración de la aplicación Wally PC Controller
"""
import os

# Información de la aplicación
VERSION = "1.0.0"
WINDOW_TITLE = "🔬 Wally - Sistema de Adquisición de Datos"
WINDOW_SIZE = "1400x900"

# Configuración ESP32
ESP32_IP = "192.168.1.100"  # ← CAMBIAR por la IP de tu ESP32
ESP32_PORT = 8080
CONNECTION_TIMEOUT = 5  # segundos

# Configuración de adquisición de datos
SAMPLE_INTERVAL = 1.0   # segundos entre lecturas
MAX_BUFFER_SIZE = 1000  # máximo de entradas en buffer
AUTO_SAVE_INTERVAL = 300  # auto-guardar cada 5 minutos

# Configuración de archivos
DATA_DIRECTORY = "data/"
DEFAULT_CSV_NAME = "wally_sensor_data.csv"
LOG_FILE = "data/system.log"

# UI Configuration
CHART_UPDATE_INTERVAL = 1000  # ms
MAX_CHART_POINTS = 100       # puntos máximos en gráfico
CHART_COLORS = {
    'temperature': '#FF4444',  # Rojo
    'ph': '#44FF44',          # Verde
    'motion': '#4444FF',      # Azul
    'pressure': '#FF8800'     # Naranja
}

# Sensor Configuration
SENSOR_LABELS = {
    'temperature': '🌡️ Temperatura',
    'ph': '🧪 pH',
    'motion': '📱 Movimiento',
    'pressure': '⚡ Presión'
}

SENSOR_UNITS = {
    'temperature': '°C',
    'ph': 'pH',
    'motion': 'g',
    'pressure': 'kPa'
}

# Rangos normales para validación
SENSOR_RANGES = {
    'temperature': (-40, 100),  # °C
    'ph': (0, 14),             # pH
    'motion': (-5, 5),         # g
    'pressure': (0, 1000)      # kPa
}

# Networking
HTTP_TIMEOUT = 3  # segundos
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1   # segundos entre reintentos