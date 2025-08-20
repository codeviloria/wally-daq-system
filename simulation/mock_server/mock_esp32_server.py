"""
Emulador local del ESP32 para desarrollo sin hardware
"""
import threading
import time
import random
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class MockESP32VernierSystem:
    """Emulador completo del sistema Vernier"""
    
    def __init__(self):
        self.active_sensor = 1
        self.reading_active = True
        self.reading_number = 0
        self.start_time = time.time()
        
        print("🔬 Mock ESP32 Vernier System inicializado")
    
    def generate_realistic_data(self):
        """Generar datos realistas con variaciones temporales"""
        current_time = time.time()
        time_diff = current_time - self.start_time
        
        # Temperatura: variación diaria simulada
        temp_base = 22 + 5 * math.sin(time_diff / 3600)
        temp_noise = random.gauss(0, 0.5)
        temperatura = temp_base + temp_noise
        
        # Fuerza: variación con picos ocasionales
        force_base = 10 + 20 * math.sin(time_diff / 60)
        force_spike = 30 if random.random() < 0.05 else 0
        fuerza = force_base + force_spike + random.gauss(0, 2)
        
        # Fotopuerta: eventos aleatorios
        photogate_blocked = random.random() < 0.1
        
        # Movimiento: distancia con movimiento realista
        distance_base = 15 + 10 * math.sin(time_diff / 30)
        distance = max(5, distance_base + random.gauss(0, 1))
        
        return {
            'vernier_temperatura': {
                'sensor_type': 'temperatura',
                'value': round(temperatura, 2),
                'unit': '°C',
                'status': 'active',
                'timestamp': current_time,
                'vernier_id': 1,
                'source': 'mock_simulation'
            },
            'vernier_fuerza': {
                'sensor_type': 'fuerza',
                'value': round(fuerza, 2),
                'unit': 'N',
                'status': 'active',
                'timestamp': current_time,
                'reading_number': self.reading_number,
                'led_status': fuerza > 25,
                'vernier_id': 2,
                'source': 'mock_simulation'
            },
            'vernier_fotopuerta': {
                'sensor_type': 'fotopuerta',
                'value': 0 if photogate_blocked else 1,
                'unit': 'blocked' if photogate_blocked else 'open',
                'status': 'active',
                'timestamp': current_time,
                'led_status': photogate_blocked,
                'vernier_id': 3,
                'source': 'mock_simulation'
            },
            'vernier_movimiento': {
                'sensor_type': 'movimiento',
                'value': round(distance, 2),
                'unit': 'cm',
                'status': 'active',
                'timestamp': current_time,
                'vernier_id': 4,
                'source': 'mock_simulation'
            }
        }
    
    def get_full_response(self):
        """Response completa compatible con Wally original"""
        readings = self.generate_realistic_data()
        self.reading_number += 1
        
        return {
            'device_id': 'mock_esp32_wally_system',
            'timestamp': time.time(),
            'readings': readings,
            'sensor_count': len([r for r in readings.values() if r['status'] == 'active']),
            'vernier_active_sensor': self.active_sensor,
            'vernier_reading_active': self.reading_active,
            'arduino_compatible': True,
            'simulation_info': {
                'platform': 'Python Mock Server',
                'uptime_seconds': time.time() - self.start_time,
                'total_readings': self.reading_number
            }
        }
    
    def handle_command(self, command):
        """Procesar comandos Arduino"""
        command_map = {
            't': (1, "Sensor changed to temperature"),
            'f': (2, "Sensor changed to force"),
            'p': (3, "Sensor changed to photogate"),
            'm': (4, "Sensor changed to motion"),
            'd': (None, "Readings stopped"),
            'c': (None, "Readings continued")
        }
        
        if command in command_map:
            if command == 'd':
                self.reading_active = False
            elif command == 'c':
                self.reading_active = True
            else:
                sensor_id, message = command_map[command]
                if sensor_id:
                    self.active_sensor = sensor_id
            
            return {
                'command': command,
                'result': command_map[command][1],
                'timestamp': time.time(),
                'active_sensor': self.active_sensor,
                'reading_active': self.reading_active
            }
        else:
            return {
                'command': command,
                'result': f"Unknown command: {command}",
                'timestamp': time.time(),
                'error': True
            }

class MockRequestHandler(BaseHTTPRequestHandler):
    """Handler para peticiones HTTP"""
    
    def log_message(self, format, *args):
        """Suprimir logs verbosos"""
        pass
    
    def do_GET(self):
        """Manejar peticiones GET"""
        try:
            if self.path == '/ping':
                self.send_json_response({
                    'pong': time.time(),
                    'message': 'Mock ESP32 server is running',
                    'platform': 'Python Emulator'
                })
            
            elif self.path == '/sensors':
                response = self.server.esp32_system.get_full_response()
                self.send_json_response(response)
            
            elif self.path.startswith('/vernier/command/'):
                command = self.path.split('/')[-1]
                response = self.server.esp32_system.handle_command(command)
                self.send_json_response(response)
            
            elif self.path == '/vernier/status':
                self.send_json_response({
                    'active_sensor': self.server.esp32_system.active_sensor,
                    'reading_active': self.server.esp32_system.reading_active,
                    'available_commands': ['t', 'f', 'p', 'm', 'd', 'c'],
                    'platform': 'Python Mock Server'
                })
            
            else:
                self.send_error(404, "Endpoint not found")
        
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def send_json_response(self, data):
        """Enviar respuesta JSON"""
        json_str = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(json_str))
        self.end_headers()
        self.wfile.write(json_str.encode('utf-8'))

def start_mock_server(host='localhost', port=8080):
    """Iniciar servidor mock"""
    esp32_system = MockESP32VernierSystem()
    
    server = HTTPServer((host, port), MockRequestHandler)
    server.esp32_system = esp32_system
    
    print(f"🌐 Mock ESP32 Server iniciado en http://{host}:{port}")
    print(f"📡 Endpoints disponibles:")
    print(f"   http://{host}:{port}/sensors")
    print(f"   http://{host}:{port}/ping")
    print(f"   http://{host}:{port}/vernier/command/[t|f|p|m|d|c]")
    print(f"🔄 Generando datos realistas...")
    print(f"🛑 Presionar Ctrl+C para detener")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    start_mock_server()
