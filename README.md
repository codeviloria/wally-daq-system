# 🔬 Wally - Sistema de Adquisición de Datos ESP32 + Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MicroPython](https://img.shields.io/badge/MicroPython-ESP32-green.svg)](https://micropython.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Simulation](https://img.shields.io/badge/Simulation-Wokwi-orange.svg)](https://wokwi.com)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-red.svg)](https://arduino.cc)

Sistema híbrido de adquisición de datos para sensores Vernier que permite **cambio dinámico de sensores sin pérdida de datos**. Migrado desde Arduino a ESP32 con MicroPython manteniendo 100% compatibilidad de comandos.

## 🎮 **¡NUEVO! Simulación Completa Sin Hardware**

**🚀 Ahora puedes probar TODO el sistema sin ESP32 ni sensores físicos:**

| **Simulador** | **Tiempo Setup** | **Características** | **Enlace** |
|---------------|------------------|---------------------|------------|
| **🌟 Wokwi (Recomendado)** | 5 min | ESP32 + MicroPython nativo, WiFi, HTTP | [🎮 Simular Ahora](https://wokwi.com/projects/new/micropython-esp32) |
| **🛠️ Python Mock** | 2 min | Emulador local, desarrollo rápido | [📝 Ver Código](simulation/mock_server/) |
| **🐳 Docker** | 3 min | Entorno aislado, CI/CD ready | [🐳 Ver Setup](docs/simulation-guide.md#docker-environment) |

### **⚡ Quick Start Simulación:**
```bash
# Opción 1: Wokwi (Online, sin instalación)
1. Ir a: https://wokwi.com/projects/new/micropython-esp32
2. Copiar código de: docs/simulation-guide.md
3. ¡Listo! Sistema funcionando en 5 minutos

# Opción 2: Python Mock (Local)
git clone este-repo
python simulation/mock_server/mock_esp32_server.py
cd pc_controller && python main.py
```

### **📋 Documentación de Simulación:**
- 📖 [**Guía Completa de Simulación**](docs/simulation-guide.md) - Setup paso a paso
- 🧪 [**Testing y Validación**](docs/simulation-guide.md#testing-y-validación) - Scripts automáticos  
- 🔧 [**Troubleshooting**](docs/simulation-guide.md#troubleshooting) - Solución problemas
- 🎯 [**Casos de Uso**](docs/simulation-guide.md#casos-de-uso) - Educación, desarrollo, demos

---

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
ANTES (Arduino):                    DESPUÉS (ESP32 + Python + Simulación):
┌─────────────────┐                ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Arduino     │ Serial         │     ESP32       │ WiFi │   PC Python     │    │  🎮 Simulación   │
│   + VernierLib  │◄──────────────►│  MicroPython    │◄────►│  Tkinter UI     │    │    Wokwi/Mock   │
│   + 4 Sensores  │                │  + HTTP Server  │      │  + Dashboard    │    │   Sin Hardware  │
└─────────────────┘                └─────────────────┘      └─────────────────┘    └─────────────────┘
```

### **🔌 Mapeo de Puertos Arduino → ESP32**

| **Sensor** | **Arduino Pin** | **ESP32 GPIO** | **Simulación** | **Función** |
|------------|-----------------|----------------|----------------|-------------|
| 🌡️ **Temperatura** | A0 (Analog) | **GPIO 34** | Potenciómetro | ADC1_CH6 |
| ⚡ **Fuerza** | A1 (Analog) | **GPIO 35** | Potenciómetro | ADC1_CH7 |
| 📷 **Fotopuerta** | D2 (Digital) | **GPIO 4** | Botón azul | Input/Pull-up |
| 📐 **Movimiento** | D3 (Digital) | **GPIO 5/18** | Automático | Trigger/Echo |
| 💡 **LED Status** | D13 (Digital) | **GPIO 2** | LED virtual | LED Integrado |

## ⚡ Características

### **🆕 Nuevas Funcionalidades (vs Arduino):**
- ✅ **🎮 Simulación completa** - Probar sin hardware con Wokwi/Mock
- ✅ **WiFi Integration** - Control remoto via HTTP
- ✅ **Interfaz gráfica profesional** con Tkinter
- ✅ **Gráficos en tiempo real** con matplotlib
- ✅ **Export CSV automático** con timestamps
- ✅ **Buffer circular inteligente** - sin pérdida de memoria
- ✅ **Threading** para UI responsive
- ✅ **Hot-swapping** de sensores sin reinicio

### **✅ Funcionalidad Arduino Preservada:**
- ✅ **Comandos idénticos** (`t`, `f`, `p`, `m`, `d`, `c`)
- ✅ **Calibraciones Vernier** específicas por sensor
- ✅ **Control LED** con threshold (sensor fuerza)
- ✅ **Timing preciso** fotopuerta y ultrasonido
- ✅ **VernierLib equivalence** - autoID simulation
- ✅ **Formato de salida** compatible

## 🚀 Quick Start

### **🎯 Elige tu Opción:**

#### **🎮 Opción 1: Simulación (SIN HARDWARE) - 5 minutos**
**✅ Ideal para:** Aprendizaje, demos, desarrollo inicial
```bash
# Setup más rápido - Solo navegador
1. Ir a: https://wokwi.com/projects/new/micropython-esp32
2. Seguir: docs/simulation-guide.md
3. ¡Sistema completo funcionando!
```

#### **🔧 Opción 2: Hardware Real - 15 minutos**
**✅ Ideal para:** Implementación final, producción
```bash
# Setup tradicional con ESP32 físico
1. git clone https://github.com/codeviloria/wally-daq-system.git
2. scripts/setup_environment.sh  # o .bat en Windows
3. Configurar WiFi en esp32/config.py
4. scripts/install_esp32.sh /dev/ttyUSB0
5. cd pc_controller && python main.py
```

#### **🛠️ Opción 3: Desarrollo Híbrido - 10 minutos**
**✅ Ideal para:** Desarrollo profesional, testing
```bash
# Simulación + desarrollo
git clone https://github.com/codeviloria/wally-daq-system.git
python simulation/mock_server/mock_esp32_server.py &
cd pc_controller && python main.py
```

## 📁 **Estructura del Repositorio**

```
wally-daq-system/
├── 📋 README.md                                  # → Este archivo - Documentación principal
├── 📄 requirements.txt                           # → Dependencias Python para PC
├── 🎮 **simulation/**                            # → **NUEVO: Simulación sin hardware**
│   ├── 🌟 **wokwi/**                            # → Código para simulador Wokwi
│   │   ├── main.py                              # → ESP32 MicroPython para Wokwi
│   │   └── diagram.json                         # → Configuración componentes virtuales
│   ├── 🛠️ **mock_server/**                     # → Emulador Python local
│   │   └── mock_esp32_server.py                 # → Servidor mock completo
│   └── 🧪 **testing/**                         # → Scripts de testing automático
│       ├── test_simulation.py                   # → Suite de validación
│       ├── monitor_simulation.py                # → Monitor tiempo real
│       └── diagnose_system.py                   # → Diagnóstico automático
├── 📚 **docs/**                                 # → Documentación técnica y guías
│   ├── 📖 **simulation-guide.md**               # → **NUEVO: Guía completa simulación**
│   ├── installation.md                          # → Guía instalación hardware real
│   └── student-setup-guide.md                   # → Guía específica para estudiantes
├── 🔧 **esp32/**                                # → Código MicroPython para ESP32 real
│   ├── main.py                                  # → Programa principal ESP32
│   ├── config.py                                # → Configuración WiFi, pines, calibraciones
│   ├── sensor_server.py                         # → Servidor HTTP + sensores Vernier
│   └── boot.py                                  # → Secuencia de arranque automático
├── 🖥️ **pc_controller/**                        # → Aplicación cliente Python/Tkinter
│   ├── main.py                                  # → Controlador principal y punto de entrada
│   ├── config.py                                # → Configuración cliente PC (IP, puertos)
│   ├── ui_dashboard.py                          # → Interfaz gráfica con gráficos tiempo real
│   ├── data_manager.py                          # → Gestión datos, buffer circular, export CSV
│   └── esp32_client.py                          # → Cliente HTTP para comunicación ESP32
└── 🔨 **scripts/**                              # → Scripts de instalación y configuración
    ├── setup_environment.sh/.bat                # → Setup completo del entorno
    └── install_esp32.sh/.bat                    # → Flash ESP32 automáticamente
```

## 🧪 Testing y Validación

### **🎯 Testing Automático**
```bash
# Test simulación completa
python simulation/testing/test_simulation.py

# Monitor datos en tiempo real
python simulation/testing/monitor_simulation.py

# Diagnóstico del sistema
python simulation/testing/diagnose_system.py
```

### **📊 Comandos Arduino Verificados**
```bash
# Test compatibilidad Arduino 100%
curl http://localhost:8080/vernier/command/t    # ✅ Temperatura
curl http://localhost:8080/vernier/command/f    # ✅ Fuerza  
curl http://localhost:8080/vernier/command/p    # ✅ Fotopuerta
curl http://localhost:8080/vernier/command/m    # ✅ Movimiento
curl http://localhost:8080/vernier/command/d    # ✅ Pausar
curl http://localhost:8080/vernier/command/c    # ✅ Continuar
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

## 🔧 Hardware Setup

### **Conexiones ESP32 ↔ Vernier Shield**

```
Vernier Shield    →    ESP32 DevKit v1    →    🎮 Simulación Wokwi
═══════════════════════════════════════════════════════════════════
ANALOG 1 (A0)     →    GPIO 34           →    Potenciómetro 1 (Verde)
ANALOG 2 (A1)     →    GPIO 35           →    Potenciómetro 2 (Azul)  
DIGITAL 1 (D2)    →    GPIO 4            →    Botón Azul (Fotopuerta)
DIGITAL 2 (D3)    →    GPIO 5            →    Automático (Ultrasonido)
LED Status (D13)  →    GPIO 2            →    LED Virtual (Rojo)
VCC (5V)          →    VIN               →    Alimentación simulada
GND               →    GND               →    Tierra simulada
```

### **Sensores Compatibles:**
- **🌡️ Temperatura**: TMP36, Stainless Steel Temperature Probe
- **⚡ Fuerza**: Dual-Range Force Sensor (±10N, ±50N)
- **📷 Fotopuerta**: Photogate Head, Light Gate
- **📐 Movimiento**: Motion Detector, HC-SR04 Ultrasonico

## 📋 Configuración

### **ESP32 (esp32/config.py):**
```python
# WiFi - EDITAR OBLIGATORIO (Hardware real)
WIFI_SSID = "TU_WIFI"
WIFI_PASSWORD = "TU_PASSWORD" 

# Para simulación Wokwi usar:
# WIFI_SSID = "Wokwi-GUEST"  
# WIFI_PASSWORD = ""
```

### **PC (pc_controller/config.py):**
```python
# Hardware real
ESP32_IP = "192.168.1.100"  # IP del ESP32 físico
ESP32_PORT = 8080

# Simulación Wokwi + Gateway
ESP32_IP = "localhost"       # Usar con Wokwi IoT Gateway
ESP32_PORT = 9080           # Puerto del gateway

# Simulación Mock local
ESP32_IP = "localhost"       # Emulador Python local
ESP32_PORT = 8080           # Puerto directo
```

## 🎯 Casos de Uso

### **🎓 Educación:**
- **Laboratorios remotos** - Estudiantes practican desde casa
- **Migración Arduino→ESP32** - Ejemplo práctico completo  
- **IoT y conectividad** - WiFi, HTTP, APIs REST
- **🎮 Sin hardware requerido** - Simulación Wokwi

### **👨‍💻 Desarrollo:**
- **Prototipado rápido** - Testing sin esperar hardware
- **CI/CD integration** - Testing automatizado en pipeline
- **Desarrollo distribuido** - Equipos remotos sin hardware
- **🧪 Validación completa** - Antes de implementación real

### **🏢 Industria:**
- **Proof of Concept** - Demos sin inversión hardware
- **Training y certificación** - Personal sin equipos físicos
- **Testing de integración** - Validar APIs y protocolos
- **📊 Análisis de datos** - Simular años de datos en minutos

## 🛠️ Desarrollo y Testing

```bash
# 🎮 Desarrollo con simulación (recomendado)
python simulation/mock_server/mock_esp32_server.py
cd pc_controller && python main.py

# 🧪 Testing unitario
python simulation/testing/test_simulation.py

# 📊 Monitor tiempo real  
python simulation/testing/monitor_simulation.py

# 🔧 Debugging ESP32 real
screen /dev/ttyUSB0 115200          # Monitor serie
curl http://ESP32_IP:8080/ping      # Test HTTP
```

## 🎓 **Getting Started por Perfil**

### **👨‍🎓 Estudiantes - "Quiero aprender"**
```
🎯 Objetivo: Entender el sistema sin gastar dinero
📖 Ruta: docs/simulation-guide.md → Wokwi setup → Cliente Python
⏱️ Tiempo: 15 minutos
💰 Costo: $0 (gratis)
```

### **👨‍💻 Desarrolladores - "Quiero implementar"**
```  
🎯 Objetivo: Adaptar para mi proyecto específico
📖 Ruta: Simulación → Hardware real → Personalización
⏱️ Tiempo: 1-2 horas setup + desarrollo
💰 Costo: ~$20 ESP32 + sensores
```

### **🏢 Empresas - "Quiero evaluar"**
```
🎯 Objetivo: Validar para uso industrial
📖 Ruta: Simulación → POC → Piloto → Producción  
⏱️ Tiempo: 1 semana evaluación
💰 Costo: Consultoría disponible
```

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. **Probar en simulación**: Usar Wokwi o Mock antes de hardware
4. Commit: `git commit -m 'Agregar nueva funcionalidad'`
5. Push: `git push origin feature/nueva-funcionalidad`  
6. Pull Request

### **🧪 Testing requerido para PRs:**
```bash
# Validar que simulación funciona
python simulation/testing/test_simulation.py

# Verificar compatibilidad Arduino
curl tests para todos los comandos t,f,p,m,d,c

# Test cliente Python conecta OK
cd pc_controller && python main.py
```

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles

## 💼 Servicios de Consultoría

### **Ingeniero Gino Viloria - Especialista en Sistemas DAQ**

**🔧 Servicios Disponibles:**
- ✅ **🎮 Setup simulación personalizada** - Wokwi/Mock para casos específicos
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

---

## 🏆 **¿Por qué Wally DAQ System?**

### **Antes vs Ahora:**

| **Aspecto** | **Arduino Tradicional** | **🔬 Wally DAQ + Simulación** |
|-------------|-------------------------|-------------------------------|
| **Setup Time** | 2-3 horas (hardware) | **5 minutos (simulación)** |
| **Costo inicial** | $100+ ESP32+sensores | **$0 (Wokwi gratis)** |
| **Debugging** | ❌ Serial Monitor básico | **✅ Dashboard profesional + logs** |
| **Conectividad** | ❌ Solo cable serie | **✅ WiFi + HTTP + APIs** |
| **Colaboración** | ❌ Hardware físico requerido | **✅ Compartir link simulación** |
| **Enseñanza** | ❌ Requiere laboratorio | **✅ Estudiantes desde casa** |
| **Escalabilidad** | ❌ Un ESP32 = un estudiante | **✅ Infinitos usuarios simultáneos** |
| **Testing** | ❌ Manual y lento | **✅ Automatizado con scripts** |

### **🎯 Resultado:**
**Mismo aprendizaje y funcionalidad, pero más rápido, barato y escalable.**

---

**🚀 ¡Comienza ahora con simulación en 5 minutos!** → [docs/simulation-guide.md](docs/simulation-guide.md)

**🏆 Proyecto Destacado:** Migración completa Arduino → ESP32 manteniendo 100% compatibilidad de comandos mientras se agrega conectividad WiFi, interfaz gráfica profesional, capacidades IoT modernas **y simulación completa sin hardware**.

**Desarrollado para proyectos académicos y aplicaciones industriales**  
**© 2025 Ingeniero Gino Viloria - Consultoría en Sistemas DAQ**