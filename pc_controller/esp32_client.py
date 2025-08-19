"""
Cliente HTTP para ESP32 - ACTUALIZADO con soporte Vernier
"""
import requests
import time
import json
import config

class ESP32Client:
    def __init__(self):
        self.base_url = None
        self.is_connected = False
        self.last_successful_request = None
        self.consecutive_errors = 0
        
        print("🌐 ESP32 Client inicializado con soporte Vernier")
    
    def connect(self, ip_address, port=8080):
        """Conectar a ESP32 (sin cambios)"""
        self.base_url = f"http://{ip_address}:{port}"
        
        try:
            print(f"🔗 Conectando a {self.base_url}...")
            
            response = requests.get(
                f"{self.base_url}/ping", 
                timeout=config.CONNECTION_TIMEOUT
            )
            
            if response.status_code == 200:
                self.is_connected = True
                self.consecutive_errors = 0
                self.last_successful_request = time.time()
                
                print(f"✅ Conectado a ESP32")
                
                # NUEVO: Verificar si tiene soporte Vernier
                status_info = self.get_device_status()
                if status_info and status_info.get('arduino_compatible'):
                    print("🔬 Soporte Vernier detectado")
                    vernier_status = self.get_vernier_status()
                    if vernier_status:
                        active_sensor = vernier_status.get('vernier_manager', {}).get('active_sensor', 'unknown')
                        print(f"📊 Sensor Vernier activo: {active_sensor}")
                
                return True
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout: {self.base_url}")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Conexión error: {self.base_url}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.is_connected = False
        return False
    
    def get_sensor_data(self):
        """Obtener datos de sensores (actualizado para Vernier)"""
        if not self.is_connected:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/sensors",
                timeout=config.HTTP_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                self.last_successful_request = time.time()
                self.consecutive_errors = 0
                return data
            else:
                print(f"⚠️ HTTP {response.status_code}")
                self.consecutive_errors += 1
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout datos")
            self.consecutive_errors += 1
        except requests.exceptions.ConnectionError:
            print("🔌 Error conexión datos")
            self.consecutive_errors += 1
            self.is_connected = False
        except json.JSONDecodeError:
            print("📄 Error JSON")
            self.consecutive_errors += 1
        except Exception as e:
            print(f"❌ Error datos: {e}")
            self.consecutive_errors += 1
        
        if self.consecutive_errors >= config.RETRY_ATTEMPTS:
            self.is_connected = False
            print(f"🔴 Muchos errores ({self.consecutive_errors})")
        
        return None
    
    # ========== NUEVOS MÉTODOS VERNIER ==========
    
    def get_vernier_status(self):
        """NUEVO: Obtener status específico Vernier"""
        if not self.is_connected:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/vernier/status",
                timeout=config.HTTP_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Vernier status HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error vernier status: {e}")
        
        return None
    
    def get_vernier_active_sensor(self):
        """NUEVO: Obtener solo sensor Vernier activo"""
        if not self.is_connected:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/vernier/active",
                timeout=config.HTTP_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Vernier active HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error vernier active: {e}")
        
        return None
    
    def send_vernier_command(self, command):
        """NUEVO: Enviar comando Arduino a ESP32"""
        if not self.is_connected:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/vernier/command/{command}",
                timeout=config.HTTP_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Comando '{command}': {result.get('result', 'OK')}")
                return result
            else:
                print(f"⚠️ Comando HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error comando {command}: {e}")
        
        return None
    
    # Métodos de conveniencia para comandos Arduino
    def change_to_temperature(self):
        """Comando 't' - Cambiar a sensor temperatura"""
        return self.send_vernier_command('t')
    
    def change_to_force(self):
        """Comando 'f' - Cambiar a sensor fuerza"""
        return self.send_vernier_command('f')
    
    def change_to_photogate(self):
        """Comando 'p' - Cambiar a fotopuerta"""
        return self.send_vernier_command('p')
    
    def change_to_motion(self):
        """Comando 'm' - Cambiar a sensor movimiento"""
        return self.send_vernier_command('m')
    
    def stop_readings(self):
        """Comando 'd' - Detener lecturas"""
        return self.send_vernier_command('d')
    
    def continue_readings(self):
        """Comando 'c' - Continuar lecturas"""
        return self.send_vernier_command('c')
    
    # Métodos originales sin cambios...
    def get_device_status(self):
        """Status del dispositivo (actualizado)"""
        if not self.base_url:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/status",
                timeout=config.HTTP_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Status HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error status: {e}")
        
        return None
    
    def ping(self):
        """Test conectividad (sin cambios)"""
        if not self.base_url:
            return False
        
        try:
            response = requests.get(f"{self.base_url}/ping", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def reconnect(self):
        """Reconectar (sin cambios)"""
        if not self.base_url:
            return False
        
        try:
            url_parts = self.base_url.replace('http://', '').split(':')
            ip = url_parts[0]
            port = int(url_parts[1]) if len(url_parts) > 1 else 8080
            
            print("🔄 Reconectando...")
            return self.connect(ip, port)
            
        except Exception as e:
            print(f"❌ Error reconexión: {e}")
            return False
    
    def get_connection_info(self):
        """Info de conexión (sin cambios)"""
        return {
            'base_url': self.base_url,
            'is_connected': self.is_connected,
            'last_successful_request': self.last_successful_request,
            'consecutive_errors': self.consecutive_errors,
            'connection_age': time.time() - self.last_successful_request if self.last_successful_request else None
        }