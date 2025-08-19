"""
Servidor de sensores para ESP32 - ACTUALIZADO con Sensores Vernier
Integra funcionalidad Arduino original + Sistema Wally HTTP
"""
import machine
import socket
import ujson
import time
import gc

# Constantes de sensores Vernier (migradas de Arduino)
SENSOR_TEMPERATURA = 1
SENSOR_FUERZA = 2
SENSOR_FOTOPUERTA = 3
SENSOR_MOVIMIENTO = 4

class VernierSensorManager:
    """Manager de sensores Vernier migrado desde Arduino"""
    
    def __init__(self):
        # Mapeo de pines Arduino → ESP32
        self.pin_config = {
            'temperatura_adc': machine.ADC(machine.Pin(34)),  # A0 → GPIO34
            'fuerza_adc': machine.ADC(machine.Pin(35)),       # A1 → GPIO35
            'led_status': machine.Pin(2, machine.Pin.OUT),    # D13 → GPIO2
            'photogate_input': machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP),  # D2 → GPIO4
            'trigger_pin': machine.Pin(5, machine.Pin.OUT),   # D3 → GPIO5
            'echo_pin': machine.Pin(18, machine.Pin.IN)       # Nuevo pin para echo
        }
        
        # Configurar ADCs
        for adc_name in ['temperatura_adc', 'fuerza_adc']:
            self.pin_config[adc_name].atten(machine.ADC.ATTN_11DB)
        
        # Variables de estado (migradas del Arduino)
        self.sensor_seleccionado = SENSOR_TEMPERATURA
        self.lectura_activa = True
        self.reading_number = 0
        self.threshold = 100.0
        self.time_between_readings = 500
        
        # Variables fotopuerta
        self.status = 1
        self.time_ms = 0
        self.time_us = 0
        
        print("🔬 VernierSensorManager inicializado (migrado desde Arduino)")
        
    def read_sensor_vernier(self, sensor_type):
        """Leer sensor específico Vernier con lógica original Arduino"""
        
        if sensor_type == SENSOR_TEMPERATURA:
            return self._read_temperatura()
        elif sensor_type == SENSOR_FUERZA:
            return self._read_fuerza()
        elif sensor_type == SENSOR_FOTOPUERTA:
            return self._read_fotopuerta()
        elif sensor_type == SENSOR_MOVIMIENTO:
            return self._read_movimiento()
        else:
            return None
    
    def _read_temperatura(self):
        """Lectura temperatura (migrado de Arduino)"""
        try:
            raw_value = self.pin_config['temperatura_adc'].read()
            voltage = raw_value * 3.3 / 4095
            
            # Calibración TMP36 (igual que Arduino)
            temperatura = (voltage - 0.5) * 100
            
            return {
                'sensor_type': 'temperatura',
                'value': round(temperatura, 2),
                'unit': '°C',
                'voltage': round(voltage, 3),
                'raw': raw_value,
                'status': 'active',
                'timestamp': time.time(),
                'vernier_id': SENSOR_TEMPERATURA
            }
        except Exception as e:
            return {
                'sensor_type': 'temperatura',
                'value': None,
                'unit': '°C',
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _read_fuerza(self):
        """Lectura fuerza (migrado de Arduino)"""
        try:
            raw_value = self.pin_config['fuerza_adc'].read()
            voltage = raw_value * 3.3 / 4095
            
            # Calibración sensor fuerza Vernier
            fuerza = (voltage - 2.5) * 50  # Ajustar según calibración real
            
            # Control LED según threshold (lógica Arduino)
            if fuerza > self.threshold:
                self.pin_config['led_status'].on()
            else:
                self.pin_config['led_status'].off()
            
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
                'led_status': fuerza > self.threshold,
                'vernier_id': SENSOR_FUERZA
            }
        except Exception as e:
            return {
                'sensor_type': 'fuerza',
                'value': None,
                'unit': 'N',
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _read_fotopuerta(self):
        """Lectura fotopuerta (migrado de Arduino)"""
        try:
            # Leer estado fotopuerta (LOW cuando bloqueada)
            photogate = self.pin_config['photogate_input'].value()
            
            if photogate == 0:  # LOW = bloqueada
                self.pin_config['led_status'].on()
                
                if self.status == 1:  # Cambio de estado
                    self.time_ms = time.ticks_ms()
                    self.time_us = time.ticks_us()
            else:
                self.pin_config['led_status'].off()
            
            self.status = photogate
            
            return {
                'sensor_type': 'fotopuerta',
                'value': photogate,
                'unit': 'blocked' if photogate == 0 else 'open',
                'status': 'active',
                'timestamp': time.time(),
                'time_ms': self.time_ms,
                'time_us': self.time_us,
                'led_status': photogate == 0,
                'vernier_id': SENSOR_FOTOPUERTA
            }
        except Exception as e:
            return {
                'sensor_type': 'fotopuerta',
                'value': None,
                'unit': None,
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _read_movimiento(self):
        """Lectura movimiento/ultrasonido (migrado de Arduino)"""
        try:
            trigger = self.pin_config['trigger_pin']
            echo = self.pin_config['echo_pin']
            
            # Enviar pulso trigger (lógica Arduino)
            trigger.off()
            time.sleep_us(4000)
            trigger.on()
            start_time = time.ticks_us()
            time.sleep_us(900)
            
            # Esperar echo con timeout
            timeout_count = 0
            while echo.value() == 0:
                timeout_count += 1
                if timeout_count > 30000:  # Timeout protection
                    raise Exception("Echo timeout")
            
            duration = time.ticks_diff(time.ticks_us(), start_time)
            
            # Calcular distancia (fórmula Arduino)
            speed_of_sound = 340  # m/s
            distance = duration * speed_of_sound / 2 / 10000  # cm
            
            return {
                'sensor_type': 'movimiento',
                'value': round(distance, 2),
                'unit': 'cm',
                'status': 'active',
                'timestamp': time.time(),
                'duration_us': duration,
                'vernier_id': SENSOR_MOVIMIENTO
            }
        except Exception as e:
            return {
                'sensor_type': 'movimiento',
                'value': None,
                'unit': 'cm',
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
    
    def handle_arduino_command(self, command):
        """Manejar comandos Arduino originales"""
        if command == 't':
            self.sensor_seleccionado = SENSOR_TEMPERATURA
            return "Sensor cambiado a temperatura"
        elif command == 'f':
            self.sensor_seleccionado = SENSOR_FUERZA
            return "Sensor cambiado a fuerza"
        elif command == 'p':
            self.sensor_seleccionado = SENSOR_FOTOPUERTA
            return "Sensor cambiado a fotopuerta"
        elif command == 'm':
            self.sensor_seleccionado = SENSOR_MOVIMIENTO
            return "Sensor cambiado a movimiento"
        elif command == 'd':
            self.lectura_activa = False
            return "Lecturas detenidas"
        elif command == 'c':
            self.lectura_activa = True
            return "Lecturas continuas"
        else:
            return f"Comando {command} no reconocido"


class SensorServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.sensors = {}  # Sensores genéricos originales
        self.running = False
        
        # NUEVO: Inicializar manager Vernier
        self.vernier_manager = VernierSensorManager()
        
        # Importar configuración original
        from config import SENSOR_PINS, SENSOR_CALIBRATION
        self.sensor_pins = SENSOR_PINS
        self.calibration = SENSOR_CALIBRATION
        
        # Inicializar sensores genéricos (compatibilidad)
        self.init_sensors()
        
    def init_sensors(self):
        """Inicializar sensores genéricos (mantener compatibilidad)"""
        print("🔧 Inicializando sensores genéricos...")
        
        for sensor_name, pin in self.sensor_pins.items():
            try:
                adc = machine.ADC(machine.Pin(pin))
                adc.atten(machine.ADC.ATTN_11DB)
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
        """Leer sensor genérico (función original)"""
        if sensor_name not in self.sensors:
            return None
            
        sensor = self.sensors[sensor_name]
        calibration = self.calibration.get(sensor_name, {})
        
        try:
            readings = []
            for _ in range(3):
                raw = sensor['adc'].read()
                readings.append(raw)
                time.sleep(0.01)
            
            raw_avg = sum(readings) / len(readings)
            voltage = raw_avg * 3.3 / 4095
            
            slope = calibration.get('slope', 1.0)
            offset = calibration.get('offset', 0.0)
            unit = calibration.get('unit', 'V')
            
            if sensor_name == 'temperature':
                value = (voltage - 0.5) * 100
            elif sensor_name == 'ph':
                value = 7 - (voltage - 2.5) * 3
            elif sensor_name == 'motion':
                value = (voltage - 1.65) / 0.33
            elif sensor_name == 'pressure':
                value = voltage * 50
            else:
                value = voltage * slope + offset
            
            sensor['last_reading'] = value
            sensor['status'] = 'active'
            
            return {
                'sensor_type': sensor_name,
                'value': round(value, 2),
                'unit': unit,
                'voltage': round(voltage, 3),
                'raw': int(raw_avg),
                'status': 'active',
                'timestamp': time.time(),
                'source': 'generic'
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
                'timestamp': time.time(),
                'source': 'generic'
            }
    
    def read_all_sensors(self):
        """Leer TODOS los sensores: genéricos + Vernier"""
        readings = {}
        
        # Leer sensores genéricos (compatibilidad)
        for sensor_name in self.sensors.keys():
            reading = self.read_sensor(sensor_name)
            if reading:
                readings[f"generic_{sensor_name}"] = reading
        
        # NUEVO: Leer sensores Vernier específicos
        vernier_sensors = {
            'vernier_temperatura': SENSOR_TEMPERATURA,
            'vernier_fuerza': SENSOR_FUERZA,
            'vernier_fotopuerta': SENSOR_FOTOPUERTA,
            'vernier_movimiento': SENSOR_MOVIMIENTO
        }
        
        for sensor_name, sensor_type in vernier_sensors.items():
            try:
                reading = self.vernier_manager.read_sensor_vernier(sensor_type)
                if reading:
                    reading['source'] = 'vernier'
                    readings[sensor_name] = reading
            except Exception as e:
                readings[sensor_name] = {
                    'sensor_type': sensor_name,
                    'value': None,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': time.time(),
                    'source': 'vernier'
                }
        
        # NUEVO: Agregar sensor activo actual
        if self.vernier_manager.lectura_activa:
            current_reading = self.vernier_manager.read_sensor_vernier(
                self.vernier_manager.sensor_seleccionado
            )
            if current_reading:
                current_reading['source'] = 'vernier_active'
                readings['current_active'] = current_reading
        
        return {
            'device_id': 'esp32_wally_vernier',
            'timestamp': time.time(),
            'readings': readings,
            'sensor_count': len([r for r in readings.values() if r['status'] == 'active']),
            'memory_free': gc.mem_free(),
            'vernier_active_sensor': self.vernier_manager.sensor_seleccionado,
            'vernier_reading_active': self.vernier_manager.lectura_activa,
            'arduino_compatible': True
        }
    
    def handle_http_request(self, request):
        """Procesar petición HTTP con nuevos endpoints Vernier"""
        try:
            lines = request.split('\n')
            if not lines:
                return self.http_error(400, "Bad Request")
            
            request_line = lines[0].strip()
            parts = request_line.split()
            
            if len(parts) < 2:
                return self.http_error(400, "Bad Request")
            
            method = parts[0]
            path = parts[1]
            
            if method == "GET":
                if path == "/" or path == "/sensors":
                    return self.http_sensor_data()
                elif path == "/status":
                    return self.http_status()
                elif path == "/ping":
                    return self.http_ping()
                # NUEVOS ENDPOINTS VERNIER
                elif path.startswith("/vernier/command/"):
                    command = path.split("/")[-1]
                    return self.http_vernier_command(command)
                elif path == "/vernier/status":
                    return self.http_vernier_status()
                elif path == "/vernier/active":
                    return self.http_vernier_active_sensor()
                else:
                    return self.http_error(404, "Not Found")
            else:
                return self.http_error(405, "Method Not Allowed")
                
        except Exception as e:
            return self.http_error(500, f"Internal Server Error: {e}")
    
    def http_sensor_data(self):
        """Endpoint principal con datos Vernier integrados"""
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
    
    def http_vernier_command(self, command):
        """NUEVO: Endpoint para comandos Arduino"""
        try:
            result = self.vernier_manager.handle_arduino_command(command)
            response_data = {
                'command': command,
                'result': result,
                'timestamp': time.time(),
                'active_sensor': self.vernier_manager.sensor_seleccionado,
                'reading_active': self.vernier_manager.lectura_activa
            }
            
            json_data = ujson.dumps(response_data)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                f"Content-Length: {len(json_data)}\r\n"
                "\r\n"
                f"{json_data}"
            )
            return response
        except Exception as e:
            return self.http_error(500, f"Command error: {e}")
    
    def http_vernier_status(self):
        """NUEVO: Status específico Vernier"""
        status = {
            'vernier_manager': {
                'active_sensor': self.vernier_manager.sensor_seleccionado,
                'reading_active': self.vernier_manager.lectura_activa,
                'reading_number': self.vernier_manager.reading_number,
                'threshold': self.vernier_manager.threshold,
                'time_between_readings': self.vernier_manager.time_between_readings
            },
            'sensor_mapping': {
                'temperatura': SENSOR_TEMPERATURA,
                'fuerza': SENSOR_FUERZA,
                'fotopuerta': SENSOR_FOTOPUERTA,
                'movimiento': SENSOR_MOVIMIENTO
            },
            'available_commands': ['t', 'f', 'p', 'm', 'd', 'c'],
            'pin_mapping': {
                'temperatura_adc': 34,
                'fuerza_adc': 35,
                'led_status': 2,
                'photogate_input': 4,
                'trigger_pin': 5,
                'echo_pin': 18
            }
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
    
    def http_vernier_active_sensor(self):
        """NUEVO: Solo el sensor activo actual"""
        if self.vernier_manager.lectura_activa:
            reading = self.vernier_manager.read_sensor_vernier(
                self.vernier_manager.sensor_seleccionado
            )
            if reading:
                reading['is_active_sensor'] = True
            data = reading or {'error': 'No reading available'}
        else:
            data = {'status': 'readings_paused', 'active_sensor': self.vernier_manager.sensor_seleccionado}
        
        json_data = ujson.dumps(data)
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            f"Content-Length: {len(json_data)}\r\n"
            "\r\n"
            f"{json_data}"
        )
        return response
    
    def http_status(self):
        """Status del sistema (actualizado)"""
        status = {
            'device_id': 'esp32_wally_vernier',
            'status': 'running',
            'uptime': time.time(),
            'sensors_configured': len(self.sensors),
            'vernier_sensors': 4,
            'memory_free': gc.mem_free(),
            'ip_address': self.ip,
            'vernier_integration': True,
            'arduino_compatible': True
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
        """Ping (sin cambios)"""
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 4\r\n"
            "\r\n"
            "pong"
        )
        return response
    
    def http_error(self, code, message):
        """Error HTTP (sin cambios)"""
        response = (
            f"HTTP/1.1 {code} {message}\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(message)}\r\n"
            "\r\n"
            f"{message}"
        )
        return response
    
    def start(self):
        """Iniciar servidor HTTP (actualizado)"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"🌐 Servidor Wally+Vernier iniciado en {self.ip}:{self.port}")
            print(f"📡 Endpoints disponibles:")
            print(f"   GET http://{self.ip}:{self.port}/sensors - Todos los sensores")
            print(f"   GET http://{self.ip}:{self.port}/status - Status sistema")
            print(f"   GET http://{self.ip}:{self.port}/ping - Test conectividad")
            print(f"🔬 Endpoints Vernier:")
            print(f"   GET http://{self.ip}:{self.port}/vernier/command/[t|f|p|m|d|c]")
            print(f"   GET http://{self.ip}:{self.port}/vernier/status")
            print(f"   GET http://{self.ip}:{self.port}/vernier/active")
            
            while self.running:
                try:
                    self.socket.settimeout(1.0)
                    conn, addr = self.socket.accept()
                    
                    conn.settimeout(2.0)
                    request = conn.recv(1024).decode('utf-8')
                    
                    response = self.handle_http_request(request)
                    conn.send(response.encode('utf-8'))
                    
                    conn.close()
                    
                    if time.time() % 30 < 1:
                        gc.collect()
                        
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
            print("🛑 Servidor detenido")