"""
Wally ESP32 Sensor Server
Sistema de adquisición de datos para sensores Vernier
"""
import machine
import network
import socket
import ujson
import time
from sensor_server import SensorServer

def main():
    print("🔬 Iniciando Wally ESP32 Sensor Server...")
    
    # Configurar WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Leer configuración
    try:
        with open('config.py', 'r') as f:
            config_code = f.read()
        exec(config_code)
    except:
        print("❌ Error cargando config.py")
        return
    
    # Conectar WiFi
    if not wlan.isconnected():
        print(f"📡 Conectando a {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
    
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"\n✅ WiFi conectado - IP: {ip}")
        
        # Iniciar servidor de sensores
        server = SensorServer(ip, SERVER_PORT)
        server.start()
    else:
        print("\n❌ Error conectando WiFi")

if __name__ == "__main__":
    main()