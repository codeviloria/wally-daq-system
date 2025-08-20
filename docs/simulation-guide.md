# 🎮 Simulación Wally DAQ System - Guía Completa

## 📖 Índice
- [🎯 Introducción](#-introducción)
- [🌟 Simulación Principal: Wokwi](#-simulación-principal-wokwi)
- [🛠️ Simuladores Alternativos](#️-simuladores-alternativos)
- [🧪 Testing y Validación](#-testing-y-validación)
- [🔧 Troubleshooting](#-troubleshooting)
- [📚 Recursos Adicionales](#-recursos-adicionales)

---

## 🎯 Introducción

Esta guía te permitirá **simular completamente el sistema Wally DAQ** sin necesidad de hardware físico ESP32 ni sensores Vernier. Podrás:

✅ **Probar la migración Arduino → ESP32** completa  
✅ **Validar toda la funcionalidad** antes del hardware real  
✅ **Desarrollar y debuggear** sin limitaciones físicas  
✅ **Enseñar y demostrar** el sistema sin equipos  
✅ **Testing automatizado** de endpoints y funciones  

### 🎯 **Objetivos de la Simulación:**
- **Educativos**: Entender migración Arduino a ESP32 + MicroPython
- **Desarrollo**: Prototipar rápidamente sin hardware
- **Validación**: Probar sistema completo antes de implementación
- **Demostración**: Mostrar capacidades sin inversión en equipos

### 📋 **Prerequisitos:**
- Navegador web moderno (Chrome, Firefox, Edge)
- Conexión a internet estable
- Python 3.8+ (para cliente PC)
- Conocimientos básicos de HTTP/JSON

---

## 🌟 Simulación Principal: Wokwi

**Wokwi** es la opción recomendada por su simplicidad, funcionalidad completa y compatibilidad nativa con ESP32 + MicroPython.

### 🚀 **Paso 1: Configuración Inicial Wokwi**

#### **1.1. Crear Proyecto Base**
```bash
1. Ir a: https://wokwi.com/projects/new/micropython-esp32
2. Título: "Wally DAQ System - ESP32 Simulation"
3. Descripción: "Migración Arduino a ESP32 con sensores Vernier simulados"
```

#### **1.2. Configurar main.py**
Copiar el siguiente código en el archivo `main.py` de Wokwi:

```python
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
        
        # Variables específicas
        self.time_ms = 0
        self.time_us = 0
        self.photogate_status = 1
        
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
            self.trigger_pin = machine.Pin(5, machine.Pin.OUT)   # Trigger ultrasonido
            self.echo_pin = machine.Pin(18, machine.Pin.IN)      # Echo ultrasonido
            
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
        print("  📷  Botón azul (GPIO4) → Fotopuerta (presionar = bloquear)")
        print("  📐  Automático → Sensor Movimiento (distancia variable)")
        print("  💡  LED integrado (GPIO2) → Indicador estado")
        print("\n🎛️ Comandos disponibles (compatibles Arduino):")
        print("  t → Cambiar a sensor temperatura")
        print("  f → Cambiar a sensor fuerza")
        print("  p → Cambiar a fotopuerta")
        print("  m → Cambiar a sensor movimiento")
        print("  d → Detener lecturas")
        print("  c → Continuar lecturas")
        print("\n📡 Endpoints HTTP:")
        print("  /sensors → Todos los sensores")
        print("  /vernier/command/[t|f|p|m|d|c] → Comandos Arduino")
        print("  /vernier/status → Estado del sistema")
        print("  /ping → Test conectividad")
        print("="*50 + "\n")
    
    def read_temperatura_simulation(self):
        """Simular sensor temperatura TMP36 (rango realista)"""
        try:
            raw_value = self.adc_temperatura.read()
            voltage = raw_value * 3.3 / 4095
            
            # Simular rango realista: 15°C a 35°C basado en potenciómetro
            temperatura_base = 15 + (voltage / 3.3) * 20
            # Agregar variación pequeña para simular ruido real
            temperatura = temperatura_base + (time.ticks_ms() % 100 - 50) / 100
            
            return {
                'sensor_type': 'temperatura',
                'value': round(temperatura, 2),
                'unit': '°C',
                'voltage': round(voltage, 3),
                'raw': raw_value,
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_TEMPERATURA,
                'simulation_note': 'Adjust potentiometer to change temperature'
            }
        except Exception as e:
            return self.error_reading('temperatura', str(e))
    
    def read_fuerza_simulation(self):
        """Simular sensor fuerza Vernier con control LED"""
        try:
            raw_value = self.adc_fuerza.read()
            voltage = raw_value * 3.3 / 4095
            
            # Simular rango Dual-Range Force Sensor: -10N a +50N
            fuerza_base = -10 + (voltage / 3.3) * 60
            # Agregar pequeña oscilación para simular medición real
            fuerza = fuerza_base + 2 * math.sin(time.ticks_ms() / 1000)
            
            # Control LED según threshold (funcionalidad Arduino original)
            led_active = abs(fuerza) > self.threshold / 10  # Ajustar threshold para simulación
            if led_active:
                self.led_status.on()
            else:
                self.led_status.off()
            
            self.reading_number += 1
            
            return {
                'sensor_type': 'fuerza',
                'value': round(fuerza, 2),
                'unit': 'N',
                'voltage': round(voltage, 3),
                'raw': raw_value,
                'status': 'active',
                'timestamp': time.time(),
                'threshold': self.threshold,
                'reading_number': self.reading_number,
                'led_status': led_active,
                'vernier_id': SENSOR_FUERZA,
                'simulation_note': 'LED activates when force > threshold'
            }
        except Exception as e:
            return self.error_reading('fuerza', str(e))
    
    def read_fotopuerta_simulation(self):
        """Simular fotopuerta con botón (presionar = bloquear)"""
        try:
            # Leer botón (LOW cuando presionado = bloqueado)
            button_state = self.photogate_pin.value()
            photogate_blocked = button_state == 0
            
            # Control LED (encender cuando bloqueada)
            if photogate_blocked:
                self.led_status.on()
                if self.photogate_status == 1:  # Cambio de estado
                    self.time_ms = time.ticks_ms()
                    self.time_us = time.ticks_us()
            else:
                self.led_status.off()
            
            self.photogate_status = button_state
            
            return {
                'sensor_type': 'fotopuerta',
                'value': 0 if photogate_blocked else 1,
                'unit': 'blocked' if photogate_blocked else 'open',
                'status': 'active',
                'timestamp': time.time(),
                'time_ms': self.time_ms,
                'time_us': self.time_us,
                'button_pressed': photogate_blocked,
                'led_status': photogate_blocked,
                'vernier_id': SENSOR_FOTOPUERTA,
                'simulation_note': 'Press blue button to block photogate'
            }
        except Exception as e:
            return self.error_reading('fotopuerta', str(e))
    
    def read_movimiento_simulation(self):
        """Simular sensor ultrasonido HC-SR04 con distancia variable"""
        try:
            # Simular distancia variable basada en tiempo (5cm a 30cm)
            time_factor = time.ticks_ms() / 1000
            distance_base = 15 + 10 * math.sin(time_factor / 5)  # Oscilación lenta
            distance_noise = 2 * math.sin(time_factor * 3)       # Ruido rápido
            distance = max(5, distance_base + distance_noise)    # Mínimo 5cm
            
            # Simular duration del pulso ultrasonido
            duration_us = int(distance * 58)  # Fórmula estándar HC-SR04
            
            return {
                'sensor_type': 'movimiento',
                'value': round(distance, 2),
                'unit': 'cm',
                'status': 'active',
                'timestamp': time.time(),
                'duration_us': duration_us,
                'vernier_id': SENSOR_MOVIMIENTO,
                'simulation_note': 'Auto-varying distance 5-30cm'
            }
        except Exception as e:
            return self.error_reading('movimiento', str(e))
    
    def error_reading(self, sensor_type, error_msg):
        """Generar lectura de error estándar"""
        return {
            'sensor_type': sensor_type,
            'value': None,
            'unit': None,
            'status': 'error',
            'error': error_msg,
            'timestamp': time.time()
        }
    
    def read_sensor_vernier(self, sensor_type):
        """Leer sensor específico (interfaz compatible Arduino)"""
        if sensor_type == SENSOR_TEMPERATURA:
            return self.read_temperatura_simulation()
        elif sensor_type == SENSOR_FUERZA:
            return self.read_fuerza_simulation()
        elif sensor_type == SENSOR_FOTOPUERTA:
            return self.read_fotopuerta_simulation()
        elif sensor_type == SENSOR_MOVIMIENTO:
            return self.read_movimiento_simulation()
        else:
            return self.error_reading('unknown', f'Sensor type {sensor_type} not supported')
    
    def handle_arduino_command(self, command):
        """Manejar comandos Arduino originales"""
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
                self.sensor_seleccionado = sensor_id
                print(f"📊 {message}")
            
            return commands[command][1]
        else:
            return f"Unknown command: {command}"

class WokwiHTTPServer:
    """Servidor HTTP compatible con sistema Wally original"""
    
    def __init__(self, vernier_manager):
        self.vernier = vernier_manager
        self.socket = None
        
    def handle_request(self, request):
        """Procesar petición HTTP"""
        try:
            lines = request.split('\n')
            if not lines:
                return self.http_error(400, "Bad Request")
            
            request_line = lines[0].strip()
            parts = request_line.split()
            
            if len(parts) < 2:
                return self.http_error(400, "Bad Request")
            
            method, path = parts[0], parts[1]
            
            if method == "GET":
                return self.route_get_request(path)
            else:
                return self.http_error(405, "Method Not Allowed")
                
        except Exception as e:
            return self.http_error(500, f"Internal Server Error: {e}")
    
    def route_get_request(self, path):
        """Enrutar peticiones GET"""
        if path == "/" or path == "/sensors":
            return self.endpoint_sensors()
        elif path == "/status":
            return self.endpoint_status()
        elif path == "/ping":
            return self.endpoint_ping()
        elif path.startswith("/vernier/command/"):
            command = path.split("/")[-1]
            return self.endpoint_vernier_command(command)
        elif path == "/vernier/status":
            return self.endpoint_vernier_status()
        elif path == "/vernier/active":
            return self.endpoint_vernier_active()
        else:
            return self.http_error(404, "Not Found")
    
    def endpoint_sensors(self):
        """Endpoint principal: todos los sensores"""
        data = {
            'device_id': 'wokwi_esp32_wally_simulation',
            'timestamp': time.time(),
            'readings': {
                'vernier_temperatura': self.vernier.read_temperatura_simulation(),
                'vernier_fuerza': self.vernier.read_fuerza_simulation(),
                'vernier_fotopuerta': self.vernier.read_fotopuerta_simulation(),
                'vernier_movimiento': self.vernier.read_movimiento_simulation(),
                'current_active': self.vernier.read_sensor_vernier(self.vernier.sensor_seleccionado)
            },
            'sensor_count': 4,
            'vernier_active_sensor': self.vernier.sensor_seleccionado,
            'vernier_reading_active': self.vernier.lectura_activa,
            'arduino_compatible': True,
            'simulation_platform': 'Wokwi ESP32',
            'simulation_info': {
                'note': 'This is a virtual simulation of the Wally DAQ System',
                'components': 'ESP32 + Virtual Vernier Sensors',
                'interaction': 'Use potentiometers and button to change sensor values'
            }
        }
        return self.json_response(data)
    
    def endpoint_vernier_command(self, command):
        """Endpoint para comandos Arduino"""
        result = self.vernier.handle_arduino_command(command)
        
        response_data = {
            'command': command,
            'result': result,
            'timestamp': time.time(),
            'active_sensor': self.vernier.sensor_seleccionado,
            'reading_active': self.vernier.lectura_activa,
            'simulation': True
        }
        
        return self.json_response(response_data)
    
    def endpoint_vernier_status(self):
        """Status específico del sistema Vernier"""
        status = {
            'vernier_manager': {
                'active_sensor': self.vernier.sensor_seleccionado,
                'reading_active': self.vernier.lectura_activa,
                'reading_number': self.vernier.reading_number,
                'threshold': self.vernier.threshold
            },
            'sensor_mapping': {
                'temperatura': SENSOR_TEMPERATURA,
                'fuerza': SENSOR_FUERZA,
                'fotopuerta': SENSOR_FOTOPUERTA,
                'movimiento': SENSOR_MOVIMIENTO
            },
            'available_commands': ['t', 'f', 'p', 'm', 'd', 'c'],
            'simulation_platform': 'Wokwi ESP32 Virtual Environment',
            'arduino_compatibility': '100% compatible with original commands'
        }
        
        return self.json_response(status)
    
    def endpoint_vernier_active(self):
        """Solo el sensor activo actual"""
        if self.vernier.lectura_activa:
            reading = self.vernier.read_sensor_vernier(self.vernier.sensor_seleccionado)
            if reading:
                reading['is_active_sensor'] = True
            data = reading or {'error': 'No reading available'}
        else:
            data = {
                'status': 'readings_paused',
                'active_sensor': self.vernier.sensor_seleccionado,
                'message': 'Use command "c" to continue readings'
            }
        
        return self.json_response(data)
    
    def endpoint_status(self):
        """Status general del sistema"""
        status = {
            'device_id': 'wokwi_esp32_wally_simulation',
            'status': 'running',
            'uptime': time.ticks_ms() / 1000,
            'platform': 'Wokwi ESP32 Simulator',
            'vernier_sensors': 4,
            'arduino_compatible': True,
            'simulation': True,
            'endpoints': ['/sensors', '/ping', '/vernier/command/*', '/vernier/status']
        }
        
        return self.json_response(status)
    
    def endpoint_ping(self):
        """Test de conectividad"""
        return self.json_response({
            'pong': time.time(),
            'message': 'Wokwi simulation is running',
            'platform': 'ESP32 Virtual'
        })
    
    def json_response(self, data):
        """Crear respuesta JSON estándar"""
        json_data = ujson.dumps(data)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Cache-Control: no-cache\r\n"
            f"Content-Length: {len(json_data)}\r\n"
            "\r\n"
            f"{json_data}"
        )
        return response
    
    def http_error(self, code, message):
        """Respuesta de error HTTP"""
        response = (
            f"HTTP/1.1 {code} {message}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(message)}\r\n"
            "\r\n"
            f"{message}"
        )
        return response
    
    def start_server(self, ip, port):
        """Iniciar servidor HTTP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', port))
            self.socket.listen(5)
            
            print(f"🌐 Wokwi HTTP Server iniciado en {ip}:{port}")
            print(f"🔗 Para acceso externo usar: http://localhost:9080")
            print(f"📋 Wokwi IoT Gateway requerido para HTTP desde navegador")
            print(f"💡 Documentación: https://docs.wokwi.com/guides/esp32-wifi")
            
            while True:
                try:
                    self.socket.settimeout(1.0)
                    conn, addr = self.socket.accept()
                    
                    conn.settimeout(2.0)
                    request = conn.recv(1024).decode('utf-8')
                    
                    response = self.handle_request(request)
                    conn.send(response.encode('utf-8'))
                    
                    conn.close()
                    
                except OSError:
                    continue
                except Exception as e:
                    print(f"❌ Error en servidor: {e}")
                    if 'conn' in locals():
                        conn.close()
                    
        except Exception as e:
            print(f"❌ Error fatal en servidor: {e}")
        finally:
            if self.socket:
                self.socket.close()

def main():
    """Función principal para simulación Wokwi"""
    print("🔬 Iniciando Wally ESP32 Sensor Server - Simulación Wokwi...")
    
    # Conectar WiFi (automático en Wokwi)
    print("📡 Conectando a WiFi Wokwi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    # Esperar conexión
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1
        print(".", end="")
    
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"\n✅ WiFi conectado - IP simulada: {ip}")
        
        # Inicializar componentes
        vernier_manager = WokwiVernierManager()
        http_server = WokwiHTTPServer(vernier_manager)
        
        # Iniciar servidor
        print("🚀 Iniciando servidor HTTP...")
        http_server.start_server(ip, SERVER_PORT)
        
    else:
        print("\n❌ Error conectando WiFi en simulación")

# Ejecutar programa principal
if __name__ == "__main__":
    main()
```

#### **1.3. Configurar diagram.json**
Crear el archivo `diagram.json` para definir los componentes virtuales:

```json
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
```

### 🎮 **Paso 2: Interacción con la Simulación**

#### **2.1. Controles Virtuales**
- **🎛️ Potenciómetro 1 (Verde)**: Ajustar temperatura simulada (15-35°C)
- **🎛️ Potenciómetro 2 (Azul)**: Ajustar fuerza simulada (-10N a +50N)
- **🔵 Botón Azul**: Presionar = fotopuerta bloqueada
- **🔴 LED Rojo**: Indica estado de sensores
- **📐 Ultrasonido**: Distancia automática variable (5-30cm)

#### **2.2. Comandos HTTP Disponibles**
```bash
# Testing básico
curl http://localhost:9080/ping
curl http://localhost:9080/sensors

# Comandos Arduino compatibles
curl http://localhost:9080/vernier/command/t    # Cambiar a temperatura
curl http://localhost:9080/vernier/command/f    # Cambiar a fuerza
curl http://localhost:9080/vernier/command/p    # Cambiar a fotopuerta  
curl http://localhost:9080/vernier/command/m    # Cambiar a movimiento
curl http://localhost:9080/vernier/command/d    # Pausar lecturas
curl http://localhost:9080/vernier/command/c    # Continuar lecturas

# Status y información
curl http://localhost:9080/vernier/status
curl http://localhost:9080/vernier/active
```

### 🌐 **Paso 3: Configurar Wokwi IoT Gateway**

Para acceder al servidor HTTP desde tu navegador:

#### **3.1. Instalar Gateway**
```bash
# Descargar desde: https://github.com/wokwi/wokwi-cli/releases
# Windows: wokwi-gateway-windows.exe
# Linux: wokwi-gateway-linux
# macOS: wokwi-gateway-macos

# Ejecutar gateway
./wokwi-gateway-linux --forward 9080:10.13.37.2:8080
```

#### **3.2. Test Conectividad**
```bash
# Una vez iniciada la simulación y gateway:
curl http://localhost:9080/ping
# Debería responder: {"pong": timestamp, "message": "Wokwi simulation is running"}
```

### 🖥️ **Paso 4: Conectar Cliente Python**

#### **4.1. Configurar IP en cliente**
Editar `pc_controller/config.py`:
```python
# Usar localhost con Wokwi Gateway
ESP32_IP = "localhost" 
ESP32_PORT = 9080  # Puerto del gateway, no 8080
```

#### **4.2. Ejecutar cliente**
```bash
cd pc_controller
python main.py
```

**¡El dashboard debe conectar automáticamente y mostrar datos en tiempo real!**

---

## 🛠️ Simuladores Alternativos

### 🥈 **Opción 2: Emulador Python Local**

Para casos donde no se puede usar Wokwi o se necesita más control:

#### **Crear mock_esp32_server.py:**
```python
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
        self.active_sensor = 1  # Temperatura por defecto
        self.reading_active = True
        self.reading_number = 0
        self.start_time = time.time()
        
        print("🔬 Mock ESP32 Vernier System inicializado")
    
    def generate_realistic_data(self):
        """Generar datos realistas con variaciones temporales"""
        current_time = time.time()
        time_diff = current_time - self.start_time
        
        # Temperatura: variación diaria simulada
        temp_base = 22 + 5 * math.sin(time_diff / 3600)  # Ciclo de 1 hora
        temp_noise = random.gauss(0, 0.5)
        temperatura = temp_base + temp_noise
        
        # Fuerza: variación con picos ocasionales
        force_base = 10 + 20 * math.sin(time_diff / 60)  # Ciclo de 1 minuto
        force_spike = 30 if random.random() < 0.05 else 0  # 5% chance de pico
        fuerza = force_base + force_spike + random.gauss(0, 2)
        
        # Fotopuerta: eventos aleatorios
        photogate_blocked = random.random() < 0.1  # 10% probabilidad bloqueado
        
        # Movimiento: distancia con movimiento realista
        distance_base = 15 + 10 * math.sin(time_diff / 30)  # Ciclo de 30 segundos
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
        
        # Incrementar contador
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
        """Suprimir logs de requests (opcional)"""
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
            
            elif self.path == '/vernier/active':
                readings = self.server.esp32_system.generate_realistic_data()
                sensor_keys = ['vernier_temperatura', 'vernier_fuerza', 'vernier_fotopuerta', 'vernier_movimiento']
                active_key = sensor_keys[self.server.esp32_system.active_sensor - 1]
                active_reading = readings[active_key]
                active_reading['is_active_sensor'] = True
                self.send_json_response(active_reading)
            
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
    print(f"   http://{host}:{port}/vernier/status")
    print(f"🔄 Generando datos realistas automáticamente...")
    print(f"🛑 Presionar Ctrl+C para detener")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    start_mock_server()
```

#### **Uso del emulador:**
```bash
# Terminal 1: Iniciar emulador
python mock_esp32_server.py

# Terminal 2: Ejecutar cliente Wally
cd pc_controller
python main.py
```

### 🥉 **Opción 3: Docker Environment**

Para entornos aislados y reproducibles:

#### **Dockerfile:**
```dockerfile
FROM python:3.9-slim

# Instalar dependencias
RUN pip install flask requests matplotlib pandas numpy

# Crear directorio de trabajo
WORKDIR /wally_simulation

# Copiar archivos
COPY mock_esp32_server.py .
COPY requirements.txt .

# Exponer puertos
EXPOSE 8080

# Comando por defecto
CMD ["python", "mock_esp32_server.py"]
```

#### **docker-compose.yml:**
```yaml
version: '3.8'

services:
  esp32-mock:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MOCK_MODE=development
    volumes:
      - ./data:/app/data
    
  wally-client:
    build: 
      context: ./pc_controller
    depends_on:
      - esp32-mock
    environment:
      - ESP32_IP=esp32-mock
    volumes:
      - ./data:/app/data
```

#### **Uso Docker:**
```bash
# Construir y ejecutar
docker-compose up --build

# Solo emulador ESP32
docker run -p 8080:8080 wally-esp32-mock
```

---

## 🧪 Testing y Validación

### 🔍 **Test Suite Automatizado**

#### **test_simulation.py:**
```python
"""
Suite de testing para validar simulación Wally DAQ
"""
import requests
import time
import json
import pytest

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
        commands = ['t', f', 'p', 'm', 'd', 'c']
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
    
    def test_sensor_data_validity(self):
        """Test validez de datos de sensores"""
        try:
            response = requests.get(f"{self.base_url}/sensors")
            data = response.json()
            readings = data['readings']
            
            # Test temperatura (15-40°C)
            temp = readings['vernier_temperatura']['value']
            assert 10 <= temp <= 45, f"Temperatura fuera de rango: {temp}°C"
            
            # Test fuerza (-50N a +100N)
            force = readings['vernier_fuerza']['value']
            assert -60 <= force <= 120, f"Fuerza fuera de rango: {force}N"
            
            # Test fotopuerta (0 o 1)
            photogate = readings['vernier_fotopuerta']['value']
            assert photogate in [0, 1], f"Fotopuerta valor inválido: {photogate}"
            
            # Test movimiento (5-50cm)
            distance = readings['vernier_movimiento']['value']
            assert 3 <= distance <= 60, f"Distancia fuera de rango: {distance}cm"
            
            print("✅ Validación datos sensores OK")
            return True
        except Exception as e:
            print(f"❌ Validación datos falló: {e}")
            return False
    
    def test_compatibility_arduino(self):
        """Test compatibilidad con Arduino original"""
        try:
            # Test cambio de sensores
            requests.get(f"{self.base_url}/vernier/command/t")
            time.sleep(0.5)
            response = requests.get(f"{self.base_url}/vernier/status")
            status = response.json()
            
            # Verificar sensor activo
            if 'active_sensor' in status:
                assert status['active_sensor'] == 1  # Temperatura
            
            # Test pause/resume
            requests.get(f"{self.base_url}/vernier/command/d")  # Pausar
            time.sleep(0.5)
            status_paused = requests.get(f"{self.base_url}/vernier/status").json()
            
            requests.get(f"{self.base_url}/vernier/command/c")  # Continuar
            time.sleep(0.5)
            status_resumed = requests.get(f"{self.base_url}/vernier/status").json()
            
            print("✅ Compatibilidad Arduino OK")
            return True
        except Exception as e:
            print(f"❌ Test compatibilidad falló: {e}")
            return False
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        tests = [
            ("Conectividad", self.test_connectivity),
            ("Endpoint Sensores", self.test_sensors_endpoint),
            ("Comandos Arduino", self.test_arduino_commands),
            ("Validez Datos", self.test_sensor_data_validity),
            ("Compatibilidad Arduino", self.test_compatibility_arduino)
        ]
        
        print("🧪 Iniciando Test Suite Wally Simulation")
        print("=" * 50)
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 Ejecutando: {test_name}")
            result = test_func()
            results.append((test_name, result))
            time.sleep(1)  # Delay entre tests
        
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

# Script ejecutable
if __name__ == "__main__":
    import sys
    
    # Permitir URL personalizada
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    print(f"🎯 Testing simulación en: {url}")
    tester = TestWallySimulation(url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)
```

### ⚡ **Scripts de Testing Rápido**

#### **quick_test.sh (Linux/macOS):**
```bash
#!/bin/bash
echo "🚀 Quick Test Wally Simulation"

# Test conectividad
echo "📡 Testing conectividad..."
curl -s http://localhost:8080/ping | jq . || echo "❌ Ping falló"

# Test sensores
echo "🔬 Testing sensores..."
curl -s http://localhost:8080/sensors | jq '.readings | keys' || echo "❌ Sensores falló"

# Test comandos Arduino
echo "🎛️ Testing comandos Arduino..."
for cmd in t f p m d c; do
    result=$(curl -s http://localhost:8080/vernier/command/$cmd | jq -r '.result')
    echo "  Comando '$cmd': $result"
done

echo "✅ Quick test completado"
```

#### **quick_test.bat (Windows):**
```batch
@echo off
echo 🚀 Quick Test Wally Simulation

echo 📡 Testing conectividad...
curl -s http://localhost:8080/ping
echo.

echo 🔬 Testing sensores...
curl -s http://localhost:8080/sensors
echo.

echo 🎛️ Testing comandos Arduino...
for %%c in (t f p m d c) do (
    echo Testing comando %%c...
    curl -s http://localhost:8080/vernier/command/%%c
    echo.
)

echo ✅ Quick test completado
pause
```

### 📊 **Validación Datos en Tiempo Real**

#### **monitor_simulation.py:**
```python
"""
Monitor de simulación en tiempo real
"""
import requests
import time
import matplotlib.pyplot as plt
from collections import deque
import threading

class SimulationMonitor:
    """Monitor de datos en tiempo real"""
    
    def __init__(self, url="http://localhost:8080", max_points=100):
        self.url = url
        self.max_points = max_points
        self.running = False
        
        # Buffers de datos
        self.timestamps = deque(maxlen=max_points)
        self.temperatura = deque(maxlen=max_points)
        self.fuerza = deque(maxlen=max_points)
        self.distancia = deque(maxlen=max_points)
        
        # Setup matplotlib
        plt.ion()
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8))
        self.fig.suptitle('Wally DAQ System - Monitor Simulación')
    
    def fetch_data(self):
        """Obtener datos del simulador"""
        try:
            response = requests.get(f"{self.url}/sensors", timeout=2)
            if response.status_code == 200:
                data = response.json()
                readings = data['readings']
                
                timestamp = time.time()
                temp = readings['vernier_temperatura']['value']
                force = readings['vernier_fuerza']['value']  
                distance = readings['vernier_movimiento']['value']
                
                return timestamp, temp, force, distance
        except Exception as e:
            print(f"Error obteniendo datos: {e}")
        
        return None
    
    def update_plots(self):
        """Actualizar gráficos"""
        if len(self.timestamps) < 2:
            return
        
        # Convertir a listas para plotting
        times = list(self.timestamps)
        temps = list(self.temperatura)
        forces = list(self.fuerza)
        distances = list(self.distancia)
        
        # Limpiar axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Plot temperatura
        self.ax1.plot(times, temps, 'r-', label='Temperatura')
        self.ax1.set_ylabel('Temperatura (°C)')
        self.ax1.legend()
        self.ax1.grid(True)
        
        # Plot fuerza
        self.ax2.plot(times, forces, 'b-', label='Fuerza')
        self.ax2.set_ylabel('Fuerza (N)')
        self.ax2.legend()
        self.ax2.grid(True)
        
        # Plot distancia
        self.ax3.plot(times, distances, 'g-', label='Distancia')
        self.ax3.set_ylabel('Distancia (cm)')
        self.ax3.set_xlabel('Tiempo')
        self.ax3.legend()
        self.ax3.grid(True)
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
    
    def monitor_loop(self):
        """Loop principal de monitoreo"""
        print("🔍 Iniciando monitor de simulación...")
        print("🛑 Cerrar ventana gráfica para detener")
        
        while self.running:
            data = self.fetch_data()
            if data:
                timestamp, temp, force, distance = data
                
                # Agregar a buffers
                self.timestamps.append(timestamp)
                self.temperatura.append(temp)
                self.fuerza.append(force)
                self.distancia.append(distance)
                
                # Actualizar gráficos
                self.update_plots()
                
                # Info en consola
                print(f"📊 T:{temp:.1f}°C F:{force:.1f}N D:{distance:.1f}cm")
            
            time.sleep(1)
    
    def start(self):
        """Iniciar monitor"""
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Mantener ventana abierta
            plt.show(block=True)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            print("🛑 Monitor detenido")

if __name__ == "__main__":
    monitor = SimulationMonitor()
    monitor.start()
```

---

## 🔧 Troubleshooting

### ❌ **Problemas Comunes Wokwi**

#### **Error: "WiFi no conecta"**
```
Solución:
- Usar WIFI_SSID = "Wokwi-GUEST" exactamente
- WIFI_PASSWORD = "" (string vacío)
- No cambiar configuración WiFi en Wokwi
```

#### **Error: "No se puede acceder HTTP"**
```
Solución:
- Instalar Wokwi IoT Gateway
- Ejecutar: ./wokwi-gateway --forward 9080:10.13.37.2:8080
- Usar localhost:9080 no localhost:8080
```

#### **Error: "Componentes no responden"**
```
Solución:
- Verificar connections en diagram.json
- Asegurar que pines GPIO coincidan
- Recargar simulación (F5)
```

#### **Error: "Cliente Python no conecta"**
```
Solución:
- ESP32_IP = "localhost" 
- ESP32_PORT = 9080 (no 8080)
- Gateway debe estar ejecutándose
```

### ❌ **Problemas Mock Server**

#### **Error: "Puerto ocupado"**
```bash
# Verificar qué usa puerto 8080
lsof -i :8080  # Linux/macOS
netstat -ano | findstr 8080  # Windows

# Usar puerto diferente
python mock_esp32_server.py --port 8081
```

#### **Error: "Datos no realistas"**
```python
# Ajustar rangos en mock_esp32_server.py
def generate_realistic_data(self):
    # Modificar rangos según necesidades
    temperatura = 20 + random.uniform(-5, 15)  # 15-35°C
    fuerza = random.uniform(-10, 50)           # -10N a 50N
```

### ❌ **Problemas Cliente Python**

#### **Error: "ModuleNotFoundError"**
```bash
# Verificar entorno virtual
source wally_env/bin/activate  # Linux/macOS
wally_env\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

#### **Error: "Connection refused"**
```bash
# Verificar simulador ejecutándose
curl http://localhost:8080/ping

# Test manual endpoints
curl http://localhost:8080/sensors
curl http://localhost:8080/vernier/status
```

### 🛠️ **Scripts de Diagnóstico**

#### **diagnose_system.py:**
```python
"""
Script de diagnóstico automático
"""
import requests
import subprocess
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
    
    # Check endpoints si disponibles
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
```

---

## 📚 Recursos Adicionales

### 📖 **Documentación Oficial**

- **Wokwi Docs**: https://docs.wokwi.com/guides/esp32
- **ESP32 MicroPython**: https://docs.micropython.org/en/latest/esp32/
- **Wokwi ESP32 WiFi**: https://docs.wokwi.com/guides/esp32-wifi

### 🎓 **Tutoriales y Ejemplos**

- **Wokwi ESP32 Examples**: https://wokwi.com/projects?tag=esp32
- **MicroPython Tutorials**: https://wokwi.com/micropython
- **HTTP Server Examples**: https://wokwi.com/projects?q=esp32+http

### 🛠️ **Herramientas Complementarias**

#### **Postman Collection para Testing:**
```json
{
  "info": {"name": "Wally DAQ System API"},
  "item": [
    {
      "name": "Ping",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/ping"
      }
    },
    {
      "name": "All Sensors",
      "request": {
        "method": "GET", 
        "url": "{{base_url}}/sensors"
      }
    },
    {
      "name": "Change to Temperature",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/vernier/command/t"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8080"
    }
  ]
}
```

### 🧪 **Casos de Prueba Específicos**

#### **Test migración Arduino:**
```python
# test_arduino_compatibility.py
def test_arduino_migration():
    """Verificar que migración Arduino funciona"""
    
    # Test comandos idénticos
    arduino_commands = ['t', 'f', 'p', 'm', 'd', 'c']
    for cmd in arduino_commands:
        response = requests.get(f"http://localhost:8080/vernier/command/{cmd}")
        assert response.status_code == 200
        
    # Test estructura datos compatible
    response = requests.get("http://localhost:8080/sensors")
    data = response.json()
    
    # Verificar campos esperados por cliente original
    assert 'arduino_compatible' in data
    assert data['arduino_compatible'] == True
    assert 'readings' in data
    assert 'vernier_active_sensor' in data
```

### 🎯 **Plantillas de Proyectos**

#### **Proyecto Educativo:**
```
Objetivos:
1. Entender migración Arduino → ESP32
2. Aprender MicroPython vs C++
3. Implementar conectividad WiFi/HTTP
4. Crear interfaz gráfica con Python

Entregables:
- Sistema funcionando en simulación
- Documentación comparativa Arduino vs ESP32  
- Presentación demo en vivo
- Propuesta extensiones futuras
```

#### **Proyecto Industrial:**
```
Objetivos:
1. Validar arquitectura IoT completa
2. Testing de robustez y escalabilidad
3. Implementación CI/CD con simulación
4. Documentación para manufactura

Entregables:
- Suite de testing automatizado
- Docker containers para desarrollo
- Análisis de performance
- Plan migración hardware real
```

---

## 🎯 **Resumen Ejecutivo**

### ✅ **Lo que puedes hacer con esta guía:**

1. **🎮 Simular completamente** el sistema Wally DAQ sin hardware
2. **🔧 Probar migración Arduino → ESP32** paso a paso
3. **📊 Validar funcionalidad** antes de implementación física
4. **🎓 Aprender IoT moderno** con herramientas profesionales
5. **⚡ Desarrollar rápidamente** sin limitaciones de hardware

### 🏆 **Beneficios Clave:**

- **⏰ Ahorro tiempo**: No esperar hardware, desarrollo inmediato
- **💰 Ahorro costos**: No comprar equipos para prototipar
- **🔒 Seguridad**: No riesgo dañar componentes reales
- **📈 Escalabilidad**: Fácil replicar para múltiples desarrolladores
- **🧪 Testing**: Validación completa antes de producción

### 🚀 **Next Steps Recomendados:**

1. **Comenzar con Wokwi** (5 minutos de setup)
2. **Probar todos los endpoints** HTTP  
3. **Conectar cliente Python** original
4. **Validar compatibilidad** Arduino completa
5. **Implementar en hardware real** cuando esté listo

**¡Con esta guía tienes todo lo necesario para simular y desarrollar el sistema Wally DAQ completo!**

---

*Guía desarrollada por [Ingeniero Gino Viloria](mailto:codevilor.ia@gmail.com) - Especialista en Sistemas DAQ y Simulación IoT*