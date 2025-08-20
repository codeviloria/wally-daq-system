#!/bin/bash
# Script para crear estructura completa de simulación
# Ejecutar desde la raíz del repositorio wally-daq-system

echo "🔬 Creando estructura de simulación Wally DAQ System..."

# Crear directorios
echo "📁 Creando directorios..."
mkdir -p simulation/wokwi
mkdir -p simulation/mock_server  
mkdir -p simulation/testing
mkdir -p docs

echo "✅ Directorios creados:"
echo "  📁 simulation/"
echo "     ├── 🌟 wokwi/"
echo "     ├── 🛠️ mock_server/"
echo "     └── 🧪 testing/"

# Crear archivos principales
echo ""
echo "📄 Creando archivos de simulación..."

# ===== SIMULATION/WOKWI/MAIN.PY =====
cat > simulation/wokwi/main.py << 'EOF'
"""
Wally ESP32 Sensor Server - Versión Simulación Wokwi
Compatible con sistema original + simulación virtual
"""
import machine
import network
import socket
import ujson
import time
import math

# ===== CONFIGURACIÓN WOKWI =====
WIFI_SSID = "Wokwi-GUEST"      # WiFi automático de Wokwi
WIFI_PASSWORD = ""             # Sin contraseña en Wokwi
SERVER_PORT = 8080

# Constantes sensores Vernier (compatibilidad Arduino)
SENSOR_TEMPERATURA = 1
SENSOR_FUERZA = 2
SENSOR_FOTOPUERTA = 3
SENSOR_MOVIMIENTO = 4

class WokwiVernierManager:
    """Manager de sensores Vernier adaptado para Wokwi"""
    
    def __init__(self):
        print("🔬 Inicializando Wokwi Vernier Manager...")
        
        # Configurar pines hardware (mapeo Arduino → ESP32)
        self.setup_hardware()
        
        # Variables de estado (migradas del Arduino)
        self.sensor_seleccionado = SENSOR_TEMPERATURA
        self.lectura_activa = True
        self.reading_number = 0
        self.threshold = 100.0
        
        print("✅ Wokwi Vernier Manager configurado")
        self.print_simulation_info()
    
    def setup_hardware(self):
        """Configurar hardware para simulación Wokwi"""
        try:
            # ADCs para sensores analógicos
            self.adc_temperatura = machine.ADC(machine.Pin(34))  # Potenciómetro 1
            self.adc_fuerza = machine.ADC(machine.Pin(35))       # Potenciómetro 2
            self.adc_temperatura.atten(machine.ADC.ATTN_11DB)
            self.adc_fuerza.atten(machine.ADC.ATTN_11DB)
            
            # GPIO digitales
            self.led_status = machine.Pin(2, machine.Pin.OUT)    # LED integrado
            self.photogate_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)  # Botón
            
            print("🔧 Hardware configurado para simulación")
            
        except Exception as e:
            print(f"❌ Error configurando hardware: {e}")
    
    def print_simulation_info(self):
        """Mostrar información de simulación"""
        print("\n" + "="*50)
        print("🎮 WALLY DAQ SYSTEM - SIMULACIÓN WOKWI")
        print("="*50)
        print("📋 Componentes virtuales:")
        print("  🌡️  Potenciómetro 1 (GPIO34) → Sensor Temperatura")
        print("  ⚡  Potenciómetro 2 (GPIO35) → Sensor Fuerza")  
        print("  📷  Botón azul (GPIO4) → Fotopuerta")
        print("  📐  Automático → Sensor Movimiento")
        print("  💡  LED integrado (GPIO2) → Indicador estado")
        print("\n🎛️ Comandos disponibles:")
        print("  t, f, p, m, d, c")
        print("="*50 + "\n")
    
    def read_sensor_vernier(self, sensor_type):
        """Leer sensor específico"""
        if sensor_type == SENSOR_TEMPERATURA:
            raw = self.adc_temperatura.read()
            voltage = raw * 3.3 / 4095
            temperatura = 15 + (voltage / 3.3) * 20  # 15-35°C
            
            return {
                'sensor_type': 'temperatura',
                'value': round(temperatura, 2),
                'unit': '°C',
                'voltage': round(voltage, 3),
                'raw': raw,
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_TEMPERATURA
            }
        
        elif sensor_type == SENSOR_FUERZA:
            raw = self.adc_fuerza.read()
            voltage = raw * 3.3 / 4095
            fuerza = -10 + (voltage / 3.3) * 60  # -10N a 50N
            
            # Control LED
            if abs(fuerza) > 15:
                self.led_status.on()
            else:
                self.led_status.off()
            
            return {
                'sensor_type': 'fuerza',
                'value': round(fuerza, 2),
                'unit': 'N',
                'voltage': round(voltage, 3),
                'raw': raw,
                'led_status': abs(fuerza) > 15,
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_FUERZA
            }
        
        elif sensor_type == SENSOR_FOTOPUERTA:
            button_state = self.photogate_pin.value()
            blocked = button_state == 0
            
            if blocked:
                self.led_status.on()
            else:
                self.led_status.off()
            
            return {
                'sensor_type': 'fotopuerta',
                'value': 0 if blocked else 1,
                'unit': 'blocked' if blocked else 'open',
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_FOTOPUERTA
            }
        
        elif sensor_type == SENSOR_MOVIMIENTO:
            # Simular distancia variable
            time_factor = time.ticks_ms() / 1000
            distance = 15 + 10 * math.sin(time_factor / 5)
            
            return {
                'sensor_type': 'movimiento',
                'value': round(distance, 2),
                'unit': 'cm',
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_MOVIMIENTO
            }
        
        return None
    
    def handle_arduino_command(self, command):
        """Manejar comandos Arduino"""
        commands = {
            't': (SENSOR_TEMPERATURA, "Sensor changed to temperature"),
            'f': (SENSOR_FUERZA, "Sensor changed to force"),
            'p': (SENSOR_FOTOPUERTA, "Sensor changed to photogate"),
            'm': (SENSOR_MOVIMIENTO, "Sensor changed to motion"),
            'd': (None, "Readings stopped"),
            'c': (None, "Readings continued")
        }
        
        if command in commands:
            if command == 'd':
                self.lectura_activa = False
            elif command == 'c':
                self.lectura_activa = True
            else:
                sensor_id, message = commands[command]
                if sensor_id:
                    self.sensor_seleccionado = sensor_id
            
            return commands[command][1]
        
        return f"Unknown command: {command}"

class WokwiHTTPServer:
    """Servidor HTTP compatible con Wally original"""
    
    def __init__(self, vernier_manager):
        self.vernier = vernier_manager
    
    def handle_request(self, request):
        """Procesar petición HTTP"""
        try:
            lines = request.split('\n')
            request_line = lines[0].strip()
            path = request_line.split()[1]
            
            if path == '/ping':
                data = {'pong': time.time(), 'platform': 'Wokwi ESP32'}
            elif path == '/sensors':
                data = self.get_all_sensors()
            elif path.startswith('/vernier/command/'):
                command = path.split('/')[-1]
                result = self.vernier.handle_arduino_command(command)
                data = {'command': command, 'result': result, 'timestamp': time.time()}
            elif path == '/vernier/status':
                data = {
                    'active_sensor': self.vernier.sensor_seleccionado,
                    'reading_active': self.vernier.lectura_activa,
                    'platform': 'Wokwi Simulation'
                }
            else:
                return self.error_response(404, "Not Found")
            
            return self.json_response(data)
            
        except Exception as e:
            return self.error_response(500, str(e))
    
    def get_all_sensors(self):
        """Obtener todos los sensores"""
        readings = {}
        
        for sensor_id in [SENSOR_TEMPERATURA, SENSOR_FUERZA, SENSOR_FOTOPUERTA, SENSOR_MOVIMIENTO]:
            sensor_names = {1: 'vernier_temperatura', 2: 'vernier_fuerza', 
                          3: 'vernier_fotopuerta', 4: 'vernier_movimiento'}
            sensor_name = sensor_names[sensor_id]
            readings[sensor_name] = self.vernier.read_sensor_vernier(sensor_id)
        
        return {
            'device_id': 'wokwi_esp32_wally',
            'timestamp': time.time(),
            'readings': readings,
            'sensor_count': 4,
            'arduino_compatible': True,
            'simulation': True
        }
    
    def json_response(self, data):
        """Crear respuesta JSON"""
        json_str = ujson.dumps(data)
        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            f"Content-Length: {len(json_str)}\r\n"
            "\r\n"
            f"{json_str}"
        )
    
    def error_response(self, code, message):
        """Respuesta de error"""
        return (
            f"HTTP/1.1 {code} {message}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(message)}\r\n"
            "\r\n"
            f"{message}"
        )
    
    def start_server(self, ip, port):
        """Iniciar servidor HTTP"""
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socket_server.bind(('', port))
            socket_server.listen(5)
            
            print(f"🌐 Wokwi HTTP Server iniciado en {ip}:{port}")
            print(f"🔗 Usar localhost:9080 con IoT Gateway")
            
            while True:
                try:
                    conn, addr = socket_server.accept()
                    request = conn.recv(1024).decode('utf-8')
                    response = self.handle_request(request)
                    conn.send(response.encode('utf-8'))
                    conn.close()
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Error servidor: {e}")

def main():
    """Función principal para simulación Wokwi"""
    print("🔬 Iniciando Wally ESP32 Sensor Server - Simulación Wokwi...")
    
    # Conectar WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not wlan.isconnected():
        time.sleep(0.1)
    
    ip = wlan.ifconfig()[0]
    print(f"✅ WiFi conectado - IP: {ip}")
    
    # Inicializar componentes
    vernier_manager = WokwiVernierManager()
    http_server = WokwiHTTPServer(vernier_manager)
    
    # Iniciar servidor
    http_server.start_server(ip, SERVER_PORT)

if __name__ == "__main__":
    main()
EOF

# ===== SIMULATION/WOKWI/DIAGRAM.JSON =====
cat > simulation/wokwi/diagram.json << 'EOF'
{
  "version": 1,
  "author": "Wally DAQ Simulation",
  "editor": "wokwi",
  "parts": [
    {
      "type": "wokwi-esp32-devkit-v1",
      "id": "esp",
      "top": 0,
      "left": 0,
      "attrs": {}
    },
    {
      "type": "wokwi-potentiometer",
      "id": "pot_temp",
      "top": 100,
      "left": 300,
      "attrs": {"label": "Temperature Sensor"}
    },
    {
      "type": "wokwi-potentiometer", 
      "id": "pot_force",
      "top": 200,
      "left": 300,
      "attrs": {"label": "Force Sensor"}
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn_photogate",
      "top": 300,
      "left": 300,
      "attrs": {"label": "Photogate", "color": "blue"}
    },
    {
      "type": "wokwi-led",
      "id": "led_status",
      "top": 400,
      "left": 300,
      "attrs": {"color": "red", "label": "Status LED"}
    }
  ],
  "connections": [
    ["esp:GPIO34", "pot_temp:SIG", "green", []],
    ["esp:GPIO35", "pot_force:SIG", "blue", []],
    ["esp:GPIO4", "btn_photogate:1.l", "yellow", []],
    ["esp:GPIO2", "led_status:A", "red", []],
    ["esp:3V3", "pot_temp:VCC", "red", []],
    ["esp:3V3", "pot_force:VCC", "red", []],
    ["esp:GND", "pot_temp:GND", "black", []],
    ["esp:GND", "pot_force:GND", "black", []],
    ["esp:GND", "btn_photogate:2.l", "black", []],
    ["esp:GND", "led_status:C", "black", []]
  ],
  "dependencies": {}
}
EOF

echo "✅ Archivos Wokwi creados:"
echo "  📄 simulation/wokwi/main.py"
echo "  📄 simulation/wokwi/diagram.json"

# ===== SIMULATION/MOCK_SERVER/MOCK_ESP32_SERVER.PY =====
cat > simulation/mock_server/mock_esp32_server.py << 'EOF'
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
EOF

echo "✅ Mock server creado:"
echo "  📄 simulation/mock_server/mock_esp32_server.py"

# ===== SIMULATION/TESTING/TEST_SIMULATION.PY =====
cat > simulation/testing/test_simulation.py << 'EOF'
"""
Suite de testing para validar simulación Wally DAQ
"""
import requests
import time
import json

class TestWallySimulation:
    """Tests para validar funcionalidad completa"""
    
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        
    def test_connectivity(self):
        """Test conectividad básica"""
        try:
            response = requests.get(f"{self.base_url}/ping", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'pong' in data
            print("✅ Conectividad OK")
            return True
        except Exception as e:
            print(f"❌ Conectividad falló: {e}")
            return False
    
    def test_sensors_endpoint(self):
        """Test endpoint principal de sensores"""
        try:
            response = requests.get(f"{self.base_url}/sensors")
            assert response.status_code == 200
            data = response.json()
            
            # Validar estructura
            assert 'device_id' in data
            assert 'readings' in data
            assert 'arduino_compatible' in data
            
            # Validar sensores Vernier
            expected_sensors = ['vernier_temperatura', 'vernier_fuerza', 
                              'vernier_fotopuerta', 'vernier_movimiento']
            
            for sensor in expected_sensors:
                assert sensor in data['readings']
                sensor_data = data['readings'][sensor]
                assert 'value' in sensor_data
                assert 'unit' in sensor_data
                assert 'status' in sensor_data
            
            print("✅ Endpoint /sensors OK")
            return True
        except Exception as e:
            print(f"❌ Test sensors falló: {e}")
            return False
    
    def test_arduino_commands(self):
        """Test comandos Arduino compatibles"""
        commands = ['t', 'f', 'p', 'm', 'd', 'c']
        results = []
        
        for cmd in commands:
            try:
                response = requests.get(f"{self.base_url}/vernier/command/{cmd}")
                assert response.status_code == 200
                data = response.json()
                assert 'command' in data
                assert 'result' in data
                results.append(f"✅ Comando '{cmd}': {data['result']}")
            except Exception as e:
                results.append(f"❌ Comando '{cmd}' falló: {e}")
        
        for result in results:
            print(result)
        
        return all("✅" in r for r in results)
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        tests = [
            ("Conectividad", self.test_connectivity),
            ("Endpoint Sensores", self.test_sensors_endpoint),
            ("Comandos Arduino", self.test_arduino_commands)
        ]
        
        print("🧪 Iniciando Test Suite Wally Simulation")
        print("=" * 50)
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 Ejecutando: {test_name}")
            result = test_func()
            results.append((test_name, result))
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print("📋 RESULTADOS FINALES:")
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} - {test_name}")
            if result:
                passed += 1
        
        print(f"\n🎯 Tests pasados: {passed}/{len(tests)}")
        
        if passed == len(tests):
            print("🎉 ¡Todos los tests pasaron! Sistema listo para uso.")
        else:
            print("⚠️ Algunos tests fallaron. Revisar configuración.")
        
        return passed == len(tests)

if __name__ == "__main__":
    import sys
    
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    print(f"🎯 Testing simulación en: {url}")
    tester = TestWallySimulation(url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)
EOF

echo "✅ Test suite creado:"
echo "  📄 simulation/testing/test_simulation.py"

# ===== SIMULATION/TESTING/DIAGNOSE_SYSTEM.PY =====
cat > simulation/testing/diagnose_system.py << 'EOF'
"""
Script de diagnóstico automático del sistema Wally
"""
import requests
import socket
import sys

def check_port(host, port):
    """Verificar si puerto está abierto"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def diagnose_wally_system():
    """Diagnóstico completo del sistema"""
    print("🔍 Diagnóstico Sistema Wally DAQ")
    print("=" * 40)
    
    # Check Python
    print(f"🐍 Python: {sys.version}")
    
    # Check dependencias
    try:
        import requests, matplotlib, tkinter
        print("✅ Dependencias Python OK")
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
    
    # Check puertos
    ports_to_check = [8080, 9080]
    for port in ports_to_check:
        if check_port('localhost', port):
            print(f"✅ Puerto {port} abierto")
        else:
            print(f"❌ Puerto {port} cerrado")
    
    # Check endpoints
    base_urls = ['http://localhost:8080', 'http://localhost:9080']
    
    for url in base_urls:
        try:
            response = requests.get(f"{url}/ping", timeout=2)
            if response.status_code == 200:
                print(f"✅ Servidor disponible en {url}")
                
                # Test endpoints principales
                endpoints = ['/sensors', '/vernier/status']
                for endpoint in endpoints:
                    try:
                        r = requests.get(f"{url}{endpoint}", timeout=2)
                        print(f"  ✅ {endpoint}: {r.status_code}")
                    except:
                        print(f"  ❌ {endpoint}: Error")
            else:
                print(f"❌ Servidor en {url}: HTTP {response.status_code}")
        except:
            print(f"❌ No hay servidor en {url}")
    
    print("\n💡 Recomendaciones:")
    print("1. Si usas Wokwi: verificar IoT Gateway ejecutándose")
    print("2. Si usas Mock: verificar python mock_esp32_server.py") 
    print("3. Cliente PC: verificar ESP32_IP en config.py")

if __name__ == "__main__":
    diagnose_wally_system()
EOF

echo "✅ Diagnóstico creado:"
echo "  📄 simulation/testing/diagnose_system.py"

# ===== README SIMULACIÓN =====
cat > simulation/README.md << 'EOF'
# 🎮 Simulación Wally DAQ System

Este directorio contiene todos los archivos necesarios para simular el sistema Wally DAQ sin hardware físico.

## 📁 Estructura

```
simulation/
├── 🌟 wokwi/                    # Simulación online Wokwi
│   ├── main.py                  # Código ESP32 para Wokwi
│   └── diagram.json             # Configuración componentes virtuales
├── 🛠️ mock_server/              # Emulador Python local
│   └── mock_esp32_server.py     # Servidor mock completo
└── 🧪 testing/                  # Scripts de testing
    ├── test_simulation.py       # Suite de validación
    └── diagnose_system.py       # Diagnóstico automático
```

## 🚀 Quick Start

### 🌟 Opción 1: Wokwi (Online)
```bash
1. Ir a: https://wokwi.com/projects/new/micropython-esp32
2. Copiar contenido de: wokwi/main.py
3. Copiar contenido de: wokwi/diagram.json
4. Iniciar simulación
```

### 🛠️ Opción 2: Mock Server (Local)
```bash
# Ejecutar emulador
python simulation/mock_server/mock_esp32_server.py

# En otra terminal: ejecutar cliente
cd pc_controller
python main.py
```

## 🧪 Testing

```bash
# Test automático
python simulation/testing/test_simulation.py

# Diagnóstico
python simulation/testing/diagnose_system.py
```

## 📚 Documentación Completa

Ver: [docs/simulation-guide.md](../docs/simulation-guide.md)
EOF

echo "✅ README simulación creado:"
echo "  📄 simulation/README.md"

echo ""
echo "🎉 ¡Estructura de simulación creada exitosamente!"
echo ""
echo "📋 Resumen de archivos creados:"
echo "  📁 simulation/"
echo "     ├── 🌟 wokwi/"
echo "     │   ├── main.py (código ESP32 para Wokwi)"
echo "     │   └── diagram.json (componentes virtuales)"
echo "     ├── 🛠️ mock_server/"
echo "     │   └── mock_esp32_server.py (emulador Python)"
echo "     ├── 🧪 testing/"
echo "     │   ├── test_simulation.py (suite de testing)"
echo "     │   └── diagnose_system.py (diagnóstico)"
echo "     └── README.md (documentación simulación)"
echo ""
echo "🚀 Próximos pasos:"
echo "1. ⚡ Probar mock server: python simulation/mock_server/mock_esp32_server.py"
echo "2. 🧪 Ejecutar tests: python simulation/testing/test_simulation.py"
echo "3. 🌟 Probar Wokwi: copiar archivos a https://wokwi.com"
echo "4. 📝 Actualizar README principal con enlaces a simulación"
echo ""
echo "✅ ¡Todo listo para simular sin hardware!"
