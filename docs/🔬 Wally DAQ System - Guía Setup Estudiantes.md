# 🔬 Wally DAQ System - Guía Setup Estudiantes

## ⚡ Setup Rápido (15 minutos)

### 1. **Prerequisitos**
```bash
# Instalar Python 3.8+ y pip
python --version  # Debe ser 3.8+
pip --version

# Instalar herramientas ESP32
pip install esptool adafruit-ampy
```

### 2. **Clonar Proyecto**
```bash
git clone https://github.com/codeviloria/wally-daq-system.git
cd wally-daq-system
```

### 3. **Setup Entorno Python**
```bash
# Linux/macOS
python3 -m venv wally_env
source wally_env/bin/activate
pip install -r requirements.txt

# Windows
python -m venv wally_env
wally_env\Scripts\activate
pip install -r requirements.txt
```

### 4. **Configurar WiFi ESP32**
Editar archivo: `esp32/config.py`
```python
# SOLO CAMBIAR ESTAS 2 LÍNEAS:
WIFI_SSID = "WIFI_DEL_LABORATORIO"     # ← TU WIFI
WIFI_PASSWORD = "PASSWORD_LABORATORIO" # ← TU PASSWORD
```

### 5. **Flash ESP32**
```bash
# Detectar puerto ESP32
# Linux: /dev/ttyUSB0 o /dev/ttyACM0
# Windows: COM3, COM4, etc.
# macOS: /dev/cu.usbserial-*

# Borrar flash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# Instalar MicroPython
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

# Subir código
ampy --port /dev/ttyUSB0 put esp32/main.py
ampy --port /dev/ttyUSB0 put esp32/config.py  
ampy --port /dev/ttyUSB0 put esp32/sensor_server.py
ampy --port /dev/ttyUSB0 put esp32/boot.py
```

### 6. **Conectar Hardware**
```
Vernier Shield → ESP32 DevKit v1
═══════════════════════════════════════
🌡️ Temperatura (A0) → GPIO 34
⚡ Fuerza (A1)      → GPIO 35  
📷 Fotopuerta (D2)  → GPIO 4
📐 Trigger (D3)     → GPIO 5
   Echo             → GPIO 18
💡 LED (D13)        → GPIO 2 (interno)
🔌 VCC (5V)         → VIN
🔌 GND              → GND
```

### 7. **Ejecutar Sistema**
```bash
# Terminal 1: Monitor ESP32 (opcional)
screen /dev/ttyUSB0 115200
# En REPL: exec(open('main.py').read())

# Terminal 2: Cliente Python
cd pc_controller
python main.py
```

## ✅ **Verificación Sistema Funcional**

### Test Conexión ESP32:
```bash
# El ESP32 debe mostrar en consola:
# 🔬 Wally DAQ System
# WiFi connected: 192.168.1.XXX
# Server started on port 8080

# Test desde PC:
curl http://192.168.1.XXX:8080/ping
# Respuesta: {"pong": 1609459200.123}
```

### Test Comandos Arduino:
```bash
# Cambiar sensores (igual que Arduino)
curl http://192.168.1.XXX:8080/vernier/command/t  # Temperatura
curl http://192.168.1.XXX:8080/vernier/command/f  # Fuerza
curl http://192.168.1.XXX:8080/vernier/command/p  # Fotopuerta
curl http://192.168.1.XXX:8080/vernier/command/m  # Movimiento
curl http://192.168.1.XXX:8080/vernier/command/d  # Detener
curl http://192.168.1.XXX:8080/vernier/command/c  # Continuar
```

### Test Interfaz Python:
- ✅ Ventana Tkinter se abre
- ✅ Gráficos en tiempo real funcionan
- ✅ Botones de control responden
- ✅ Export CSV funciona
- ✅ Datos se muestran correctamente

## 🎛️ **Uso del Sistema**

### Comandos Disponibles:
| Comando | Función | URL |
|---------|---------|-----|
| `t` | Temperatura | `/vernier/command/t` |
| `f` | Fuerza | `/vernier/command/f` |
| `p` | Fotopuerta | `/vernier/command/p` |
| `m` | Movimiento | `/vernier/command/m` |
| `d` | Detener | `/vernier/command/d` |
| `c` | Continuar | `/vernier/command/c` |

### Interfaz Python:
- 🟢 **Iniciar**: Comenzar recolección datos
- 🔴 **Detener**: Parar recolección  
- 💾 **Guardar CSV**: Export datos
- 🎛️ **Comandos**: Botones t, f, p, m, d, c
- 📊 **Gráfico**: Tiempo real automático

## 🔧 **Desarrollo y Personalización**

### Agregar Nuevos Sensores:
1. Editar `esp32/sensor_server.py`
2. Agregar configuración en `esp32/config.py`
3. Actualizar mapeo de comandos

### Modificar Calibraciones:
```python
# En esp32/config.py
SENSOR_CALIBRATION = {
    'temperatura': {'slope': 100.0, 'offset': -50.0},
    'fuerza': {'slope': 50.0, 'offset': -25.0},
    # Agregar nuevos sensores aquí
}
```

### Personalizar Interfaz:
- Archivo: `pc_controller/ui_dashboard.py`
- Framework: Tkinter + matplotlib
- Fácil modificación de layouts y gráficos

## 🐛 **Troubleshooting**

### ESP32 no conecta WiFi:
1. Verificar SSID/password en `config.py`
2. Revisar que WiFi sea 2.4GHz (no 5GHz)
3. Monitor serie: `screen /dev/ttyUSB0 115200`

### Puerto ESP32 no encontrado:
```bash
# Linux: Ver puertos disponibles
ls /dev/tty*

# Windows: Device Manager → Ports
# macOS: ls /dev/cu.*
```

### Cliente Python no conecta:
1. Verificar IP ESP32 en consola serie
2. Editar `pc_controller/config.py` con IP correcta
3. Test ping: `curl http://IP:8080/ping`

### Sensores no leen correctamente:
1. Verificar conexiones hardware
2. Revisar calibraciones en `esp32/config.py`
3. Test individual: `curl http://IP:8080/vernier/active`

## 📚 **Recursos Adicionales**

- **Documentación Vernier**: Calibraciones y especificaciones
- **ESP32 MicroPython**: https://docs.micropython.org/en/latest/esp32/
- **Tkinter GUI**: https://docs.python.org/3/library/tkinter.html
- **matplotlib**: https://matplotlib.org/stable/tutorials/

## 🎯 **Objetivos del Proyecto**

### Estudiantes pueden:
- ✅ Migrar sistemas Arduino a ESP32
- ✅ Crear interfaces gráficas profesionales  
- ✅ Implementar comunicación WiFi/HTTP
- ✅ Desarrollar sistemas de adquisición de datos
- ✅ Trabajar con sensores científicos
- ✅ Crear sistemas híbridos embebido + PC

### Entregables:
1. Sistema funcional completo
2. Documentación técnica
3. Manual de usuario
4. Casos de prueba
5. Extensiones personalizadas

---

**💡 El sistema está 100% funcional tal como está. Pueden enfocarse en desarrollo y mejoras, no en debugging básico.**