"""
Cliente HTTP para comunicación con ESP32
"""
import requests
import time
import json
import config

class ESP32Client:
    """Cliente para comunicación con ESP32 via HTTP"""
    
    def __init__(self):
        self.base_url = None
        self.is_connected = False
        self.last_successful_request = None
        self.consecutive_errors = 0
        
        print("🌐 ESP32 Client inicializado")
    
    def connect(self, ip_address, port=8080):
        """Establecer conexión con ESP32"""
        self.base_url = f"http://{ip_address}:{port}"
        
        try:
            # Test de conectividad básico
            print(f"🔗 Intentando conectar a {self.base_url}...")
            
            response = requests.get(
                f"{self.base_url}/ping", 
                timeout=config.CONNECTION_TIMEOUT
            )
            
            if response.status_code == 200:
                self.is_connected = True
                self.consecutive_errors = 0
                self.last_successful_request = time.time()
                
                print(f"✅ Conectado exitosamente a ESP32")
                
                # Obtener información del dispositivo
                status_info = self.get_device_status()
                if status_info:
                    device_id = status_info.get('device_id', 'unknown')
                    sensors_count = status_info.get('sensors_configured', 0)
                    print(f"📱 Dispositivo: {device_id}")
                    print(f"🔧 Sensores configurados: {sensors_count}")
                
                return True
            else:
                print(f"❌ Respuesta HTTP inválida: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout conectando a {self.base_url}")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Error de conexión a {self.base_url}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        self.is_connected = False
        return False
    
    def get_sensor_data(self):
        """Obtener datos de sensores del ESP32"""
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
                print(f"⚠️ HTTP {response.status_code} obteniendo datos")
                self.consecutive_errors += 1
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout obteniendo datos de sensores")
            self.consecutive_errors += 1
        except requests.exceptions.ConnectionError:
            print("🔌 Error de conexión obteniendo datos")
            self.consecutive_errors += 1
            self.is_connected = False
        except json.JSONDecodeError:
            print("📄 Error decodificando JSON del ESP32")
            self.consecutive_errors += 1
        except Exception as e:
            print(f"❌ Error inesperado obteniendo datos: {e}")
            self.consecutive_errors += 1
        
        # Si hay demasiados errores consecutivos, marcar como desconectado
        if self.consecutive_errors >= config.RETRY_ATTEMPTS:
            self.is_connected = False
            print(f"🔴 Demasiados errores consecutivos ({self.consecutive_errors})")
        
        return None
    
    def get_device_status(self):
        """Obtener status del dispositivo ESP32"""
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
                print(f"⚠️ HTTP {response.status_code} obteniendo status")
                
        except Exception as e:
            print(f"❌ Error obteniendo status: {e}")
        
        return None
    
    def ping(self):
        """Test de conectividad simple"""
        if not self.base_url:
            return False
        
        try:
            response = requests.get(
                f"{self.base_url}/ping",
                timeout=2
            )
            return response.status_code == 200
            
        except:
            return False
    
    def reconnect(self):
        """Intentar reconexión"""
        if not self.base_url:
            return False
        
        # Extraer IP y puerto del URL
        try:
            url_parts = self.base_url.replace('http://', '').split(':')
            ip = url_parts[0]
            port = int(url_parts[1]) if len(url_parts) > 1 else 8080
            
            print("🔄 Intentando reconexión...")
            return self.connect(ip, port)
            
        except Exception as e:
            print(f"❌ Error en reconexión: {e}")
            return False
    
    def get_connection_info(self):
        """Obtener información de conexión"""
        return {
            'base_url': self.base_url,
            'is_connected': self.is_connected,
            'last_successful_request': self.last_successful_request,
            'consecutive_errors': self.consecutive_errors,
            'connection_age': time.time() - self.last_successful_request if self.last_successful_request else None
        }