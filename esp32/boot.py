"""
Boot script para ESP32 - Wally DAQ
Configuración inicial del sistema
"""
import gc
import machine
import esp

# Optimizar rendimiento
esp.osdebug(None)  # Desactivar debug del OS
gc.collect()       # Garbage collection inicial

# Configurar LED indicador (opcional)
try:
    led = machine.Pin(2, machine.Pin.OUT)
    led.on()  # LED encendido = sistema iniciando
except:
    pass

print("🔬 Wally ESP32 - Boot sequence iniciada")
print(f"📊 Memoria libre: {gc.mem_free()} bytes")