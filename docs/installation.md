# 📥 Instalación Wally DAQ System - Migración Arduino → ESP32

## 🔄 Información de Migración

Este sistema es una **migración completa de Arduino a ESP32** manteniendo 100% compatibilidad con sensores Vernier y comandos originales, agregando conectividad WiFi e interfaz gráfica profesional.

### **Migración desde Arduino:**
- ✅ **Comandos idénticos**: `t`, `f`, `p`, `m`, `d`, `c`
- ✅ **Sensores Vernier**: Temperatura, Fuerza, Fotopuerta, Movimiento
- ✅ **Calibraciones preservadas**: VernierLib equivalence
- ✅ **Funcionalidad ampliada**: WiFi + GUI + Export CSV

## 📋 Prerrequisitos

### Hardware Requerido

#### **ESP32 Setup:**
- **ESP32 DevKit v1** (recomendado para compatibilidad)
- **Vernier Shield** o protoboard + resistencias
- **Sensores Vernier compatibles**:
  - 🌡️ **Temperatura**: TMP36, Stainless Steel Temperature Probe
  - ⚡ **Fuerza**: Dual-Range Force Sensor (±10N, ±50N)
  - 📷 **Fotopuerta**: Photogate Head, Light Gate
  - 📐 **Movimiento**: Motion Detector, HC-SR04 Ultrasonico
- **Cables jumper** y **resistencias pull-up**
- **Fuente de alimentación** USB o externa 5V

#### **Conexiones Hardware (Arduino → ESP32):**
```
Sensor/Función       Arduino Pin    →    ESP32 GPIO    Tipo
═══════════════════════════════════════════════════════════
🌡️ Temperatura      A0 (Analog)    →    GPIO 34       ADC1_CH6
⚡ Fuerza           A1 (Analog)    →    GPIO 35       ADC1_CH7
📷 Fotopuerta       D2 (Digital)   →    GPIO 4        Input/Pull-up
📐 Trigger Ultrasonido  D3 (Digital)   →    GPIO 5        Output
📐 Echo Ultrasonido     D2 (Digital)   →    GPIO 18       Input
💡 LED Status       D13 (Digital)  →    GPIO 2        LED Integrado
🔌 VCC              5V             →    VIN           Alimentación
⚡ GND              GND            →    GND           Tierra
```

### Software Multiplataforma

#### 🪟 Windows:
- **Python 3.8+** (desde Microsoft Store o python.org)
- **Git for Windows**
- **Drivers USB ESP32** (CP210x o CH340)
- **Terminal**: PowerShell, CMD, o Windows Terminal
- **Editor opcional**: VS Code, Thonny IDE

#### 🐧 Linux:
- **Python 3.8+**: `sudo apt install python3 python3-pip python3-tkinter`
- **Git**: `sudo apt install git`
- **Drivers USB**: automáticos en la mayoría de distribuciones
- **Tools**: `sudo apt install screen curl wget`

#### 🍎 macOS:
- **Python 3.8+**: Homebrew `brew install python`
- **Git**: Xcode Command Line Tools
- **Drivers USB**: automáticos
- **Tools**: incluidos en sistema

## 🚀 Instalación Paso a Paso

### 1. Clonar Repositorio

```bash
git clone https://github.com/codeviloria/wally-daq-system.git
cd wally-daq-system
```

### 2. Verificar Estructura (Opcional - para repos nuevos)

Si estás creando desde cero, genera la estructura:

#### 🐧 Linux/macOS:
```bash
# Comando único para crear todos los archivos
touch README.md requirements.txt .gitignore LICENSE \
esp32/main.py esp32/config.py esp32/sensor_server.py esp32/boot.py \
pc_controller/main.py pc_controller/config.py pc_controller/ui_dashboard.py pc_controller/data_manager.py pc_controller/esp32_client.py pc_controller/utils.py \
scripts/setup_environment.sh scripts/install_esp32.sh scripts/setup_environment.bat scripts/install_esp32.bat \
docs/installation.md data/.gitkeep

# Permisos de ejecución
chmod +x scripts/setup_environment.sh scripts/install_esp32.sh
```

#### 🪟 Windows PowerShell:
```powershell
# Crear estructura completa
$files = @(
    "README.md", "requirements.txt", ".gitignore", "LICENSE",
    "esp32/main.py", "esp32/config.py", "esp32/sensor_server.py", "esp32/boot.py",
    "pc_controller/main.py", "pc_controller/config.py", "pc_controller/ui_dashboard.py", 
    "pc_controller/data_manager.py", "pc_controller/esp32_client.py", "pc_controller/utils.py",
    "scripts/setup_environment.sh", "scripts/install_esp32.sh",
    "scripts/setup_environment.bat", "scripts/install_esp32.bat",
    "docs/installation.md", "data/.gitkeep"
)
$files | ForEach-Object { New-Item -ItemType File -Path $_ -Force }
```

### 3. Setup Entorno Python

#### 🐧 Linux/macOS:
```bash
# Opción 1: Script automático (recomendado)
./scripts/setup_environment.sh

# Opción 2: Manual
python3 -m venv wally_env
source wally_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación
python -c "import matplotlib, tkinter, requests; print('✅ Dependencias OK')"
```

#### 🪟 Windows:
```cmd
REM Opción 1: Script automático (recomendado)
scripts\setup_environment.bat

REM Opción 2: Manual
python -m venv wally_env
wally_env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Verificar instalación
python -c "import matplotlib, tkinter, requests; print('✅ Dependencias OK')"
```

### 4. Configurar Hardware ESP32

#### **Paso 4.1: Configuración WiFi (CRÍTICO)**

Editar archivo de configuración:

```bash
# Linux/macOS
nano esp32/config.py

# Windows
notepad esp32/config.py
```

**Contenido a modificar:**
```python
# esp32/config.py - CONFIGURACIÓN OBLIGATORIA

# WiFi Configuration - EDITAR ESTAS LÍNEAS
WIFI_SSID = "TU_WIFI_AQUI"          # ← CAMBIAR por tu red WiFi
WIFI_PASSWORD = "TU_PASSWORD_AQUI"  # ← CAMBIAR por tu contraseña

# Server Configuration (no cambiar)
SERVER_PORT = 8080
DEVICE_ID = "esp32_wally_vernier"

# Pin Configuration - Arduino Mapping (verificar si usas pins diferentes)
SENSOR_PINS = {
    'temperatura': 34,  # A0 → GPIO34 (ADC1_CH6)
    'fuerza': 35,      # A1 → GPIO35 (ADC1_CH7)
    'fotopuerta': 4,   # D2 → GPIO4 (Input + Pull-up)
    'trigger': 5,      # D3 → GPIO5 (Output)
    'echo': 18,        # Nuevo pin para echo ultrasonido
    'led_status': 2    # D13 → GPIO2 (LED integrado)
}

# Calibraciones Vernier (ajustar según sensores específicos)
SENSOR_CALIBRATION = {
    'temperatura': {'slope': 100.0, 'offset': -50.0, 'unit': '°C'},
    'fuerza': {'slope': 50.0, 'offset': -25.0, 'unit': 'N'},
    'fotopuerta': {'slope': 1.0, 'offset': 0.0, 'unit': 'blocked'},
    'movimiento': {'slope': 1.0, 'offset': 0.0, 'unit': 'cm'}
}
```

#### **Paso 4.2: Identificar Puerto ESP32**

Antes de flashear, identificar el puerto correcto:

🪟 **Windows:**
```cmd
# Método 1: Listar puertos COM
mode | findstr "COM"

# Método 2: Python (más detallado)
python -c "import serial.tools.list_ports; [print(f'{p.device}: {p.description}') for p in serial.tools.list_ports.comports()]"

# Resultado esperado: COM3, COM5, etc.
```

🐧 **Linux:**
```bash
# Método 1: Listar puertos USB
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# Método 2: Info detallada
dmesg | grep -i "cp210x\|ch341" | tail -5

# Método 3: udev info
lsusb | grep -i "cp210x\|silicon\|qinheng"

# Resultado esperado: /dev/ttyUSB0, /dev/ttyACM0, etc.
```

🍎 **macOS:**
```bash
# Listar puertos serie
ls /dev/cu.* | grep -E "(SLAB|wchusbserial)"

# Info sistema sobre USB
system_profiler SPUSBDataType | grep -A 10 -i "ESP32\|CP210x\|CH340"

# Resultado esperado: /dev/cu.SLAB_USBtoUART, etc.
```

#### **Paso 4.3: Flashear ESP32 con MicroPython**

🐧 **Linux/macOS:**
```bash
# Script automático (detecta puerto automáticamente)
./scripts/install_esp32.sh

# Script con puerto específico
./scripts/install_esp32.sh /dev/ttyUSB0

# Manual step-by-step
# 1. Instalar herramientas si es necesario
pip install esptool adafruit-ampy

# 2. Descargar firmware MicroPython
wget https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin

# 3. Limpiar flash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# 4. Flashear MicroPython
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

# 5. Subir archivos Python
ampy --port /dev/ttyUSB0 put esp32/main.py
ampy --port /dev/ttyUSB0 put esp32/config.py
ampy --port /dev/ttyUSB0 put esp32/sensor_server.py
ampy --port /dev/ttyUSB0 put esp32/boot.py

echo "✅ ESP32 configurado - listo para usar"
```

🪟 **Windows:**
```cmd
REM Script automático (usa COM3 por defecto)
scripts\install_esp32.bat

REM Script con puerto específico
scripts\install_esp32.bat COM5

REM Manual step-by-step
REM 1. Instalar herramientas
pip install esptool adafruit-ampy

REM 2. Descargar firmware (usar PowerShell o navegador)
powershell -Command "Invoke-WebRequest -Uri 'https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin' -OutFile 'esp32-20230426-v1.20.0.bin'"

REM 3. Limpiar flash
esptool.py --chip esp32 --port COM3 erase_flash

REM 4. Flashear MicroPython  
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin

REM 5. Subir archivos Python
ampy --port COM3 put esp32\main.py
ampy --port COM3 put esp32\config.py
ampy --port COM3 put esp32\sensor_server.py
ampy --port COM3 put esp32\boot.py

echo ✅ ESP32 configurado - listo para usar
```

### 5. Primera Ejecución ESP32

#### **Paso 5.1: Iniciar ESP32**

🐧 **Linux/macOS:**
```bash
# Monitor serie para ver output ESP32
screen /dev/ttyUSB0 115200

# En el REPL de MicroPython, ejecutar:
exec(open('main.py').read())
```

🪟 **Windows:**
```cmd
REM Opción A: PuTTY (recomendado)
REM Configurar: COM3, 115200 baud, Serial
REM Después de conectar, presionar Enter y ejecutar:
REM exec(open('main.py').read())

REM Opción B: Python miniterm
python -m serial.tools.miniterm COM3 115200
REM En REPL: exec(open('main.py').read())
```

#### **Paso 5.2: Verificar Conexión WiFi**

Deberías ver output similar a:
```
🔬 Iniciando Wally ESP32 Sensor Server...
📡 Conectando a TU_WIFI...
✅ WiFi conectado - IP: 192.168.1.100
🔧 Inicializando sensores...
  ✅ temperatura en pin 34
  ✅ fuerza en pin 35
  ✅ fotopuerta en pin 4
🌐 Servidor HTTP iniciado en 192.168.1.100:8080
📡 Endpoints disponibles:
   GET http://192.168.1.100:8080/sensors
   GET http://192.168.1.100:8080/vernier/command/t
✅ Sistema Wally iniciado correctamente
```

**⚠️ Importante:** Anotar la **IP mostrada** (ej: 192.168.1.100)

### 6. Configurar PC Controller

#### **Paso 6.1: Actualizar IP en PC Controller**

```bash
# Editar configuración PC
nano pc_controller/config.py  # Linux/macOS
notepad pc_controller/config.py  # Windows
```

**Modificar:**
```python
# pc_controller/config.py
ESP32_IP = "192.168.1.100"  # ← Usar IP del paso anterior
ESP32_PORT = 8080
SAMPLE_INTERVAL = 1.0       # segundos entre lecturas
```

#### **Paso 6.2: Test de Conectividad**

```bash
# Test ping
ping 192.168.1.100

# Test HTTP endpoint  
curl http://192.168.1.100:8080/ping
# Respuesta esperada: "pong"

# Test sensores Vernier
curl http://192.168.1.100:8080/vernier/status
# Respuesta: JSON con info de sensores
```

### 7. Ejecutar Sistema Completo

#### **Paso 7.1: Mantener ESP32 Ejecutándose**

El ESP32 debe seguir corriendo desde el Paso 5. Si se desconectó:

```bash
# Reconectar al ESP32
screen /dev/ttyUSB0 115200  # Linux/macOS
# python -m serial.tools.miniterm COM3 115200  # Windows

# Si no está ejecutando, ejecutar:
exec(open('main.py').read())
```

#### **Paso 7.2: Iniciar Aplicación PC**

🐧 **Linux/macOS:**
```bash
# Activar entorno virtual
source wally_env/bin/activate

# Ejecutar aplicación
cd pc_controller
python main.py
```

🪟 **Windows:**
```cmd
REM Activar entorno virtual
wally_env\Scripts\activate.bat

REM Ejecutar aplicación
cd pc_controller
python main.py
```

## 🧪 Testing y Verificación

### **Test 1: Conectividad Básica**
```bash
# Verificar estructura archivos
find . -name "*.py" | wc -l  # Debe mostrar ~10 archivos

# Test dependencias Python
python -c "import matplotlib, tkinter, requests; print('✅ Dependencias OK')"

# Test ESP32 HTTP
curl http://ESP32_IP:8080/ping
curl http://ESP32_IP:8080/status
```

### **Test 2: Comandos Arduino Migrados**
```bash
# Test comandos originales Arduino via HTTP
curl http://ESP32_IP:8080/vernier/command/t    # Cambiar a temperatura
curl http://ESP32_IP:8080/vernier/command/f    # Cambiar a fuerza
curl http://ESP32_IP:8080/vernier/command/p    # Cambiar a fotopuerta
curl http://ESP32_IP:8080/vernier/command/m    # Cambiar a movimiento
curl http://ESP32_IP:8080/vernier/command/d    # Pausar lecturas
curl http://ESP32_IP:8080/vernier/command/c    # Continuar lecturas
```

### **Test 3: Interfaz Completa**
1. **Aplicación PC** debería mostrar dashboard con:
   - 📊 **Sensores en tiempo real** con valores actualizándose
   - 📈 **Gráficos históricos** con plots en tiempo real
   - 🔬 **Panel Vernier** con botones para cambiar sensores
   - 🎛️ **Controles** start/stop/export

2. **Test funcionalidad:**
   - Click **🌡️ Temperatura** → Datos temperatura en gráfico
   - Click **⚡ Fuerza** → Cambio a sensor fuerza
   - Click **📥 Exportar CSV** → Descarga archivo datos
   - **Desconectar sensor físico** → Sistema mantiene datos previos
   - **Reconectar sensor** → Continuidad automática

### **Test 4: Comparación Arduino vs ESP32**

| **Función Arduino** | **Test ESP32** | **Resultado Esperado** |
|---------------------|----------------|------------------------|
| `Serial.println("t")` | Click botón 🌡️ Temperatura | Cambio a sensor temperatura |
| `Serial.println("f")` | Click botón ⚡ Fuerza | Cambio a sensor fuerza + LED control |
| `Serial.println("p")` | Click botón 📷 Fotopuerta | Detección estado puerta + LED |
| `Serial.println("m")` | Click botón 📐 Movimiento | Medición distancia ultrasonido |
| `Serial.println("d")` | Click botón ⏸️ Pausar | Lecturas pausadas |
| `Serial.println("c")` | Click botón ▶️ Continuar | Lecturas continuadas |

## 🔧 Troubleshooting Específico

### 🪟 **Windows - Problemas Comunes**

#### **Error: "Python no reconocido"**
```cmd
# Verificar instalación Python
python --version

# Si no funciona, agregar al PATH:
# Control Panel > System > Advanced > Environment Variables
# Path > Edit > New > C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python3X\
# Path > Edit > New > C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python3X\Scripts\
```

#### **Error: "Puerto COM no disponible"**
```cmd
# Verificar Device Manager
# Puertos (COM & LPT) - debe aparecer "Silicon Labs CP210x USB to UART Bridge"

# Si no aparece, instalar drivers:
# Descargar de: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
```

#### **Error: "Permission denied" en scripts**
```powershell
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar permisos
Get-ExecutionPolicy -List
```

#### **Error: "esptool not found"**
```cmd
# Reinstalar herramientas
pip uninstall esptool
pip install esptool

# Verificar instalación
esptool.py version
```

### 🐧 **Linux - Problemas Comunes**

#### **Error: "Permission denied" puerto USB**
```bash
# Solución permanente: agregar usuario al grupo dialout
sudo usermod -a -G dialout $USER
# Logout/login requerido

# Solución temporal
sudo chmod 666 /dev/ttyUSB0

# Verificar permisos
ls -l /dev/ttyUSB0
groups $USER
```

#### **Error: "ModuleNotFoundError: tkinter"**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-tkinter

# Fedora/CentOS/RHEL  
sudo dnf install tkinter
# sudo yum install tkinter  # versiones antiguas

# Arch Linux
sudo pacman -S tk
```

#### **Error: "Command not found: wget/curl"**
```bash
# Ubuntu/Debian
sudo apt install wget curl

# Usar alternativa si falta wget
curl -O https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin
```

#### **Error: "screen: command not found"**
```bash
# Ubuntu/Debian
sudo apt install screen

# Alternativa con miniterm
python -m serial.tools.miniterm /dev/ttyUSB0 115200
```

### 🍎 **macOS - Problemas Comunes**

#### **Error: "Developer Tools not installed"**
```bash
# Instalar Xcode Command Line Tools
xcode-select --install

# Verificar instalación
xcode-select -p
```

#### **Error: "Permission denied" puerto USB**
```bash
# Cambiar permisos temporalmente
sudo chmod 666 /dev/cu.SLAB_USBtoUART

# Listar puertos disponibles
ls /dev/cu.*
```

#### **Error: "brew command not found"**
```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Luego instalar Python
brew install python
```

### 🔬 **ESP32/Sensores - Problemas Específicos**

#### **Error: "WiFi no conecta"**
```python
# En REPL ESP32, debugging WiFi:
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Networks:", wlan.scan())  # Ver redes disponibles
print("Config:", wlan.ifconfig())  # Ver configuración actual

# Verificar credenciales en config.py
print("SSID configurado:", WIFI_SSID)
```

#### **Error: "Sensores no detectados"**
```python
# En REPL ESP32, test ADC manual:
import machine
adc = machine.ADC(machine.Pin(34))  # Pin temperatura
adc.atten(machine.ADC.ATTN_11DB)
print("ADC reading:", adc.read())  # Debe dar valor 0-4095

# Verificar conexiones físicas
# GPIO34/35 deben tener señal analógica 0-3.3V
```

#### **Error: "HTTP endpoints no responden"**
```bash
# Verificar que ESP32 esté ejecutando
curl -v http://ESP32_IP:8080/ping

# Si falla, verificar:
# 1. ESP32 ejecutando main.py
# 2. IP correcta en pc_controller/config.py
# 3. Firewall no bloquea puerto 8080
# 4. Misma red WiFi
```

## 📡 Configuración de Red Avanzada

### **Red WiFi Empresarial/Educativa**

Si tu red requiere autenticación especial:

```python
# esp32/config.py - Para redes WPA2-Enterprise
WIFI_SSID = "RED_UNIVERSIDAD"
WIFI_PASSWORD = "tu_password"
WIFI_USERNAME = "tu_usuario"  # Si usa WPA2-Enterprise

# Nota: MicroPython estándar no soporta WPA2-Enterprise
# Usar red huésped o hotspot móvil como alternativa
```

### **IP Estática (Opcional)**

Para IP fija en lugar de DHCP:

```python
# esp32/config.py - Agregar configuración IP estática
STATIC_IP = "192.168.1.200"
SUBNET_MASK = "255.255.255.0"
GATEWAY = "192.168.1.1"
DNS = "8.8.8.8"

# En main.py usar:
# wlan.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY, DNS))
```

### **Multiple Networks**

Para múltiples redes WiFi:

```python
# esp32/config.py - Múltiples redes
WIFI_NETWORKS = [
    {"ssid": "RED_CASA", "password": "password1"},
    {"ssid": "RED_LAB", "password": "password2"},
    {"ssid": "HOTSPOT", "password": "password3"}
]
```

## 📊 Logs y Debugging

### **Logs del Sistema**
```bash
# Ver logs en tiempo real
tail -f data/system.log

# Verificar puertos en uso
netstat -an | grep 8080
lsof -i :8080  # Linux/macOS

# Monitor tráfico red ESP32
tcpdump -i any host 192.168.1.100
```

### **Debugging ESP32**
```python
# En REPL ESP32 - Información de sistema
import gc, machine
print("Memory free:", gc.mem_free())
print("CPU freq:", machine.freq())
print("Reset cause:", machine.reset_cause())

# Debugging sensores específicos
import machine
adc_temp = machine.ADC(machine.Pin(34))
adc_temp.atten(machine.ADC.ATTN_11DB)
print("Temperature ADC:", adc_temp.read())
```

## 🚀 Quick Start Commands

### **🪟 Windows (Todo en uno):**
```cmd
git clone https://github.com/codeviloria/wally-daq-system.git
cd wally-daq-system
scripts\setup_environment.bat
REM Editar esp32\config.py con tu WiFi
scripts\install_esp32.bat COM3
REM En ESP32 REPL: exec(open('main.py').read())
cd pc_controller && python main.py
```

### **🐧 Linux (Todo en uno):**
```bash
git clone https://github.com/codeviloria/wally-daq-system.git
cd wally-daq-system
./scripts/setup_environment.sh
# Editar esp32/config.py con tu WiFi
./scripts/install_esp32.sh /dev/ttyUSB0
# En ESP32 REPL: exec(open('main.py').read())
cd pc_controller && python main.py
```

---

## 📞 Soporte Técnico

### **Autodiagnóstico:**
```bash
# Checklist completo del sistema
echo "=== Wally DAQ System - Diagnóstico ==="
python --version
python -c "import matplotlib, tkinter, requests; print('✅ Python OK')"
ping -c 1 192.168.1.100 && echo "✅ ESP32 reachable"
curl -s http://192.168.1.100:8080/ping && echo "✅ HTTP OK"
ls pc_controller/*.py | wc -l && echo "archivos Python"
```

### **Consultoría y Soporte Profesional:**

**Ingeniero Gino Viloria**
- 📧 **Email técnico:** codevilor.ia@gmail.com
- 🔗 **LinkedIn:** [linkedin.com/in/gino-viloria](https://linkedin.com/in/gino-viloria)
- 💻 **GitHub:** [github.com/codeviloria](https://github.com/codeviloria)

**Servicios disponibles:**
- ✅ Instalación remota y configuración
- ✅ Troubleshooting de hardware ESP32
- ✅ Calibración de sensores Vernier específicos
- ✅ Migración de sistemas Arduino legacy
- ✅ Customización para aplicaciones específicas

---

**✅ Al finalizar esta guía tendrás un sistema completamente funcional que migra tu código Arduino a ESP32 con interfaz gráfica profesional y conectividad WiFi, manteniendo 100% compatibilidad con tus sensores Vernier existentes.**