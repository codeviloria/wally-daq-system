"""
Dashboard UI para Wally - Sistema de Adquisición de Datos
Interfaz gráfica completa con Tkinter y matplotlib
"""
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import numpy as np
from collections import deque
from datetime import datetime
import config

class WallyDashboard:
    """Dashboard principal del sistema Wally"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Datos para gráficos
        self.plot_data = {
            sensor: deque(maxlen=config.MAX_CHART_POINTS) 
            for sensor in config.SENSOR_LABELS.keys()
        }
        self.time_data = deque(maxlen=config.MAX_CHART_POINTS)
        
        # Referencias a widgets
        self.status_label = None
        self.sensor_frames = {}
        self.chart_canvas = None
        self.stats_labels = {}
        self.control_buttons = {}
        
        # Estado
        self.last_update = None
    
    def setup_ui(self):
        """Configurar interfaz completa"""
        # Configurar grid principal
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Configurar paneles
        self.setup_header(main_frame)
        self.setup_sensors_panel(main_frame)
        self.setup_chart_panel(main_frame)
        self.setup_controls_panel(main_frame)
        self.setup_stats_panel(main_frame)
        
        print("🖥️ Dashboard UI configurado")
    
    def setup_header(self, parent):
        """Configurar header con título y status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(header_frame, text="🔬 Wally - Sistema de Adquisición de Datos", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Status en tiempo real
        self.status_label = ttk.Label(header_frame, text="🔴 Desconectado", 
                                     font=("Arial", 14, "bold"))
        self.status_label.grid(row=0, column=1, sticky=tk.E)
        
        # Línea separadora
        ttk.Separator(header_frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def setup_sensors_panel(self, parent):
        """Panel de sensores en tiempo real"""
        sensors_frame = ttk.LabelFrame(parent, text="📊 Sensores en Tiempo Real", padding="10")
        sensors_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Crear tarjetas para cada sensor
        for i, (sensor_key, sensor_label) in enumerate(config.SENSOR_LABELS.items()):
            # Frame individual
            card_frame = ttk.LabelFrame(sensors_frame, text=sensor_label, padding="15")
            card_frame.pack(fill=tk.X, pady=8)
            
            # Valor principal
            value_label = ttk.Label(card_frame, text="--", 
                                   font=("Arial", 28, "bold"), 
                                   foreground=config.CHART_COLORS[sensor_key])
            value_label.pack()
            
            # Unidad
            unit_label = ttk.Label(card_frame, text="--", 
                                  font=("Arial", 12))
            unit_label.pack()
            
            # Status y último update
            status_frame = ttk.Frame(card_frame)
            status_frame.pack(fill=tk.X, pady=(5, 0))
            
            status_label = ttk.Label(status_frame, text="🔴 Desconectado", 
                                    font=("Arial", 10))
            status_label.pack(side=tk.LEFT)
            
            time_label = ttk.Label(status_frame, text="", 
                                  font=("Arial", 9), foreground="gray")
            time_label.pack(side=tk.RIGHT)
            
            # Guardar referencias
            self.sensor_frames[sensor_key] = {
                'value': value_label,
                'unit': unit_label,
                'status': status_label,
                'time': time_label,
                'frame': card_frame
            }
    
    def setup_chart_panel(self, parent):
        """Panel de gráficos históricos"""
        chart_frame = ttk.LabelFrame(parent, text="📈 Gráficos en Tiempo Real", padding="10")
        chart_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear figura matplotlib
        plt.style.use('default')
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))
        self.fig.suptitle("Sensores Wally - Datos Históricos", fontsize=14, fontweight='bold')
        
        # Configurar cada subplot
        sensors = list(config.SENSOR_LABELS.keys())
        for i, sensor_key in enumerate(sensors):
            row, col = i // 2, i % 2
            ax = self.axes[row, col]
            
            sensor_label = config.SENSOR_LABELS[sensor_key]
            sensor_unit = config.SENSOR_UNITS[sensor_key]
            color = config.CHART_COLORS[sensor_key]
            
            ax.set_title(f"{sensor_label}", fontsize=12, fontweight='bold')
            ax.set_ylabel(f"Valor ({sensor_unit})")
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45, labelsize=8)
            
            # Configurar límites iniciales
            sensor_range = config.SENSOR_RANGES.get(sensor_key, (0, 100))
            ax.set_ylim(sensor_range[0] * 0.9, sensor_range[1] * 1.1)
        
        plt.tight_layout()
        
        # Integrar con Tkinter
        self.chart_canvas = FigureCanvasTkinter(self.fig, chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar de matplotlib (opcional)
        # toolbar = NavigationToolbar2Tk(self.chart_canvas, chart_frame)
        # toolbar.update()
    
    def setup_controls_panel(self, parent):
        """Panel de controles principales"""
        controls_frame = ttk.LabelFrame(parent, text="🎛️ Controles", padding="10")
        controls_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Frame para botones principales
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Botones principales
        self.control_buttons['start'] = ttk.Button(
            buttons_frame, text="▶️ Iniciar Adquisición", 
            command=self.controller.start_acquisition, style="Accent.TButton")
        self.control_buttons['start'].pack(side=tk.LEFT, padx=5)
        
        self.control_buttons['stop'] = ttk.Button(
            buttons_frame, text="⏹️ Detener", 
            command=self.controller.stop_acquisition, state=tk.DISABLED)
        self.control_buttons['stop'].pack(side=tk.LEFT, padx=5)
        
        self.control_buttons['export'] = ttk.Button(
            buttons_frame, text="📥 Exportar CSV", 
            command=self.controller.export_data)
        self.control_buttons['export'].pack(side=tk.LEFT, padx=5)
        
        # Separador vertical
        ttk.Separator(controls_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Frame para información adicional
        info_frame = ttk.Frame(controls_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Labels de información
        ttk.Label(info_frame, text="📊 Estadísticas:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.stats_labels['readings'] = ttk.Label(info_frame, text="Lecturas: 0")
        self.stats_labels['readings'].pack(anchor=tk.W)
        
        self.stats_labels['duration'] = ttk.Label(info_frame, text="Duración: 00:00:00")
        self.stats_labels['duration'].pack(anchor=tk.W)
        
        self.stats_labels['rate'] = ttk.Label(info_frame, text="Tasa: 0.0 Hz")
        self.stats_labels['rate'].pack(anchor=tk.W)
    
    def setup_stats_panel(self, parent):
        """Panel de estadísticas (si es necesario más detalle)"""
        pass  # Expandir en futuras versiones
    
    def update_sensors(self, readings):
        """Actualizar displays de sensores"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        for sensor_key, frames in self.sensor_frames.items():
            if sensor_key in readings:
                reading = readings[sensor_key]
                
                if reading['status'] == 'active' and reading['value'] is not None:
                    # Sensor activo
                    value = reading['value']
                    unit = reading['unit']
                    
                    frames['value'].config(text=f"{value:.2f}", 
                                         foreground=config.CHART_COLORS[sensor_key])
                    frames['unit'].config(text=unit)
                    frames['status'].config(text="🟢 Activo", foreground="green")
                    frames['time'].config(text=current_time)
                    
                    # Validar rango
                    sensor_range = config.SENSOR_RANGES.get(sensor_key, (float('-inf'), float('inf')))
                    if not (sensor_range[0] <= value <= sensor_range[1]):
                        frames['value'].config(foreground="red")
                        frames['status'].config(text="⚠️ Fuera de rango", foreground="orange")
                
                else:
                    # Sensor con error
                    frames['value'].config(text="ERROR", foreground="red")
                    frames['unit'].config(text="--")
                    frames['status'].config(text="🔴 Error", foreground="red")
                    frames['time'].config(text=current_time)
            
            else:
                # Sensor no disponible
                frames['value'].config(text="--", foreground="gray")
                frames['unit'].config(text="--")
                frames['status'].config(text="🔘 No disponible", foreground="gray")
                frames['time'].config(text="")
    
    def update_chart(self, data):
        """Actualizar gráficos en tiempo real"""
        if not data or 'readings' not in data:
            return
        
        # Agregar timestamp
        current_time = datetime.fromtimestamp(data['timestamp'])
        self.time_data.append(current_time)
        
        # Agregar datos de sensores
        readings = data['readings']
        for sensor_key in config.SENSOR_LABELS.keys():
            if sensor_key in readings and readings[sensor_key]['value'] is not None:
                value = readings[sensor_key]['value']
                self.plot_data[sensor_key].append(value)
            else:
                # Usar último valor conocido o None
                if len(self.plot_data[sensor_key]) > 0:
                    self.plot_data[sensor_key].append(self.plot_data[sensor_key][-1])
                else:
                    self.plot_data[sensor_key].append(0)
        
        # Actualizar gráficos solo si hay suficientes datos
        if len(self.time_data) < 2:
            return
        
        # Redraw charts
        sensors = list(config.SENSOR_LABELS.keys())
        for i, sensor_key in enumerate(sensors):
            row, col = i // 2, i % 2
            ax = self.axes[row, col]
            ax.clear()
            
            # Configurar ejes
            sensor_label = config.SENSOR_LABELS[sensor_key]
            sensor_unit = config.SENSOR_UNITS[sensor_key]
            color = config.CHART_COLORS[sensor_key]
            
            ax.set_title(f"{sensor_label}", fontsize=12, fontweight='bold')
            ax.set_ylabel(f"Valor ({sensor_unit})")
            ax.grid(True, alpha=0.3)
            
            # Plot data si hay datos
            if len(self.plot_data[sensor_key]) > 0:
                times = list(self.time_data)
                values = list(self.plot_data[sensor_key])
                
                ax.plot(times, values, color=color, linewidth=2, marker='o', markersize=3)
                
                # Formatear eje X
                if len(times) > 10:
                    # Mostrar solo algunas etiquetas para evitar solapamiento
                    step = max(1, len(times) // 5)
                    ax.set_xticks(times[::step])
                
                ax.tick_params(axis='x', rotation=45, labelsize=8)
                
                # Auto-scale Y con margen
                if values:
                    min_val, max_val = min(values), max(values)
                    margin = (max_val - min_val) * 0.1 if max_val != min_val else 1
                    ax.set_ylim(min_val - margin, max_val + margin)
        
        plt.tight_layout()
        self.chart_canvas.draw()
    
    def update_stats(self, stats):
        """Actualizar estadísticas del sistema"""
        if not stats:
            return
        
        # Actualizar labels de estadísticas
        self.stats_labels['readings'].config(text=f"Lecturas: {stats.get('total_readings', 0)}")
        
        duration = stats.get('duration_seconds', 0)
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        self.stats_labels['duration'].config(text=f"Duración: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        rate = stats.get('sample_rate', 0)
        self.stats_labels['rate'].config(text=f"Tasa: {rate:.1f} Hz")
    
    def update_status(self, status):
        """Actualizar status del sistema"""
        self.status_label.config(text=status)
        
        # Cambiar color según status
        if "🟢" in status:
            self.status_label.config(foreground="green")
        elif "🔴" in status:
            self.status_label.config(foreground="red")
        elif "🔄" in status:
            self.status_label.config(foreground="orange")
        else:
            self.status_label.config(foreground="black")
    
    def set_controls_state(self, state):
        """Cambiar estado de controles (running/stopped)"""
        if state == "running":
            self.control_buttons['start'].config(state=tk.DISABLED)
            self.control_buttons['stop'].config(state=tk.NORMAL)
        elif state == "stopped":
            self.control_buttons['start'].config(state=tk.NORMAL)
            self.control_buttons['stop'].config(state=tk.DISABLED)
    
    def get_export_filename(self):
        """Obtener nombre de archivo para exportación"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"wally_data_{timestamp}.csv"
        
        filename = filedialog.asksaveasfilename(
            title="Exportar datos de sensores",
            defaultextension=".csv",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ],
            initialname=default_name,
            initialdir=config.DATA_DIRECTORY
        )
        
        return filename