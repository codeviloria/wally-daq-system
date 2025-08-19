"""
Data Manager para Wally - Gestión de datos y archivos
"""
import csv
import json
import time
from datetime import datetime
from collections import deque
import os
import config

class DataManager:
    """Gestor de datos del sistema Wally"""
    
    def __init__(self):
        self.data_buffer = deque(maxlen=config.MAX_BUFFER_SIZE)
        self.start_time = None
        self.reading_count = 0
        
        # Crear directorio de datos si no existe
        os.makedirs(config.DATA_DIRECTORY, exist_ok=True)
        
        print(f"📊 Data Manager inicializado - Buffer máximo: {config.MAX_BUFFER_SIZE}")
    
    def add_reading(self, data):
        """Agregar nueva lectura al buffer"""
        if not data:
            return
        
        # Marcar tiempo de inicio en primera lectura
        if self.start_time is None:
            self.start_time = time.time()
        
        # Preparar entrada para el buffer
        entry = {
            'timestamp': data.get('timestamp', time.time()),
            'device_id': data.get('device_id', 'unknown'),
            'readings': data.get('readings', {}),
            'sensor_count': data.get('sensor_count', 0),
            'memory_free': data.get('memory_free', 0),
            'entry_id': self.reading_count
        }
        
        # Agregar al buffer
        self.data_buffer.append(entry)
        self.reading_count += 1
        
        return True
    
    def get_recent_data(self, limit=None):
        """Obtener datos recientes del buffer"""
        if limit is None:
            return list(self.data_buffer)
        else:
            return list(self.data_buffer)[-limit:]
    
    def get_reading_count(self):
        """Obtener número total de lecturas"""
        return self.reading_count
    
    def get_stats(self):
        """Obtener estadísticas del sistema"""
        current_time = time.time()
        duration = current_time - self.start_time if self.start_time else 0
        
        # Calcular tasa de muestreo
        if duration > 0 and self.reading_count > 0:
            sample_rate = self.reading_count / duration
        else:
            sample_rate = 0
        
        # Estadísticas del buffer
        buffer_usage = len(self.data_buffer) / config.MAX_BUFFER_SIZE * 100
        
        return {
            'total_readings': self.reading_count,
            'buffer_size': len(self.data_buffer),
            'buffer_usage_percent': buffer_usage,
            'duration_seconds': duration,
            'sample_rate': sample_rate,
            'start_time': self.start_time,
            'current_time': current_time
        }
    
    def export_to_csv(self, filename):
        """Exportar datos a archivo CSV"""
        try:
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Headers
                fieldnames = [
                    'timestamp', 'datetime', 'device_id', 'entry_id',
                    'sensor_type', 'value', 'unit', 'voltage', 'raw', 'status'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Escribir datos
                exported_rows = 0
                for entry in self.data_buffer:
                    timestamp = entry['timestamp']
                    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    device_id = entry['device_id']
                    entry_id = entry['entry_id']
                    
                    # Una fila por sensor
                    for sensor_type, reading in entry['readings'].items():
                        row = {
                            'timestamp': timestamp,
                            'datetime': datetime_str,
                            'device_id': device_id,
                            'entry_id': entry_id,
                            'sensor_type': sensor_type,
                            'value': reading.get('value'),
                            'unit': reading.get('unit'),
                            'voltage': reading.get('voltage'),
                            'raw': reading.get('raw'),
                            'status': reading.get('status')
                        }
                        writer.writerow(row)
                        exported_rows += 1
                
            print(f"📁 CSV exportado: {filename} ({exported_rows} filas)")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando CSV: {e}")
            return False
    
    def export_to_json(self, filename):
        """Exportar datos a archivo JSON"""
        try:
            data_export = {
                'metadata': {
                    'export_time': datetime.now().isoformat(),
                    'total_readings': self.reading_count,
                    'duration_seconds': time.time() - self.start_time if self.start_time else 0,
                    'wally_version': config.VERSION
                },
                'stats': self.get_stats(),
                'readings': list(self.data_buffer)
            }
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data_export, jsonfile, indent=2, default=str)
            
            print(f"📁 JSON exportado: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exportando JSON: {e}")
            return False
    
    def clear_buffer(self):
        """Limpiar buffer de datos"""
        self.data_buffer.clear()
        print("🗑️ Buffer de datos limpiado")
    
    def reset_stats(self):
        """Resetear estadísticas"""
        self.start_time = None
        self.reading_count = 0
        self.clear_buffer()
        print("🔄 Estadísticas reseteadas")