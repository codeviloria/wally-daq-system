# 🔬 Wally - Sistema de Adquisición de Datos ESP32 + Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MicroPython](https://img.shields.io/badge/MicroPython-ESP32-green.svg)](https://micropython.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-brightgreen.svg)](https://github.com)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-orange.svg)](https://arduino.cc)

Sistema híbrido de adquisición de datos para sensores Vernier que permite **cambio dinámico de sensores sin pérdida de datos**. Migrado desde Arduino a ESP32 con MicroPython manteniendo 100% compatibilidad de comandos.

## 👨‍💻 Consultoría y Desarrollo
**Desarrollado por:** [Ingeniero Gino Viloria](mailto:codevilor.ia@gmail.com)  
**Especialización:** Sistemas IoT, Adquisición de Datos, Python & MicroPython  
**Consultoría disponible:** Implementación, customización y soporte técnico

📧 **Contacto profesional:** codevilor.ia@gmail.com  
🔗 **LinkedIn:** [linkedin.com/in/gino-viloria](https://linkedin.com/in/gino-viloria)  
💼 **Servicios:** Desarrollo de prototipos, integración de sensores, sistemas DAQ personalizados

## 🔄 Migración Arduino → ESP32 Completa

### **Arquitectura Original vs Nueva**

```
ANTES (Arduino):                    DESPUÉS (ESP32 + Python):
┌─────────────────┐                ┌─────────────────┐    ┌─────────────────┐
│     Arduino     │ Serial         │     ESP32       │ WiFi │   PC Python     │
│   + VernierLib  │◄──────────────►│  MicroPython    │◄────►│  Tkinter UI     │
│   + 4 Sensores  │                │  + HTTP Server  │      │  + Dashboard    │
└─────────────────┘                └─────────────────┘      └─────────────────┘
```

### **🔌 Mapeo de Puertos Arduino → ESP32**

| **Sensor** | **Arduino Pin** | **ESP32 GPIO** | **Función** | **Tipo** |
|------------|-----------------|----------------|-------------|----------|
| 🌡️ **Temperatura** | A0 (Analog) | **GPIO 34** | ADC1_CH6 | Entrada Analógica |
| ⚡ **Fuerza** | A1 (Analog) | **GPIO 35** | ADC1_CH7 | Entrada Analógica |
| 📷 **Fotopuerta** | D2 (Digital) | **GPIO 4** | Input/Pull-up | Entrada Digital |
| 📐 **Movimiento Echo** | D2 (Digital) | **GPIO 18** | Input | Entrada Digital |
| 🔊 **Movimiento Trigger** | D3 (Digital) | **GPIO 5** | Output | Salida Digital |
| 💡 **LED Status** | D13 (Digital) | **GPIO 2** | Output | LED Integrado |

### **⚡ Comandos Arduino Migrados**

| **Comando** | **Función Original** | **Nueva Implementación** | **URL HTTP** |
|-------------|---------------------|--------------------------|--------------|
| `t` | Cambiar a Temperatura | ✅ HTTP GET | `/vernier/command/t` |
| `f` | Cambiar a Fuerza | ✅ HTTP GET | `/vernier/command/f` |
| `p` | Cambiar a Fotopuerta | ✅ HTTP GET | `/vernier/command/p` |
| `m` | Cambiar a Movimiento | ✅ HTTP GET | `/vernier/command/m` |
| `d` | Detener lecturas | ✅ HTTP GET | `/vernier/command/d` |
| `c` | Continuar lecturas | ✅ HTTP GET | `/vernier/command/c` |

### **🔬 Sensores Vernier Soportados**

```cpp
// Código Arduino Original:
#define SENSOR_TEMPERATURA 1    // TMP36 en A0
#define SENSOR_FUERZA 2        // Dual-Range Force + VernierLib 
#define SENSOR_FOTOPUERTA 3    // Photogate en D2
#define SENSOR_MOVIMIENTO 4    // Ultrasonico HC-SR04 D2/D3
```

```python
# Migración ESP32 MicroPython:
SENSOR_TEMPERATURA = 1    # ADC GPIO34 - TMP36 compatible
SENSOR_FUERZA = 2        # ADC GPIO35 - Calibración Vernier
SENSOR_FOTOPUERTA = 3    # GPIO4 - Detección estado + LED
SENSOR_MOVIMIENTO = 4    # GPIO5/18 - Ultrasonico timing
```

## 🏗️ Arquitectura del Sistema

```
ESP32 (MicroPython) ←→ HTTP/JSON ←→ Python Controller ←→ Tkinter UI
     │                                    │                    │
┌────▼────────────────┐          ┌────────▼────────┐    ┌─────▼─────────────┐
│ • Sensores Vernier  │          │ • Data Manager  │    │ • Dashboard       │
│ • Servidor HTTP     │          │ • Buffer Logic  │    │ • Real-time Plots │
│ • Comandos Arduino  │          │ • CSV Export    │    │ • Sensor Control  │
│ • Auto-detección    │          │ • Threading     │    │ • Status Monitor  │
└─────────────────────┘          └─────────────────┘    └───────────────────┘
```

## ⚡ Características

### **🆕 Nuevas Funcionalidades (vs Arduino):**
- ✅ **WiFi Integration** - Control remoto via HTTP
- ✅ **Interfaz gráfica profesional** con Tkinter
- ✅ **Gráficos en tiempo real** con matplotlib
- ✅ **Export CSV automático** con timestamps
- ✅ **Buffer circular inteligente** - sin pérdida de memoria
- ✅ **Threading** para UI responsive
- ✅ **Reconexión automática** WiFi/HTTP
- ✅ **Hot-swapping** de sensores sin reinicio

### **✅ Funcionalidad Arduino Preservada:**
- ✅ **Comandos idénticos** (`t`, `f`, `p`, `m`, `d`, `c`)
- ✅ **Calibraciones Vernier** específicas por sensor
- ✅ **Control LED** con threshold (sensor fuerza)
- ✅ **Timing preciso** fotopuerta y ultrasonido
- ✅ **VernierLib equivalence** - autoID simulation
- ✅ **Formato de salida** compatible

## 📁 **Estructura del Repositorio**

```
wally-daq-system/
├── LICENSE                                    # → Licencia del proyecto (MIT)
├── README.md                                  # → Documentación principal del sistema
├── requirements.txt                           # → Dependencias Python para PC
├── data/                                      # → Directorio para almacenar datos CSV exportados
├── docs/                                      # ← Documentación técnica y guías
│   ├── installation.md                        # → Guía detallada de instalación paso a paso
│   └── 🔬 Wally DAQ System - Guía Setup Estudiantes.md  # → Guía específica para estudiantes
├── esp32/                                     # ← Código MicroPython para ESP32
│   ├── boot.py                                # → Secuencia de arranque automático del ESP32
│   ├── config.py                              # → Configuración WiFi, pines y calibraciones
│   ├── main.py                                # → Programa principal (equivale a setup() y loop() de Arduino)
│   ├── sensor_server.py                       # → Servidor HTTP + manejo de sensores Vernier
│   └── vernier_sensors_migrated.py           # → Migración específica de sensores Vernier desde Arduino
├── pc_controller/                             # ← Aplicación cliente Python/Tkinter
│   ├── config.py                              # → Configuración del cliente PC (IP, puertos, intervalos)
│   ├── data_manager.py                        # → Gestión de datos, buffer circular y export CSV
│   ├── esp32_client.py                        # → Cliente HTTP para comunicación con ESP32
│   ├── esp32_client_backup.py                 # → Respaldo de versión anterior del cliente
│   ├── main.py                                # → Controlador principal y punto de entrada
│   ├── main_backup.py                         # → Respaldo de versión anterior del main
│   ├── ui_dashboard.py                        # → Interfaz gráfica con controles y gráficos tiempo real
│   ├── ui_dashboard_backup.py                 # → Respaldo de versión anterior de la interfaz
│   └── utils.py                               # → Funciones utilitarias y helpers
└── scripts/                                   # ← Scripts de instalación y configuración
    ├── install_esp32.bat                      # → Script Windows para flashear ESP32 automáticamente
    ├── install_esp32.sh                       # → Script Linux/macOS para flashear ESP32 automáticamente
    ├── setup_environment.bat                  # → Setup completo del entorno en Windows
    └── setup_environment.sh                   # → Setup completo del entorno en Linux/macOS
```

### 📋 **Descripción de Archivos Clave**

| Archivo | Función Principal | Tecnología |
|---------|------------------|------------|
| `esp32/main.py` | Punto de entrada ESP32, inicia servidor HTTP | MicroPython |
| `esp32/sensor_server.py` | Manejo de sensores + API REST compatible Arduino | MicroPython |
| `esp32/config.py` | Configuración WiFi y mapeo de pines ESP32 | MicroPython |
| `pc_controller/main.py` | Aplicación cliente principal con GUI | Python + Tkinter |
| `pc_controller/ui_dashboard.py` | Interfaz gráfica y visualización tiempo real | Tkinter + matplotlib |
| `pc_controller/data_manager.py` | Buffer de datos y exportación CSV | Python + pandas |
| `esp32/vernier_sensors_migrated.py` | Migración específica de funciones Vernier | MicroPython |

### 🔧 **Archivos de Configuración**

- **`esp32/config.py`**: WiFi, pines GPIO, calibraciones Vernier
- **`pc_controller/config.py`**: IP ESP32, intervalos, configuración UI
- **`requirements.txt`**: Dependencias Python (requests, matplotlib, pandas, etc.)

### 📜 **Scripts de Automatización**

- **`scripts/setup_environment.*`**: Instalación completa del entorno
- **`scripts/install_esp32.*`**: Flash automático del ESP32 con MicroPython

## 🚀 Quick Start

### 1. Clonar repositorio
```bash
git clone https://github.com/codeviloria/wally-daq-system.git
cd wally-daq-system
```

### 2. Setup Multiplataforma

#### 🐧 Linux/macOS:
```bash
# Setup automático
./scripts/setup_environment.sh

# O manual:
python3 -m venv wally_env
source wally_env/bin/activate
pip install -r requirements.txt
```

#### 🪟 Windows:
```cmd
REM Setup automático
scripts\setup_environment.bat

REM O manual:
python -m venv wally_env
wally_env\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar ESP32

#### Editar configuración WiFi:
```python
# Archivo: esp32/config.py
WIFI_SSID = "TU_WIFI_AQUI"          # ← CAMBIAR
WIFI_PASSWORD = "TU_PASSWORD_AQUI"  # ← CAMBIAR
```

#### Flashear ESP32:

🐧 **Linux/macOS:**
```bash
# Script automático
./scripts/install_esp32.sh /dev/ttyUSB0

# Manual
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
ampy --port /dev/ttyUSB0 put esp32/main.py
ampy --port /dev/ttyUSB0 put esp32/config.py
ampy --port /dev/ttyUSB0 put esp32/sensor_server.py
ampy --port /dev/ttyUSB0 put esp32/boot.py
```

🪟 **Windows:**
```cmd
REM Script automático
scripts\install_esp32.bat COM3

REM Manual
esptool.py --chip esp32 --port COM3 erase_flash
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
ampy --port COM3 put esp32/main.py
ampy --port COM3 put esp32/config.py
ampy --port COM3 put esp32/sensor_server.py
ampy --port COM3 put esp32/boot.py
```

### 4. Ejecutar Sistema

#### 🐧 Linux/macOS:
```bash
# Terminal 1: ESP32
screen /dev/ttyUSB0 115200
# En REPL: exec(open('main.py').read())

# Terminal 2: Aplicación Python
cd pc_controller
python main.py
```

#### 🪟 Windows:
```cmd
REM Terminal 1: ESP32
python -m serial.tools.miniterm COM3 115200
REM En REPL: exec(open('main.py').read())

REM Terminal 2: Aplicación Python
cd pc_controller
python main.py
```

## 🔧 Hardware Setup

### **Conexiones ESP32 ↔ Vernier Shield**

```
Vernier Shield    →    ESP32 DevKit v1
═══════════════════════════════════════
ANALOG 1 (A0)     →    GPIO 34 (ADC1_CH6) - Temperatura
ANALOG 2 (A1)     →    GPIO 35 (ADC1_CH7) - Fuerza  
DIGITAL 1 (D2)    →    GPIO 4 (Pull-up)   - Fotopuerta
DIGITAL 2 (D3)    →    GPIO 5 (Output)    - Trigger Ultrasonido
Echo Ultrasonido  →    GPIO 18 (Input)    - Echo Ultrasonido
LED Status (D13)  →    GPIO 2 (Built-in)  - LED Status
VCC (5V)          →    VIN                - Alimentación
GND               →    GND                - Tierra
```

### **Sensores Compatibles:**
- **🌡️ Temperatura**: TMP36, Stainless Steel Temperature Probe
- **⚡ Fuerza**: Dual-Range Force Sensor (±10N, ±50N)
- **📷 Fotopuerta**: Photogate Head, Light Gate
- **📐 Movimiento**: Motion Detector, HC-SR04 Ultrasonico

## 📊 Nueva Interfaz vs Arduino

### **Antes (Arduino Serial Monitor):**
```
Seleccione un sensor:
t: Temperatura
f: Fuerza  
p: Fotopuerta
m: Movimiento

Temperature: 23.5
Temperature: 23.7
```

### **Ahora (Tkinter Dashboard):**

```
🔬 Wally - Sistema de Adquisición de Datos        🟢 Adquisición activa
═══════════════════════════════════════════════════════════════════

📊 Sensores en Tiempo Real    │    📈 Gráficos en Tiempo Real
                               │
🌡️ Temperatura: 23.5°C ✅     │    [Gráfico temp en tiempo real]
⚡ Fuerza: 12.3N ✅           │    [Gráfico fuerza en tiempo real]  
📷 Fotopuerta: Abierta ✅     │    [Gráfico eventos fotopuerta]
📐 Movimiento: 15.2cm ✅      │    [Gráfico distancia ultrasonido]

🎛️ Controles Sistema
[▶️ Iniciar] [⏹️ Detener] [📥 Exportar CSV]   📊 Lecturas: 1,234 | Duración: 02:15:30

🔬 Control Sensores Vernier (Arduino Compatible)
Cambiar Sensor: [🌡️ Temperatura] [⚡ Fuerza] [📷 Fotopuerta] [📐 Movimiento]
Control Lecturas: [⏸️ Pausar] [▶️ Continuar]  Estado: Sensor: Temperatura ✅ Lecturas: Activas
```

## 🌐 API REST Endpoints

### **Endpoints Principales:**
```bash
GET /sensors                    # Todos los sensores (genéricos + Vernier)
GET /status                     # Status sistema completo
GET /ping                       # Test conectividad
```

### **Endpoints Vernier (Arduino Compatible):**
```bash
GET /vernier/command/t          # Cambiar a temperatura (Arduino 't')
GET /vernier/command/f          # Cambiar a fuerza (Arduino 'f')
GET /vernier/command/p          # Cambiar a fotopuerta (Arduino 'p')
GET /vernier/command/m          # Cambiar a movimiento (Arduino 'm')
GET /vernier/command/d          # Detener lecturas (Arduino 'd')
GET /vernier/command/c          # Continuar lecturas (Arduino 'c')
GET /vernier/status             # Status específico Vernier
GET /vernier/active             # Solo sensor activo actual
```

### **Ejemplo Response JSON:**
```json
{
  "device_id": "esp32_wally_vernier",
  "timestamp": 1609459200.123,
  "readings": {
    "vernier_temperatura": {
      "sensor_type": "temperatura",
      "value": 23.7,
      "unit": "°C",
      "vernier_id": 1,
      "source": "vernier"
    },
    "vernier_fuerza": {
      "sensor_type": "fuerza", 
      "value": 12.5,
      "unit": "N",
      "threshold": 100.0,
      "led_status": false,
      "vernier_id": 2,
      "source": "vernier"
    }
  },
  "vernier_active_sensor": 1,
  "arduino_compatible": true
}
```

## 🧪 Testing y Validación

### **Compatibilidad Arduino Verificada:**

```bash
# Test comandos originales via HTTP
curl http://ESP32_IP:8080/vernier/command/t    # ✅ Temperatura
curl http://ESP32_IP:8080/vernier/command/f    # ✅ Fuerza  
curl http://ESP32_IP:8080/vernier/command/p    # ✅ Fotopuerta
curl http://ESP32_IP:8080/vernier/command/m    # ✅ Movimiento
curl http://ESP32_IP:8080/vernier/command/d    # ✅ Pausar
curl http://ESP32_IP:8080/vernier/command/c    # ✅ Continuar
```

### **Benchmark Arduino vs ESP32:**

| **Aspecto** | **Arduino Original** | **ESP32 Migrado** | **Mejora** |
|-------------|---------------------|------------------|------------|
| **Resolución ADC** | 10-bit (0-1023) | 12-bit (0-4095) | **4x mejor** |
| **Velocidad CPU** | 16 MHz | 240 MHz | **15x más rápido** |
| **Memoria RAM** | 2KB | 520KB | **260x más memoria** |
| **Conectividad** | ❌ Solo Serial | ✅ WiFi + HTTP | **Inalámbrico** |
| **Interfaz** | ❌ Monitor Serial | ✅ GUI Profesional | **Visual** |
| **Storage** | ❌ Sin persistencia | ✅ CSV + Buffer | **Persistente** |
| **Multi-sensor** | ❌ Uno a la vez | ✅ Todos simultáneos | **Paralelo** |

## 📋 Configuración

### **ESP32 (esp32/config.py):**
```python
# WiFi - EDITAR OBLIGATORIO
WIFI_SSID = "TU_WIFI"
WIFI_PASSWORD = "TU_PASSWORD" 

# Pines Hardware (mapeo Arduino)
SENSOR_PINS = {
    'temperatura': 34,  # A0 → GPIO34
    'fuerza': 35,      # A1 → GPIO35  
    'fotopuerta': 4,   # D2 → GPIO4
    'trigger': 5,      # D3 → GPIO5
    'echo': 18,        # Nuevo para ultrasonido
    'led': 2          # D13 → GPIO2
}

# Calibraciones Vernier
SENSOR_CALIBRATION = {
    'temperatura': {'slope': 100.0, 'offset': -50.0, 'unit': '°C'},
    'fuerza': {'slope': 50.0, 'offset': -25.0, 'unit': 'N'},
    'fotopuerta': {'slope': 1.0, 'offset': 0.0, 'unit': 'blocked'},
    'movimiento': {'slope': 1.0, 'offset': 0.0, 'unit': 'cm'}
}
```

### **PC (pc_controller/config.py):**
```python
ESP32_IP = "192.168.1.100"  # ← IP del ESP32 (mostrada en consola)
SAMPLE_INTERVAL = 1.0       # segundos entre lecturas
MAX_BUFFER_SIZE = 1000      # entradas máximas en buffer
```

## 🛠️ Desarrollo y Testing

```bash
# Desarrollo modo standalone
cd pc_controller
python main.py

# Testing unitario
python -m pytest tests/

# Scripts utilidad
./scripts/setup_environment.sh     # Setup completo
./scripts/install_esp32.sh         # Flash ESP32

# Debugging ESP32
screen /dev/ttyUSB0 115200          # Monitor serie
curl http://ESP32_IP:8080/ping      # Test HTTP
```

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles

## 🎯 Casos de Uso

### **Educación:**
- **Laboratorios de física** - Experimentos con múltiples sensores
- **Cursos de ingeniería** - Ejemplo de migración hardware/software
- **Proyectos estudiantiles** - Sistema DAQ completo funcional

### **Investigación:**
- **Adquisición de datos continua** - 24/7 sin intervención
- **Experimentos remotos** - Control via WiFi
- **Análisis en tiempo real** - Gráficos y tendencias inmediatas

### **Industria:**
- **Prototipos IoT** - Base para sistemas de monitoreo
- **Control de calidad** - Mediciones automatizadas
- **Mantenimiento predictivo** - Sensores en equipos críticos

## 💼 Servicios de Consultoría

### **Ingeniero Gino Viloria - Especialista en Sistemas DAQ**

**🔧 Servicios Disponibles:**
- ✅ **Migración Arduino → ESP32** - Sistemas legacy a IoT moderno
- ✅ **Implementación personalizada** de sistemas de adquisición de datos
- ✅ **Integración de sensores** específicos y calibración avanzada
- ✅ **Optimización de performance** para aplicaciones industriales
- ✅ **Desarrollo de interfaces** web y desktop personalizadas
- ✅ **Soporte técnico** y mantenimiento de sistemas DAQ
- ✅ **Capacitación** en Python, MicroPython y ESP32

**📞 Contacto Profesional:**
- 📧 **Email:** codevilor.ia@gmail.com
- 🔗 **LinkedIn:** [linkedin.com/in/gino-viloria](https://linkedin.com/in/gino-viloria)
- 💻 **GitHub:** [github.com/codeviloria](https://github.com/codeviloria)

**🎓 Especialización:**
- **Sistemas IoT** y automatización industrial
- **Adquisición de datos** en tiempo real
- **Python/MicroPython** para sistemas embebidos
- **Arquitecturas híbridas** ESP32 + PC
- **Sensores científicos** e industriales
- **Migración legacy** Arduino/PIC a ESP32

**💡 Proyectos Similares:**
- Sistemas DAQ para universidades
- Monitoreo ambiental IoT  
- Control industrial con ESP32
- Interfaces HMI personalizadas
- Integración sensores Vernier/Pasco

---

**🏆 Proyecto Destacado:** Migración completa Arduino → ESP32 manteniendo 100% compatibilidad de comandos mientras se agrega conectividad WiFi, interfaz gráfica profesional y capacidades IoT modernas.

**Desarrollado para proyectos académicos y aplicaciones industriales**  
**© 2025 Ingeniero Gino Viloria - Consultoría en Sistemas DAQ**