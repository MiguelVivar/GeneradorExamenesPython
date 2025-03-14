#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generador de Exámenes de Admisión
Sistema para generar múltiples versiones de exámenes de admisión
con preguntas y alternativas en orden aleatorio.
"""

import os
import sys
import tkinter as tk
from view.gui import ExamenGeneratorGUI
from view.splash_screen import SplashScreen

def main():
    """
    Función principal que inicia la aplicación
    """
    # Crear directorio para exámenes si no existe
    if not os.path.exists('Examenes'):
        os.makedirs('Examenes')
    
    # Crear una ventana raíz temporal para mostrar el splash screen
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana raíz temporal
    
    # Mostrar pantalla de carga
    splash = SplashScreen(root)
    
    # Esperar a que se cierre la pantalla de carga
    root.wait_window(splash)
    
    # Cerrar ventana raíz temporal
    root.destroy()
    
    # Iniciar la interfaz gráfica principal
    app = ExamenGeneratorGUI()
    app.mainloop()

if __name__ == "__main__":
    main()