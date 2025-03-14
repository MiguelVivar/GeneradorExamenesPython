#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para la interfaz gráfica del generador de exámenes
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
from PIL import Image, ImageTk
from controller.examen_generator import ExamenGenerator

class ExamenGeneratorGUI(tk.Tk):
    """
    Clase para la interfaz gráfica del generador de exámenes
    """
    
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana principal
        self.title("Generador de Exámenes de Admisión")
        self.geometry("1200x800")
        self.resizable(False, False)
        
        # Cargar imágenes
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        self.logo_path = os.path.join(images_dir, 'logo.png')
        self.banner_path = os.path.join(images_dir, 'banner.png')
        self.hero_path = os.path.join(images_dir, 'hero.jpg')
        
        # Establecer icono de la ventana
        if os.path.exists(self.logo_path):
            logo_icon = tk.PhotoImage(file=self.logo_path)
            self.iconphoto(True, logo_icon)
            # Keep reference to prevent garbage collection
            self.logo_icon = logo_icon
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TSpinbox', font=('Arial', 20))
        self.style.configure('Horizontal.TProgressbar', 
                           background='#FF0000',
                           troughcolor='#f0f0f0',
                           bordercolor='#FF0000',
                           lightcolor='#FF0000',
                           darkcolor='#FF0000')
        
        # Inicializar el controlador
        self.examen_generator = ExamenGenerator()
        
        # Crear los componentes de la interfaz
        self._crear_componentes()
        
        # Centrar la ventana en la pantalla
        self._centrar_ventana()

    def _crear_componentes(self):
        # Frame principal con fondo
        main_frame = tk.Frame(self, bg='#fcf3ea')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Banner superior con efecto de sombra
        banner_frame = tk.Frame(main_frame, bg='#fcf3ea', relief='raised', bd=1)
        banner_frame.pack(fill=tk.X, padx=2, pady=2)
        
        if os.path.exists(self.banner_path):
            banner_img = tk.PhotoImage(file=self.banner_path)
            banner_label = tk.Label(banner_frame, image=banner_img, bg='#fcf3ea')
            banner_label.image = banner_img
            banner_label.pack(fill=tk.X, padx=20, pady=10)
        
        # Contenedor principal con efecto de tarjeta
        card_frame = tk.Frame(main_frame, bg='#fcf3ea', relief='raised', bd=1)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Panel izquierdo para controles
        left_panel = tk.Frame(card_frame, bg='#fcf3ea')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título con efecto de sombra
        title_frame = tk.Frame(left_panel, bg='#fcf3ea', relief='raised', bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            title_frame,
            text="GENERADOR DE TEMAS\nPARA EXÁMEN DE ADMISIÓN",
            font=("Arial", 28, "bold"),
            fg="#FF0000",
            bg='#fcf3ea',
            justify=tk.CENTER
        ).pack(pady=10)
        
        # Contenido mejorado
        content_frame = tk.Frame(left_panel, bg='#fcf3ea')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content_frame,
            text="CANTIDAD DE TEMAS A GENERAR:",
            font=("Arial", 18, "bold"),
            fg="#333333",
            bg='#fcf3ea'
        ).pack(pady=(0, 20))
        
        # Frame para el spinbox con borde
        spin_frame = tk.Frame(content_frame, bg='#fcf3ea', relief='solid', bd=2)
        spin_frame.pack(pady=10)
        
        # Estilo personalizado para el Spinbox
        self.style.configure('Custom.TSpinbox',
                           fieldbackground='white',
                           background='white',
                           arrowcolor='#cc7a29',
                           bordercolor='#cc7a29',
                           darkcolor='#cc7a29',
                           lightcolor='#cc7a29')
        
        self.temas_var = tk.IntVar(value=2)
        self.temas_spinner = ttk.Spinbox(
            spin_frame,
            from_=2,
            to=100,
            textvariable=self.temas_var,
            width=4,
            font=("Arial", 28, "bold"),
            justify=tk.CENTER,
            style='Custom.TSpinbox',
            increment=1,
            wrap=True,
            command=lambda: self.temas_var.set(max(2, min(100, self.temas_var.get())))
        )
        self.temas_spinner.pack(padx=15, pady=8)
        
        # Validación de entrada
        def validate_input(P):
            if P == "": return True
            try:
                value = int(P)
                return 2 <= value <= 100
            except ValueError:
                return False
        
        vcmd = (self.register(validate_input), '%P')
        self.temas_spinner.configure(validate='key', validatecommand=vcmd)
        
        # Botones con efectos hover
        button_frame = tk.Frame(content_frame, bg='#fcf3ea')
        button_frame.pack(pady=30)
        
        self.generar_button = tk.Button(
            button_frame,
            text="GENERAR EXÁMENES",
            command=self._generar_examenes,
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#FF0000",
            activebackground="#CC0000",
            activeforeground="white",
            width=20,
            height=1,
            cursor="hand2",
            relief='flat'
        )
        self.generar_button.pack(pady=10)
        
        self.ver_button = tk.Button(
            button_frame,
            text="VER EXÁMENES",
            command=self._ver_examenes,
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#FF0000",
            activebackground="#CC0000",
            activeforeground="white",
            width=20,
            height=1,
            cursor="hand2",
            relief='flat'
        )
        self.ver_button.pack(pady=10)
        
        # Efectos de hover
        self.generar_button.bind('<Enter>', lambda e: self.generar_button.configure(bg="#CC0000"))
        self.generar_button.bind('<Leave>', lambda e: self.generar_button.configure(bg="#FF0000"))
        self.ver_button.bind('<Enter>', lambda e: self.ver_button.configure(bg="#CC0000"))
        self.ver_button.bind('<Leave>', lambda e: self.ver_button.configure(bg="#FF0000"))
        
        # Panel derecho para hero image
        right_panel = tk.Frame(card_frame, bg='#fcf3ea')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if os.path.exists(self.hero_path):
            hero_img = Image.open(self.hero_path)
            hero_img = hero_img.resize((500, 600), Image.Resampling.LANCZOS)
            hero_photo = ImageTk.PhotoImage(hero_img)
            hero_label = tk.Label(right_panel, image=hero_photo, bg='#fcf3ea')
            hero_label.image = hero_photo
            hero_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Barra de progreso mejorada
        progress_frame = tk.Frame(left_panel, bg='#fcf3ea')
        progress_frame.pack(fill=tk.X, pady=20)
        
        self.progreso_var = tk.DoubleVar()
        self.progreso_bar = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate',
            variable=self.progreso_var,
            style='Horizontal.TProgressbar'
        )
        self.progreso_bar.pack()
        
        # Estado con mejor diseño
        self.estado_var = tk.StringVar(value="Listo para generar exámenes")
        self.estado_label = tk.Label(
            progress_frame,
            textvariable=self.estado_var,
            font=("Arial", 12),
            bg='#fcf3ea',
            fg="#666666"
        )
        self.estado_label.pack(pady=10)  # Add this line to display the label
        
        # Footer mejorado
        footer_frame = tk.Frame(main_frame, bg='#fcf3ea', relief='raised', bd=1)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            footer_frame,
            text="DESARROLLADO POR: III CICLO 'A' 2024-I",
            font=("Arial", 12, "bold"),
            fg="#333333",
            bg='#fcf3ea'
        ).pack(pady=10)

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
    
    def _crear_pantalla_carga(self):
        """
        Crea una pantalla de carga superpuesta
        """
        # Crear ventana de carga
        self.loading_window = tk.Toplevel(self)
        self.loading_window.title("Generando Exámenes")
        self.loading_window.geometry("500x300")
        self.loading_window.resizable(False, False)
        self.loading_window.transient(self)  # Hacer que sea una ventana hija
        self.loading_window.grab_set()  # Bloquear interacción con ventana principal
        
        # Configurar estilo
        self.loading_window.configure(bg='#fcf3ea')
        
        # Centrar la ventana de carga
        self.loading_window.update_idletasks()
        width = self.loading_window.winfo_width()
        height = self.loading_window.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.loading_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Título
        tk.Label(
            self.loading_window,
            text="GENERANDO EXÁMENES",
            font=("Arial", 20, "bold"),
            fg="#FF0000",
            bg='#fcf3ea'
        ).pack(pady=(30, 20))
        
        # Mensaje de carga
        self.loading_message = tk.StringVar(value="Preparando generación...")
        tk.Label(
            self.loading_window,
            textvariable=self.loading_message,
            font=("Arial", 14),
            fg="#333333",
            bg='#fcf3ea'
        ).pack(pady=10)
        
        # Barra de progreso
        self.loading_progress = ttk.Progressbar(
            self.loading_window,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate',
            variable=self.progreso_var,
            style='Horizontal.TProgressbar'
        )
        self.loading_progress.pack(pady=20, padx=50)
        
        # Contador de temas generados
        self.temas_generados = tk.StringVar(value="0 de 0 temas generados")
        tk.Label(
            self.loading_window,
            textvariable=self.temas_generados,
            font=("Arial", 12),
            fg="#666666",
            bg='#fcf3ea'
        ).pack(pady=10)
        
        # Animación de carga (texto parpadeante)
        self.loading_dots = tk.StringVar(value="")
        self.loading_dots_label = tk.Label(
            self.loading_window,
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
        if hasattr(self, 'loading_window') and self.loading_window.winfo_exists():
            dots = self.loading_dots.get()
            if len(dots) >= 6:
                dots = ""
            else:
                dots += "."
            self.loading_dots.set(dots)
            self.after(500, self._animar_puntos)
    
    def _actualizar_pantalla_carga(self, mensaje, progreso, temas_completados=None):
        """
        Actualiza la pantalla de carga
        """
        if hasattr(self, 'loading_window') and self.loading_window.winfo_exists():
            self.loading_message.set(mensaje)
            self.progreso_var.set(progreso)
            if temas_completados is not None:
                total_temas = self.temas_var.get()
                self.temas_generados.set(f"{temas_completados} de {total_temas} temas generados")
    
    def _cerrar_pantalla_carga(self):
        """
        Cierra la pantalla de carga
        """
        if hasattr(self, 'loading_window') and self.loading_window.winfo_exists():
            self.loading_window.destroy()
    
    def _generar_examenes(self):
        """
        Genera los exámenes según la cantidad de temas especificada
        """
        # Obtener la cantidad de temas
        cantidad_temas = self.temas_var.get()
        
        # Deshabilitar botones durante la generación
        self.generar_button.config(state=tk.DISABLED)
        self.ver_button.config(state=tk.DISABLED)
        
        # Reiniciar barra de progreso
        self.progreso_var.set(0)
        self.estado_var.set("Generando exámenes...")
        
        # Mostrar pantalla de carga
        self._crear_pantalla_carga()
        
        # Crear un hilo para generar los exámenes sin bloquear la interfaz
        def generar_en_hilo():
            try:
                # Generar exámenes con actualización de progreso
                temas_completados = 0
                
                # Actualizar mensaje inicial
                self.after(0, lambda: self._actualizar_pantalla_carga(
                    "Iniciando generación de exámenes...", 5, temas_completados))
                
                # Simular progreso de carga inicial (preparación)
                for i in range(1, 6):
                    self.after(i * 200, lambda p=i*4: self._actualizar_pantalla_carga(
                        "Preparando datos...", p, temas_completados))
                
                # Generar exámenes
                rutas_archivos = []
                for i in range(cantidad_temas):
                    # Actualizar progreso
                    progreso = 20 + (i / cantidad_temas) * 80
                    temas_completados = i
                    self.after(0, lambda p=progreso, t=temas_completados, i=i+1: 
                              self._actualizar_pantalla_carga(f"Generando tema {i}...", p, t))
                    
                    # Generar un tema
                    ruta = self.examen_generator.generar_examen(i+1)
                    rutas_archivos.append(ruta)
                
                # Actualizar progreso final
                self.after(0, lambda: self._actualizar_pantalla_carga(
                    "¡Exámenes generados correctamente!", 100, cantidad_temas))
                
                # Pequeña pausa para mostrar el mensaje de finalización
                self.after(1500, lambda: self._mostrar_resultado(rutas_archivos))
                
            except Exception as e:
                # Mostrar error en el hilo principal
                self.after(0, lambda: self._mostrar_error(str(e)))
        
        # Iniciar el hilo
        threading.Thread(target=generar_en_hilo).start()
    
    def _mostrar_resultado(self, rutas_archivos):
        """
        Muestra el resultado de la generación de exámenes
        
        Args:
            rutas_archivos (list): Lista con las rutas de los archivos generados
        """
        # Cerrar pantalla de carga
        self._cerrar_pantalla_carga()
        
        # Actualizar barra de progreso principal
        self.progreso_var.set(100)
        self.estado_var.set("Exámenes generados correctamente")
        
        # Habilitar botones
        self.generar_button.config(state=tk.NORMAL)
        self.ver_button.config(state=tk.NORMAL)
        
        # Mostrar mensaje de éxito
        mensaje = f"Se han generado {len(rutas_archivos)} exámenes correctamente.\n\n"
        mensaje += "Los archivos se encuentran en la carpeta 'Examenes'."
        
        messagebox.showinfo("Generación Exitosa", mensaje)
    
    def _mostrar_error(self, mensaje_error):
        """
        Muestra un mensaje de error
        
        Args:
            mensaje_error (str): Mensaje de error a mostrar
        """
        # Cerrar pantalla de carga
        self._cerrar_pantalla_carga()
        
        # Actualizar estado
        self.estado_var.set("Error al generar exámenes")
        
        # Habilitar botones
        self.generar_button.config(state=tk.NORMAL)
        self.ver_button.config(state=tk.NORMAL)
        
        # Mostrar mensaje de error
        messagebox.showerror("Error", f"Error al generar exámenes:\n{mensaje_error}")
    
    def _ver_examenes(self):
        """
        Abre el explorador de archivos en la carpeta de exámenes
        """
        # Verificar si la carpeta existe
        if not os.path.exists("Examenes"):
            messagebox.showinfo(
                "Información", 
                "No hay exámenes generados. Genere algunos exámenes primero."
            )
            return
        
        # Abrir la carpeta de exámenes
        try:
            if os.name == 'nt':  # Windows
                os.startfile("Examenes")
            elif os.name == 'posix':  # macOS y Linux
                subprocess.call(["open", "Examenes"])
            else:
                messagebox.showinfo(
                    "Información", 
                    f"La carpeta de exámenes se encuentra en: {os.path.abspath('Examenes')}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la carpeta de exámenes:\n{str(e)}")

# Para pruebas
if __name__ == "__main__":
    app = ExamenGeneratorGUI()
    app.mainloop()