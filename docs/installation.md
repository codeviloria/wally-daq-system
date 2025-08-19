## 📁 docs/

### 📄 docs/installation.md
```markdown
# 📥 Instalación Wally DAQ System

## Prerrequisitos

### Hardware
- ESP32 DevKit v1
- Sensores Vernier (temperatura, pH, movimiento, presión)  
- Cables jumper
- PC con Python 3.8+ (Windows 10+, Linux, macOS)

### Software

#### 🪟 Windows:
- Python 3.8+ (desde Microsoft Store o python.org)
- Git for Windows
- Drivers USB ESP32 (CP210x o CH340)
- Terminal: PowerShell, CMD, o Windows Terminal

#### 🐧 Linux:
- Python 3.8+ (`sudo apt install python3 python3-pip`)
- Git (`sudo apt install git`)
- Drivers USB automáticos
- Terminal integrado

#### 🍎 macOS:
- Python 3.8+ (Homebrew: `brew install python`)
- Git (Xcode Command Line Tools)
- Drivers USB automáticos
- Terminal integrado

## Instalación Multiplataforma

### 1. Clonar Repositorio
```bash
git clone https://github.com/gino-viloria/wally-daq-system.git
cd wally-daq-system
```

### 2. Crear Estructura de Archivos

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
# Crear todos los archivos vacíos
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

#### 🪟 Windows CMD:
```cmd
REM Crear archivos principales
type nul > README.md & type nul > requirements.txt & type nul > .gitignore & type nul > LICENSE

REM Crear archivos ESP32
type nul > esp32\main.py & type nul > esp32\config.py & type nul > esp32\sensor_server.py & type nul > esp32\boot.py

REM Crear archivos PC Controller
type nul > pc_controller\main.py & type nul > pc_controller\config.py & type nul > pc_controller\ui_dashboard.py & type nul > pc_controller\data_manager.py & type nul > pc_controller\esp32_client.py & type nul > pc_controller\utils.py

REM Crear scripts
type nul > scripts\setup_environment.sh & type nul > scripts\install_esp32.sh & type nul > scripts\setup_environment.bat & type nul > scripts\install_esp32.bat

REM Crear documentación
type nul > docs\installation.md & type nul > data\.gitkeep
```

### 3. Setup Entorno Python

#### 🐧 Linux/macOS:
```bash
# Automático
./scripts/setup_environment.sh

# Manual
python3 -m venv wally_env
source wally_env/bin/activate
pip install -r requirements.txt
```

#### 🪟 Windows:
```cmd
REM Automático
scripts\setup_environment.bat

REM Manual
python -m venv wally_env
wally_env\Scripts\activate.bat
pip install -r requirements.txt
```

### 4. Configurar ESP32

#### Editar configuración WiFi (IMPORTANTE):
```python
# Archivo: esp32/config.py
WIFI_SSID = "TU_WIFI_AQUI"          # ← CAMBIAR
WIFI_PASSWORD = "TU_PASSWORD_AQUI"  # ← CAMBIAR
```

#### Flashear ESP32:

🐧 **Linux/macOS:**
```bash
# Automático (detecta puerto USB automáticamente)
./scripts/install_esp32.sh

# Manual con puerto específico
./scripts/install_esp32.sh /dev/ttyUSB0
```

🪟 **Windows:**
```cmd
REM Automático (usa COM3 por defecto)
scripts\install_esp32.bat

REM Manual con puerto específico
scripts\install_esp32.bat COM5
```

### 5. Identificar Puerto COM/USB

#### 🪟 Windows:
```cmd
# Ver puertos disponibles
mode | findstr "COM"

# O usar Python
python -c "import serial.tools.list_ports; [print(p.device, p.description) for p in serial.tools.list_ports.comports()]"
```

#### 🐧 Linux:
```bash
# Ver puertos USB
ls /dev/ttyUSB* /dev/ttyACM*

# Con información detallada
dmesg | grep tty
```

#### 🍎 macOS:
```bash
# Ver puertos disponibles
ls /dev/cu.*

# Información detallada
system_profiler SPUSBDataType | grep -A 10 "ESP32"
```

### 6. Ejecutar Sistema

#### 🐧 Linux/macOS:
```bash
# Terminal 1: Monitor ESP32
screen /dev/ttyUSB0 115200
# En REPL: exec(open('main.py').read())

# Terminal 2: Aplicación PC
cd pc_controller
python main.py
```

#### 🪟 Windows:
```cmd
REM Terminal 1: Monitor ESP32
REM Opción A: PuTTY (recomendado)
REM Configurar: COM3, 115200, Serial

REM Opción B: Python miniterm
python -m serial.tools.miniterm COM3 115200
REM En REPL: exec(open('main.py').read())

REM Terminal 2: Aplicación PC
cd pc_controller
python main.py
```

## Troubleshooting por OS

### 🪟 Windows

#### Error: "Python no reconocido"
```cmd
# Agregar Python al PATH
# Control Panel > System > Advanced > Environment Variables
# Agregar: C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python3X\
```

#### Error: "Puerto COM no disponible"
```cmd
# Verificar Device Manager
# Puertos (COM & LPT)
# Reinstalar drivers ESP32
```

#### Error: "Permission denied" en scripts
```powershell
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 🐧 Linux

#### Error: "Permission denied" puerto USB
```bash
# Agregar usuario al grupo dialout
sudo usermod -a -G dialout $USER
# Logout/login requerido

# O dar permisos temporales
sudo chmod 666 /dev/ttyUSB0
```

#### Error: "ModuleNotFoundError tkinter"
```bash
# Ubuntu/Debian
sudo apt install python3-tkinter

# Fedora/CentOS
sudo dnf install tkinter
```

#### Error: "Command not found: wget"
```bash
# Ubuntu/Debian
sudo apt install wget

# Usar curl como alternativa
curl -O https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin
```

### 🍎 macOS

#### Error: "Developer Tools not installed"
```bash
# Instalar Xcode Command Line Tools
xcode-select --install
```

#### Error: "Permission denied" puerto USB
```bash
# Cambiar permisos temporalmente
sudo chmod 666 /dev/cu.usbserial-*
```

## Configuración de Red

### 1. Verificar Conexión WiFi ESP32
```python
# En REPL del ESP32, verificar IP:
import network
wlan = network.WLAN(network.STA_IF)
print("IP:", wlan.ifconfig()[0] if wlan.isconnected() else "No conectado")
```

### 2. Actualizar IP en PC Controller
```python
# Archivo: pc_controller/config.py
ESP32_IP = "192.168.1.100"  # ← Usar IP del paso anterior
```

### 3. Test de Conectividad

#### 🪟 Windows:
```cmd
ping 192.168.1.100
```

#### 🐧 Linux/macOS:
```bash
ping -c 4 192.168.1.100
```

## Verificación de Instalación

### Test Rápido
```bash
# 1. Verificar estructura
find . -name "*.py" | wc -l  # Debe mostrar ~10 archivos

# 2. Test Python
python -c "import matplotlib, tkinter, requests; print('✅ Dependencias OK')"

# 3. Test ESP32 (si está conectado)
curl http://192.168.1.100:8080/ping
```

### Logs y Debugging
```bash
# Ver logs del sistema
tail -f data/system.log

# Verificar puertos en uso
netstat -an | grep 8080

# Monitor de red ESP32
tcpdump -i any host 192.168.1.100
```

---

## 🚀 Quick Commands por OS

### 🪟 Windows (Todo en uno):
```cmd
git clone https://github.com/gino-viloria/wally-daq-system.git
cd wally-daq-system
scripts\setup_environment.bat
REM Editar esp32\config.py con tu WiFi
scripts\install_esp32.bat COM3
cd pc_controller && python main.py
```

### 🐧 Linux (Todo en uno):
```bash
git clone https://github.com/gino-viloria/wally-daq-system.git
cd wally-daq-system
./scripts/setup_environment.sh
# Editar esp32/config.py con tu WiFi
./scripts/install_esp32.sh /dev/ttyUSB0
cd pc_controller && python main.py
```

---
**💼 Consultoría:** Para soporte profesional contactar Ingeniero Gino Viloria
```

