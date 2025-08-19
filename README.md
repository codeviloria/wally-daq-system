# 🔬 Wally - Sistema de Adquisición de Datos ESP32 + Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MicroPython](https://img.shields.io/badge/MicroPython-ESP32-green.svg)](https://micropython.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Windows%20%7C%20Linux%20%7C%20macOS-brightgreen.svg)](https://github.com)

Sistema híbrido de adquisición de datos para sensores Vernier que permite **cambio dinámico de sensores sin pérdida de datos**. Utiliza ESP32 como servidor de sensores y Python/Tkinter para interfaz profesional.

## 👨‍💻 Consultoría y Desarrollo
**Desarrollado por:** [Ingeniero Gino Viloria](mailto:codevilor.ia@gmail.com)  
**Especialización:** Sistemas IoT, Adquisición de Datos, Python & MicroPython  
**Consultoría disponible:** Implementación, customización y soporte técnico

📧 **Contacto profesional:** codevilor.ia@gmail.com  
🔗 **LinkedIn:** [linkedin.com/in/gino-viloria](https://linkedin.com/in/gino-viloria)  
💼 **Servicios:** Desarrollo de prototipos, integración de sensores, sistemas DAQ personalizados

## 🏗️ Arquitectura
```
ESP32 (MicroPython) ←→ Python Controller ←→ Tkinter UI
     │                        │                  │
   Sensores              Data Manager       Dashboard
   Vernier               Buffer Logic       Real-time Charts
```

## ⚡ Características
- ✅ **Cambio dinámico** de sensores sin reinicio
- ✅ **Interfaz profesional** con Tkinter nativo
- ✅ **Gráficos en tiempo real** con matplotlib
- ✅ **Export CSV** con timestamps
- ✅ **Reconexión automática** WiFi/HTTP
- ✅ **Buffer circular** para gestión de memoria
- ✅ **Threading** para UI responsive

## 🚀 Quick Start

### 1. Clonar repositorio
```bash
git clone https://github.com/tu-usuario/wally-daq-system.git
cd wally-daq-system
```

### 2. Crear estructura de archivos

#### 🐧 Linux/macOS:
```bash
# Crear todos los archivos vacíos
touch README.md requirements.txt .gitignore LICENSE \
esp32/main.py esp32/config.py esp32/sensor_server.py esp32/boot.py \
pc_controller/main.py pc_controller/config.py pc_controller/ui_dashboard.py pc_controller/data_manager.py pc_controller/esp32_client.py pc_controller/utils.py \
scripts/setup_environment.sh scripts/install_esp32.sh \
docs/installation.md data/.gitkeep

# Hacer ejecutables los scripts
chmod +x scripts/setup_environment.sh scripts/install_esp32.sh
```

#### 🪟 Windows (PowerShell):
```powershell
# Crear todos los archivos vacíos
New-Item -ItemType File -Path @(
    "README.md", "requirements.txt", ".gitignore", "LICENSE",
    "esp32/main.py", "esp32/config.py", "esp32/sensor_server.py", "esp32/boot.py",
    "pc_controller/main.py", "pc_controller/config.py", "pc_controller/ui_dashboard.py", 
    "pc_controller/data_manager.py", "pc_controller/esp32_client.py", "pc_controller/utils.py",
    "scripts/setup_environment.bat", "scripts/install_esp32.bat",
    "docs/installation.md", "data/.gitkeep"
) -Force
```

#### 🪟 Windows (CMD):
```cmd
REM Crear archivos principales
type nul > README.md
type nul > requirements.txt
type nul > .gitignore
type nul > LICENSE

REM Crear archivos ESP32
type nul > esp32\main.py
type nul > esp32\config.py
type nul > esp32\sensor_server.py
type nul > esp32\boot.py

REM Crear archivos PC Controller
type nul > pc_controller\main.py
type nul > pc_controller\config.py
type nul > pc_controller\ui_dashboard.py
type nul > pc_controller\data_manager.py
type nul > pc_controller\esp32_client.py
type nul > pc_controller\utils.py

REM Crear scripts
type nul > scripts\setup_environment.bat
type nul > scripts\install_esp32.bat

REM Crear documentación
type nul > docs\installation.md
type nul > data\.gitkeep
```

### 3. Setup Python

#### 🐧 Linux/macOS:
```bash
# Ejecutar script automático
./scripts/setup_environment.sh

# O manual:
python3 -m venv wally_env
source wally_env/bin/activate
pip install -r requirements.txt
```

#### 🪟 Windows:
```cmd
REM Ejecutar script automático
scripts\setup_environment.bat

REM O manual:
python -m venv wally_env
wally_env\Scripts\activate
pip install -r requirements.txt
```

### 4. Configurar ESP32

#### Editar configuración WiFi:
```python
# Editar esp32/config.py
WIFI_SSID = "TU_WIFI_AQUI"
WIFI_PASSWORD = "TU_PASSWORD_AQUI"
```

#### Flashear ESP32:

🐧 **Linux/macOS:**
```bash
# Script automático
./scripts/install_esp32.sh /dev/ttyUSB0

# O manual:
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

REM O manual:
esptool.py --chip esp32 --port COM3 erase_flash
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
ampy --port COM3 put esp32/main.py
ampy --port COM3 put esp32/config.py
ampy --port COM3 put esp32/sensor_server.py
ampy --port COM3 put esp32/boot.py
```

### 5. Ejecutar sistema

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
REM Terminal 1: ESP32 (usar PuTTY, Tera Term, o Python)
python -m serial.tools.miniterm COM3 115200
REM En REPL: exec(open('main.py').read())

REM Terminal 2: Aplicación Python
cd pc_controller
python main.py
```

## 🔧 Hardware Setup
- **ESP32 DevKit v1**
- **Sensores Vernier**: Temperatura (Pin 34), pH (Pin 35), Movimiento (Pin 32), Presión (Pin 33)
- **WiFi**: Misma red que PC controller

## 📊 Demo
1. Conectar sensores → Ver datos en tiempo real
2. Desconectar sensor → Datos previos preservados
3. Reconectar sensor → Continuidad automática
4. Export CSV → Descarga con timestamps

## 🛠️ Desarrollo
```bash
# Modo desarrollo
cd pc_controller
python main.py

# Tests
python -m pytest tests/

# Scripts de utilidad
./scripts/setup_environment.sh
./scripts/install_esp32.sh
```

## 📋 Configuración

### ESP32 (esp32/config.py)
```python
WIFI_SSID = "TU_WIFI"
WIFI_PASSWORD = "TU_PASSWORD"
```

### PC (pc_controller/config.py)
```python
ESP32_IP = "192.168.1.100"  # IP del ESP32
SAMPLE_INTERVAL = 1.0       # segundos entre lecturas
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
- **Laboratorios educativos** - Experimentos con múltiples sensores
- **Investigación** - Adquisición de datos continua
- **Prototipos IoT** - Base para sistemas de monitoreo
- **Aprendizaje** - Ejemplo de arquitectura híbrida

## 💼 Servicios de Consultoría

### Ingeniero Gino Viloria - Especialista en Sistemas DAQ
**🔧 Servicios Disponibles:**
- ✅ **Implementación personalizada** de sistemas de adquisición de datos
- ✅ **Integración de sensores** específicos y calibración avanzada
- ✅ **Optimización de performance** para aplicaciones industriales
- ✅ **Desarrollo de interfaces** web y desktop personalizadas
- ✅ **Soporte técnico** y mantenimiento de sistemas DAQ
- ✅ **Capacitación** en Python, MicroPython y ESP32

**📞 Contacto Profesional:**
- 📧 Email: codevilor.ia@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/gino-viloria]()
- 💻 GitHub: [github.com/codeviloria](https://github.com/codeviloria)


**🎓 Especialización:**
- Sistemas IoT y automatización industrial
- Adquisición de datos en tiempo real
- Python/MicroPython para sistemas embebidos
- Arquitecturas híbridas ESP32 + PC
- Sensores científicos e industriales

---

**Desarrollado para proyectos académicos y aplicaciones industriales**  
**© 2025  Gino Viloria - Consultoría en Sistemas DAQ**
```

