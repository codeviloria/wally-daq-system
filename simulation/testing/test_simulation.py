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
