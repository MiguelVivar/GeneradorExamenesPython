#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para la pantalla de carga inicial del generador de exámenes
"""

import os
import time
import threading
import queue
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SplashScreen(tk.Toplevel):
    """
    Clase para la pantalla de carga inicial
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configurar la ventana de carga
        self.title("Iniciando Generador de Exámenes")
        self.geometry("620x400")
        self.resizable(False, False)
        self.overrideredirect(True)  # Quitar bordes de la ventana
        
        # Configurar estilo
        self.configure(bg='#fcf3ea')
        
        # Cola para comunicación entre hilos
        self.queue = queue.Queue()
        
        # Centrar la ventana
        self._centrar_ventana()
        
        # Crear los componentes
        self._crear_componentes()
        
        # Iniciar proceso de carga
        self.after(100, self._iniciar_carga)
        
        # Iniciar procesamiento de la cola
        self.after(100, self._procesar_cola)
    
    def _centrar_ventana(self):
        """
        Centra la ventana en la pantalla
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _crear_componentes(self):
        """
        Crea los componentes de la interfaz
        """
        # Frame principal
        main_frame = tk.Frame(self, bg='#fcf3ea')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="GENERADOR DE EXÁMENES DE ADMISIÓN",
            font=("Arial", 20, "bold"),
            fg="#FF0000",
            bg='#fcf3ea'
        ).pack(pady=(20, 10))
        
        # Subtítulo
        tk.Label(
            main_frame,
            text='UNIVERSIDAD NACIONAL "SAN LUIS GONZAGA"',
            font=("Arial", 14, "bold"),
            fg="#333333",
            bg='#fcf3ea'
        ).pack(pady=(0, 20))
        
        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(main_frame, image=logo_photo, bg='#fcf3ea')
            logo_label.image = logo_photo
            logo_label.pack(pady=10)
        
        # Mensaje de carga
        self.loading_message = tk.StringVar(value="Iniciando aplicación...")
        tk.Label(
            main_frame,
            textvariable=self.loading_message,
            font=("Arial", 12),
            fg="#333333",
            bg='#fcf3ea'
        ).pack(pady=10)
        
        # Barra de progreso
        self.style = ttk.Style()
        self.style.configure('Splash.Horizontal.TProgressbar', 
                           background='#FF0000',
                           troughcolor='#f0f0f0',
                           bordercolor='#FF0000',
                           lightcolor='#FF0000',
                           darkcolor='#FF0000')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=500,
            mode='determinate',
            variable=self.progress_var,
            style='Splash.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=20, padx=20)
        
        # Animación de puntos
        self.loading_dots = tk.StringVar(value="")
        self.loading_dots_label = tk.Label(
            main_frame,
            textvariable=self.loading_dots,
            font=("Arial", 16, "bold"),
            fg="#FF0000",
            bg='#fcf3ea'
        )
        self.loading_dots_label.pack(pady=10)
        self._animar_puntos()
    
    def _animar_puntos(self):
        """
        Anima los puntos de carga
        """
        if self.winfo_exists():
            dots = self.loading_dots.get()
            if len(dots) >= 6:
                dots = ""
            else:
                dots += "."
            self.loading_dots.set(dots)
            self.after(500, self._animar_puntos)
    
    def _iniciar_carga(self):
        """
        Inicia el proceso de carga simulado
        """
        def simular_carga():
            # Simular carga de recursos
            self.queue.put(("Conectando a la base de datos...", 10))
            time.sleep(0.5)
            
            self.queue.put(("Cargando banco de preguntas...", 30))
            time.sleep(0.8)
            
            self.queue.put(("Inicializando generador de exámenes...", 60))
            time.sleep(0.7)
            
            self.queue.put(("Preparando interfaz gráfica...", 80))
            time.sleep(0.6)
            
            self.queue.put(("¡Listo para comenzar!", 100))
            time.sleep(0.5)
            
            # Señal para cerrar la ventana
            self.queue.put(("CLOSE", None))
        
        # Iniciar hilo de carga
        threading.Thread(target=simular_carga, daemon=True).start()
    
    def _actualizar_carga(self, mensaje, progreso):
        """
        Actualiza el mensaje y progreso de carga
        
        Args:
            mensaje (str): Mensaje a mostrar
            progreso (int): Valor del progreso (0-100)
        """
        self.loading_message.set(mensaje)
        self.progress_var.set(progreso)
    
    def _procesar_cola(self):
        """
        Procesa los mensajes de la cola en el hilo principal
        """
        try:
            while True:
                mensaje, progreso = self.queue.get_nowait()
                
                if mensaje == "CLOSE":
                    self.destroy()
                    return
                
                self._actualizar_carga(mensaje, progreso)
                self.queue.task_done()
        except queue.Empty:
            # Si la cola está vacía, programar la próxima verificación
            if self.winfo_exists():
                self.after(100, self._procesar_cola)