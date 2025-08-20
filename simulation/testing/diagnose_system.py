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
