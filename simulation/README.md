# 🎮 Simulación Wally DAQ System

Este directorio contiene todos los archivos necesarios para simular el sistema Wally DAQ sin hardware físico.

## 📁 Estructura

```
simulation/
├── 🌟 wokwi/                    # Simulación online Wokwi
│   ├── main.py                  # Código ESP32 para Wokwi
│   └── diagram.json             # Configuración componentes virtuales
├── 🛠️ mock_server/              # Emulador Python local
│   └── mock_esp32_server.py     # Servidor mock completo
└── 🧪 testing/                  # Scripts de testing
    ├── test_simulation.py       # Suite de validación
    └── diagnose_system.py       # Diagnóstico automático
```

## 🚀 Quick Start

### 🌟 Opción 1: Wokwi (Online)
```bash
1. Ir a: https://wokwi.com/projects/new/micropython-esp32
2. Copiar contenido de: wokwi/main.py
3. Copiar contenido de: wokwi/diagram.json
4. Iniciar simulación
```

### 🛠️ Opción 2: Mock Server (Local)
```bash
# Ejecutar emulador
python simulation/mock_server/mock_esp32_server.py

# En otra terminal: ejecutar cliente
cd pc_controller
python main.py
```

## 🧪 Testing

```bash
# Test automático
python simulation/testing/test_simulation.py

# Diagnóstico
python simulation/testing/diagnose_system.py
```

## 📚 Documentación Completa

Ver: [docs/simulation-guide.md](../docs/simulation-guide.md)
