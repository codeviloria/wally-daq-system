"""
Wally Data Acquisition System - Main Controller
Sistema principal de adquisición de datos con interfaz Tkinter
"""
import tkinter as tk
from tkinter import messagebox
import threading
import time
import sys
import os

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui_dashboard import WallyDashboard
from data_manager import DataManager
from esp32_client import ESP32Client
import config

class WallyController:
    """Controlador principal del sistema Wally"""
    
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Inicializar componentes
        self.data_manager = DataManager()
        self.esp32_client = ESP32Client()
        self.dashboard = WallyDashboard(self.root, self)
        
        # Estado del sistema
        self.is_running = False
        self.current_data = {}
        self.connection_status = "disconnected"
        
        # Threading
        self.data_thread = None
        self.stop_event = threading.Event()
        
        print("🔬 Wally Controller inicializado")
    
    def start_acquisition(self):
        """Iniciar proceso de adquisición de datos"""
        if self.is_running:
            messagebox.showwarning("Advertencia", "El sistema ya está ejecutándose")
            return
        
        # Intentar conectar al ESP32
        self.dashboard.update_status("🔄 Conectando...")
        
        if self.esp32_client.connect(config.ESP32_IP, config.ESP32_PORT):
            self.is_running = True
            self.stop_event.clear()
            
            # Iniciar thread de adquisición
            self.data_thread = threading.Thread(target=self.data_acquisition_loop, daemon=True)
            self.data_thread.start()
            
            # Actualizar UI
            self.dashboard.update_status("🟢 Adquisición activa")
            self.dashboard.set_controls_state("running")
            
            messagebox.showinfo("Éxito", f"Conectado a ESP32: {config.ESP32_IP}")
            print(f"✅ Adquisición iniciada - ESP32: {config.ESP32_IP}")
            
        else:
            self.dashboard.update_status("🔴 Error de conexión")
            messagebox.showerror("Error", 
                f"No se pudo conectar al ESP32 en {config.ESP32_IP}:{config.ESP32_PORT}\n\n"
                "Verificar:\n"
                "• ESP32 encendido y conectado a WiFi\n"
                "• IP correcta en config.py\n"
                "• Mismo network que el PC")
    
    def stop_acquisition(self):
        """Detener adquisición de datos"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.stop_event.set()
        
        # Esperar que termine el thread
        if self.data_thread and self.data_thread.is_alive():
            self.data_thread.join(timeout=2)
        
        # Actualizar UI
        self.dashboard.update_status("🔴 Detenido")
        self.dashboard.set_controls_state("stopped")
        
        print("🛑 Adquisición detenida")
    
    def data_acquisition_loop(self):
        """Bucle principal de adquisición de datos (ejecuta en thread separado)"""
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.is_running and not self.stop_event.is_set():
            try:
                # Obtener datos del ESP32
                data = self.esp32_client.get_sensor_data()
                
                if data:
                    # Datos recibidos correctamente
                    consecutive_errors = 0
                    self.current_data = data
                    
                    # Guardar en buffer
                    self.data_manager.add_reading(data)
                    
                    # Actualizar UI de forma thread-safe
                    self.root.after(0, self.update_ui_callback, data)
                    
                    # Log cada 10 lecturas
                    if self.data_manager.get_reading_count() % 10 == 0:
                        sensor_count = data.get('sensor_count', 0)
                        print(f"📊 Datos: {self.data_manager.get_reading_count()} | Sensores activos: {sensor_count}")
                        
                else:
                    # Error obteniendo datos
                    consecutive_errors += 1
                    print(f"⚠️ Error obteniendo datos ({consecutive_errors}/{max_consecutive_errors})")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        # Demasiados errores consecutivos - detener
                        self.root.after(0, self.handle_connection_lost)
                        break
                
                # Esperar antes de la siguiente lectura
                self.stop_event.wait(config.SAMPLE_INTERVAL)
                
            except Exception as e:
                consecutive_errors += 1
                print(f"❌ Error en data_acquisition_loop: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.root.after(0, self.handle_connection_lost)
                    break
                
                self.stop_event.wait(1)  # Esperar 1 segundo antes de reintentar
    
    def update_ui_callback(self, data):
        """Callback para actualizar UI desde el thread principal"""
        self.dashboard.update_sensors(data.get('readings', {}))
        self.dashboard.update_chart(data)
        self.dashboard.update_stats(self.data_manager.get_stats())
    
    def handle_connection_lost(self):
        """Manejar pérdida de conexión con ESP32"""
        self.stop_acquisition()
        self.dashboard.update_status("🔴 Conexión perdida")
        
        messagebox.showerror("Conexión Perdida", 
            "Se perdió la conexión con el ESP32.\n\n"
            "Verificar:\n"
            "• ESP32 sigue encendido\n"
            "• Conexión WiFi estable\n"
            "• No hay interferencias de red")
    
    def export_data(self):
        """Exportar datos a archivo CSV"""
        try:
            filename = self.dashboard.get_export_filename()
            if filename:
                if self.data_manager.export_to_csv(filename):
                    count = self.data_manager.get_reading_count()
                    messagebox.showinfo("Éxito", 
                        f"Datos exportados exitosamente:\n"
                        f"Archivo: {filename}\n"
                        f"Registros: {count}")
                    print(f"📁 Datos exportados: {filename}")
                else:
                    messagebox.showerror("Error", "Error exportando datos")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error en exportación: {str(e)}")
    
    def get_current_data(self):
        """Obtener datos actuales del sistema"""
        return self.current_data
    
    def get_data_manager(self):
        """Obtener instancia del data manager"""
        return self.data_manager
    
    def on_closing(self):
        """Manejar cierre de aplicación"""
        if self.is_running:
            result = messagebox.askyesno("Confirmar", 
                "El sistema está ejecutándose.\n¿Detener y cerrar?")
            if not result:
                return
        
        # Detener adquisición
        self.stop_acquisition()
        
        # Guardar datos finales
        if self.data_manager.get_reading_count() > 0:
            auto_filename = f"data/auto_save_{int(time.time())}.csv"
            self.data_manager.export_to_csv(auto_filename)
            print(f"💾 Auto-guardado: {auto_filename}")
        
        # Cerrar aplicación
        self.root.destroy()
        print("👋 Wally Controller cerrado")
    
    def run(self):
        """Ejecutar aplicación principal"""
        try:
            # Configurar UI
            self.dashboard.setup_ui()
            
            # Mostrar información inicial
            print(f"🚀 Wally DAQ System v{config.VERSION}")
            print(f"📡 ESP32 esperado en: {config.ESP32_IP}:{config.ESP32_PORT}")
            print(f"💾 Directorio de datos: {config.DATA_DIRECTORY}")
            
            # Iniciar loop de Tkinter
            self.root.mainloop()
            
        except Exception as e:
            print(f"❌ Error fatal: {e}")
            messagebox.showerror("Error Fatal", f"Error inesperado: {str(e)}")

def main():
    """Función principal"""
    try:
        # Crear directorio de datos si no existe
        os.makedirs("data", exist_ok=True)
        
        # Inicializar y ejecutar aplicación
        app = WallyController()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Aplicación interrumpida por usuario")
    except Exception as e:
        print(f"❌ Error fatal en main: {e}")

if __name__ == "__main__":
    main()