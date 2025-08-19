# esp32/vernier_sensors_migrated.py
"""
Migración del código Arduino Vernier a ESP32 MicroPython
Mantiene la misma funcionalidad y comandos serie
"""
import machine
import time
import ujson

# Definición de sensores (mantener compatibilidad)
SENSOR_TEMPERATURA = 1
SENSOR_FUERZA = 2
SENSOR_FOTOPUERTA = 3
SENSOR_MOVIMIENTO = 4

class VernierSensorManager:
    def __init__(self):
        # Mapeo de pines Arduino → ESP32
        self.pin_config = {
            'temperatura_adc': machine.ADC(machine.Pin(34)),  # A0 → GPIO34
            'fuerza_adc': machine.ADC(machine.Pin(35)),       # A1 → GPIO35
            'led_status': machine.Pin(2, machine.Pin.OUT),    # D13 → GPIO2 (LED)
            'photogate_input': machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP),  # D2 → GPIO4
            'trigger_pin': machine.Pin(5, machine.Pin.OUT),   # D3 → GPIO5
            'echo_pin': machine.Pin(18, machine.Pin.IN)       # D2 → GPIO18 (diferente)
        }
        
        # Configurar ADCs
        for adc_name in ['temperatura_adc', 'fuerza_adc']:
            self.pin_config[adc_name].atten(machine.ADC.ATTN_11DB)  # 0-3.3V
        
        # Variables de estado (migradas del Arduino)
        self.sensor_seleccionado = 0
        self.lectura_activa = True
        self.reading_number = 0
        self.threshold = 100.0
        self.time_between_readings = 500
        
        # Variables para fotopuerta
        self.status = 1  # HIGH
        self.time_ms = 0
        self.time_us = 0
        
        print("✅ VernierSensorManager inicializado")
        print("📡 Pines configurados para ESP32")
        
    def auto_id_sensor(self, sensor_type):
        """Simulación de VernierLib.autoID() para diferentes sensores"""
        sensor_info = {
            SENSOR_TEMPERATURA: {
                'name': 'Stainless Steel Temperature Probe',
                'short_name': 'Temp',
                'units': '°C',
                'slope': 100.0,
                'intercept': -50.0
            },
            SENSOR_FUERZA: {
                'name': 'Dual-Range Force Sensor',
                'short_name': 'Force',
                'units': 'N',
                'slope': 50.0,
                'intercept': -25.0
            },
            SENSOR_FOTOPUERTA: {
                'name': 'Photogate Head',
                'short_name': 'Gate',
                'units': 'blocked',
                'slope': 1.0,
                'intercept': 0.0
            },
            SENSOR_MOVIMIENTO: {
                'name': 'Motion Detector',
                'short_name': 'Motion',
                'units': 'cm',
                'slope': 1.0,
                'intercept': 0.0
            }
        }
        return sensor_info.get(sensor_type, sensor_info[SENSOR_TEMPERATURA])
    
    def configurar_temperatura(self):
        """Migración de configurarTemperatura()"""
        print("Vernier Format 2")
        print("Stainless Steel Temperature Probe")
        print("Readings taken using ESP32")
        print("Data Set")
        print("Time\tTemperature")
        print("s\t°C")
        print("seconds\tdegrees Celsius")
        print("✅ Sensor de temperatura configurado")
    
    def configurar_fuerza(self):
        """Migración de configurarFuerza()"""
        self.threshold = 100
        self.time_between_readings = 500
        
        sensor_info = self.auto_id_sensor(SENSOR_FUERZA)
        print("Vernier Format 2")
        print(sensor_info['name'])
        print("Readings taken using ESP32")
        print("Data Set")
        print(f"Time\t{sensor_info['name']}")
        print(f"t\t{sensor_info['short_name']}")
        print(f"seconds\t{sensor_info['units']}")
        print("✅ Sensor de fuerza configurado")
    
    def configurar_fotopuerta(self):
        """Migración de configurarFotopuerta()"""
        self.time_ms = 0
        self.time_us = 0
        self.status = 1
        
        print("Vernier Format 2")
        print("Photogate blocked times taken using ESP32")
        print("Time\tTime")
        print("ms\tmicroseconds")
        print("✅ Sensor de fotopuerta configurado")
    
    def configurar_movimiento(self):
        """Migración de configurarMovimiento()"""
        print("Vernier Format 2")
        print("Motion Detector Readings taken using ESP32")
        print("Data Set")
        print("Time for Echo\tDistance")
        print("delta t\tD")
        print("seconds\tcentimeters")
        print("✅ Sensor de movimiento configurado")
    
    def leer_temperatura(self):
        """Migración de leerTemperatura()"""
        # Leer ADC y convertir a temperatura
        raw_value = self.pin_config['temperatura_adc'].read()
        voltage = raw_value * 3.3 / 4095
        
        # Calibración típica sensor temperatura Vernier
        temperatura = (voltage - 0.5) * 100  # TMP36 formula
        
        timestamp = time.time()
        print(f"{timestamp:.3f}\t{temperatura:.2f}")
        
        return {
            'sensor': 'temperatura',
            'value': temperatura,
            'unit': '°C',
            'timestamp': timestamp,
            'raw': raw_value,
            'voltage': voltage
        }
    
    def leer_fuerza(self):
        """Migración de leerFuerza()"""
        # Leer ADC del sensor de fuerza
        raw_value = self.pin_config['fuerza_adc'].read()
        voltage = raw_value * 3.3 / 4095
        
        # Calibración sensor fuerza Vernier (aproximada)
        fuerza = (voltage - 2.5) * 50  # Ajustar según calibración real
        
        # Mostrar datos en formato Arduino
        timestamp = self.reading_number / 1000.0 * self.time_between_readings
        print(f"{timestamp:.3f}\t{fuerza:.2f}")
        
        # Control LED según threshold (migrado de Arduino)
        if fuerza > self.threshold:
            self.pin_config['led_status'].on()
        else:
            self.pin_config['led_status'].off()
        
        self.reading_number += 1
        
        return {
            'sensor': 'fuerza',
            'value': fuerza,
            'unit': 'N',
            'timestamp': timestamp,
            'raw': raw_value,
            'voltage': voltage
        }
    
    def leer_fotopuerta(self):
        """Migración de leerFotopuerta()"""
        # Leer estado fotopuerta (LOW cuando bloqueada)
        photogate = self.pin_config['photogate_input'].value()
        
        if photogate == 0:  # LOW = bloqueada
            self.pin_config['led_status'].on()
            
            if self.status == 1:  # Cambio de estado
                self.time_ms = time.ticks_ms()
                self.time_us = time.ticks_us()
                print(f"{self.time_ms}\t{self.time_us}")
        else:
            self.pin_config['led_status'].off()
        
        self.status = photogate
        
        return {
            'sensor': 'fotopuerta',
            'value': photogate,
            'unit': 'blocked' if photogate == 0 else 'open',
            'timestamp': time.time(),
            'time_ms': self.time_ms,
            'time_us': self.time_us
        }
    
    def leer_movimiento(self):
        """Migración de leerMovimiento()"""
        # Implementación sensor ultrasónico HC-SR04
        trigger = self.pin_config['trigger_pin']
        echo = self.pin_config['echo_pin']
        
        # Enviar pulso trigger
        trigger.off()
        time.sleep_us(4000)
        trigger.on()
        start_time = time.ticks_us()
        time.sleep_us(900)
        
        # Esperar echo
        while echo.value() == 0:
            pass
        
        duration = time.ticks_diff(time.ticks_us(), start_time)
        
        # Calcular distancia (misma fórmula del Arduino)
        speed_of_sound = 340  # m/s
        distance = duration * speed_of_sound / 2 / 10000  # convertir a cm
        
        print(f"{duration}\t{distance:.2f}")
        
        return {
            'sensor': 'movimiento',
            'value': distance,
            'unit': 'cm',
            'timestamp': time.time(),
            'duration': duration
        }
    
    def leer_sensor(self, sensor_type):
        """Migración de leerSensor() - dispatcher principal"""
        if sensor_type == SENSOR_TEMPERATURA:
            return self.leer_temperatura()
        elif sensor_type == SENSOR_FUERZA:
            return self.leer_fuerza()
        elif sensor_type == SENSOR_FOTOPUERTA:
            return self.leer_fotopuerta()
        elif sensor_type == SENSOR_MOVIMIENTO:
            return self.leer_movimiento()
        else:
            print(f"❌ Sensor tipo {sensor_type} no soportado")
            return None
    
    def configurar_sensor(self, sensor_type):
        """Configurar sensor según tipo"""
        if sensor_type == SENSOR_TEMPERATURA:
            self.configurar_temperatura()
        elif sensor_type == SENSOR_FUERZA:
            self.configurar_fuerza()
        elif sensor_type == SENSOR_FOTOPUERTA:
            self.configurar_fotopuerta()
        elif sensor_type == SENSOR_MOVIMIENTO:
            self.configurar_movimiento()
        
        self.sensor_seleccionado = sensor_type

# Función principal (migración del setup() y loop())
def main():
    """Migración de setup() y loop() de Arduino"""
    sensor_manager = VernierSensorManager()
    
    print("Sistema de Sensores Vernier - ESP32")
    print("Comandos disponibles:")
    print("t: Temperatura")
    print("f: Fuerza") 
    print("p: Fotopuerta")
    print("m: Movimiento")
    print("d: Detener lecturas")
    print("c: Continuar lecturas")
    
    # Configuración inicial (esperar selección como en Arduino)
    while True:
        # Simular Serial.available() con input no bloqueante
        try:
            # En ESP32, esto sería manejo de UART o HTTP requests
            import select
            import sys
            
            # Para demo, usar primer sensor disponible
            sensor_manager.configurar_sensor(SENSOR_TEMPERATURA)
            break
        except:
            time.sleep(0.1)
    
    # Loop principal
    while True:
        try:
            # Simular comandos serie (en ESP32 real sería HTTP o UART)
            # Por ahora, leer sensor activo continuamente
            
            if sensor_manager.lectura_activa:
                data = sensor_manager.leer_sensor(sensor_manager.sensor_seleccionado)
                if data:
                    # También enviar como JSON para integración con sistema Wally
                    json_data = ujson.dumps(data)
                    # print(f"JSON: {json_data}")  # Comentado para no saturar
                
                time.sleep(1)  # Delay 1 segundo como en Arduino
            else:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()