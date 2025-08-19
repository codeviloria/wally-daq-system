"""
Configuración ESP32 - Wally DAQ System
EDITAR ESTAS VARIABLES SEGÚN TU SETUP
"""

# WiFi Configuration
WIFI_SSID = "TU_WIFI_AQUI"          # ← CAMBIAR
WIFI_PASSWORD = "TU_PASSWORD_AQUI"  # ← CAMBIAR

# Server Configuration
SERVER_PORT = 8080
DEVICE_ID = "esp32_wally_001"

# Sensor Pin Configuration
SENSOR_PINS = {
    'temperature': 34,  # Pin ADC para sensor temperatura
    'ph': 35,          # Pin ADC para sensor pH
    'motion': 32,      # Pin ADC para sensor movimiento
    'pressure': 33     # Pin ADC para sensor presión
}

# Sensor Calibration (ajustar según sensores específicos)
SENSOR_CALIBRATION = {
    'temperature': {
        'slope': 100.0,
        'offset': -50.0,
        'unit': '°C'
    },
    'ph': {
        'slope': -3.0,
        'offset': 7.0,
        'unit': 'pH'
    },
    'motion': {
        'slope': 3.03,
        'offset': -1.65,
        'unit': 'g'
    },
    'pressure': {
        'slope': 50.0,
        'offset': 0.0,
        'unit': 'kPa'
    }
}

# Timing Configuration
SAMPLE_RATE = 0.5  # segundos entre lecturas
RESPONSE_TIMEOUT = 1.0  # timeout para respuestas HTTP