"""
Utilidades varias para el sistema Wally
"""
import time
import os
import json
from datetime import datetime

def format_timestamp(timestamp):
    """Formatear timestamp a string legible"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def ensure_directory(path):
    """Asegurar que un directorio existe"""
    os.makedirs(path, exist_ok=True)

def save_config(config_data, filename):
    """Guardar configuración a archivo JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(config_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando config: {e}")
        return False

def load_config(filename):
    """Cargar configuración desde archivo JSON"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando config: {e}")
        return None

def validate_sensor_value(sensor_type, value):
    """Validar que un valor de sensor esté en rango válido"""
    ranges = {
        'temperature': (-40, 100),
        'ph': (0, 14),
        'motion': (-10, 10),
        'pressure': (0, 1000)
    }
    
    if sensor_type not in ranges:
        return True  # No validation for unknown sensors
    
    min_val, max_val = ranges[sensor_type]
    return min_val <= value <= max_val