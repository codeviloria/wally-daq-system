"""
Servidor de sensores para ESP32
Maneja lecturas de sensores Vernier y servidor HTTP
"""
import machine
import socket
import ujson
import time
import gc

class SensorServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.sensors = {}
        self.running = False
        
        # Importar configuración
        from config import SENSOR_PINS, SENSOR_CALIBRATION
        self.sensor_pins = SENSOR_PINS
        self.calibration = SENSOR_CALIBRATION
        
        # Inicializar sensores
        self.init_sensors()
        
    def init_sensors(self):
        """Inicializar ADCs para todos los sensores"""
        print("🔧 Inicializando sensores...")
        
        for sensor_name, pin in self.sensor_pins.items():
            try:
                adc = machine.ADC(machine.Pin(pin))
                adc.atten(machine.ADC.ATTN_11DB)  # 0-3.3V range
                self.sensors[sensor_name] = {
                    'adc': adc,
                    'pin': pin,
                    'last_reading': None,
                    'status': 'initialized'
                }
                print(f"  ✅ {sensor_name} en pin {pin}")
            except Exception as e:
                print(f"  ❌ Error {sensor_name}: {e}")
                
    def read_sensor(self, sensor_name):
        """Leer un sensor específico con calibración"""
        if sensor_name not in self.sensors:
            return None
            
        sensor = self.sensors[sensor_name]
        calibration = self.calibration.get(sensor_name, {})
        
        try:
            # Leer ADC múltiples veces para estabilidad
            readings = []
            for _ in range(3):
                raw = sensor['adc'].read()
                readings.append(raw)
                time.sleep(0.01)
            
            # Promedio para reducir ruido
            raw_avg = sum(readings) / len(readings)
            voltage = raw_avg * 3.3 / 4095
            
            # Aplicar calibración
            slope = calibration.get('slope', 1.0)
            offset = calibration.get('offset', 0.0)
            unit = calibration.get('unit', 'V')
            
            # Cálculo calibrado específico por sensor
            if sensor_name == 'temperature':
                # TMP36: (voltage - 0.5) * 100
                value = (voltage - 0.5) * 100
            elif sensor_name == 'ph':
                # pH sensor: mapeo lineal alrededor de 7
                value = 7 - (voltage - 2.5) * 3
            elif sensor_name == 'motion':
                # Acelerómetro: (V - Vref) / sensitivity
                value = (voltage - 1.65) / 0.33
            elif sensor_name == 'pressure':
                # Sensor presión: mapeo lineal
                value = voltage * 50
            else:
                # Genérico
                value = voltage * slope + offset
            
            # Actualizar estado del sensor
            sensor['last_reading'] = value
            sensor['status'] = 'active'
            
            return {
                'sensor_type': sensor_name,
                'value': round(value, 2),
                'unit': unit,
                'voltage': round(voltage, 3),
                'raw': int(raw_avg),
                'status': 'active',
                'timestamp': time.time()
            }
            
        except Exception as e:
            sensor['status'] = 'error'
            return {
                'sensor_type': sensor_name,
                'value': None,
                'unit': None,
                'voltage': None,
                'raw': None,
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def read_all_sensors(self):
        """Leer todos los sensores configurados"""
        readings = {}
        
        for sensor_name in self.sensors.keys():
            reading = self.read_sensor(sensor_name)
            if reading:
                readings[sensor_name] = reading
        
        return {
            'device_id': 'esp32_wally',
            'timestamp': time.time(),
            'readings': readings,
            'sensor_count': len([r for r in readings.values() if r['status'] == 'active']),
            'memory_free': gc.mem_free()
        }
    
    def handle_http_request(self, request):
        """Procesar petición HTTP y generar respuesta"""
        try:
            # Parsear línea de petición
            lines = request.split('\n')
            if not lines:
                return self.http_error(400, "Bad Request")
            
            request_line = lines[0].strip()
            parts = request_line.split()
            
            if len(parts) < 2:
                return self.http_error(400, "Bad Request")
            
            method = parts[0]
            path = parts[1]
            
            # Rutear peticiones
            if method == "GET":
                if path == "/" or path == "/sensors":
                    return self.http_sensor_data()
                elif path == "/status":
                    return self.http_status()
                elif path == "/ping":
                    return self.http_ping()
                else:
                    return self.http_error(404, "Not Found")
            else:
                return self.http_error(405, "Method Not Allowed")
                
        except Exception as e:
            return self.http_error(500, f"Internal Server Error: {e}")
    
    def http_sensor_data(self):
        """Endpoint principal - datos de sensores"""
        data = self.read_all_sensors()
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
    
    def http_status(self):
        """Endpoint de status del sistema"""
        status = {
            'device_id': 'esp32_wally',
            'status': 'running',
            'uptime': time.time(),
            'sensors_configured': len(self.sensors),
            'memory_free': gc.mem_free(),
            'ip_address': self.ip
        }
        
        json_data = ujson.dumps(status)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(json_data)}\r\n"
            "\r\n"
            f"{json_data}"
        )
        return response
    
    def http_ping(self):
        """Endpoint simple para verificar conectividad"""
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 4\r\n"
            "\r\n"
            "pong"
        )
        return response
    
    def http_error(self, code, message):
        """Generar respuesta de error HTTP"""
        response = (
            f"HTTP/1.1 {code} {message}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(message)}\r\n"
            "\r\n"
            f"{message}"
        )
        return response
    
    def start(self):
        """Iniciar servidor HTTP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"🌐 Servidor HTTP iniciado en {self.ip}:{self.port}")
            print(f"📡 Endpoints disponibles:")
            print(f"   GET http://{self.ip}:{self.port}/sensors - Datos de sensores")
            print(f"   GET http://{self.ip}:{self.port}/status  - Status del sistema")
            print(f"   GET http://{self.ip}:{self.port}/ping    - Test conectividad")
            
            # Bucle principal del servidor
            while self.running:
                try:
                    # Aceptar conexión con timeout
                    self.socket.settimeout(1.0)
                    conn, addr = self.socket.accept()
                    
                    # Leer petición
                    conn.settimeout(2.0)
                    request = conn.recv(1024).decode('utf-8')
                    
                    # Procesar y responder
                    response = self.handle_http_request(request)
                    conn.send(response.encode('utf-8'))
                    
                    # Cerrar conexión
                    conn.close()
                    
                    # Garbage collection periódico
                    if time.time() % 30 < 1:
                        gc.collect()
                        
                except OSError:
                    # Timeout - continuar
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
            print("🛑 Servidor detenido")