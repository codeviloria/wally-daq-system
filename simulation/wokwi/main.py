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
