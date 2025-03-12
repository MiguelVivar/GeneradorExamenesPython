#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generador de Exámenes de Admisión
Sistema para generar múltiples versiones de exámenes de admisión
con preguntas y alternativas en orden aleatorio.
"""

import os
import sys
from view.gui import ExamenGeneratorGUI

def main():
    """
    Función principal que inicia la aplicación
    """
    # Crear directorio para exámenes si no existe
    if not os.path.exists('Examenes'):
        os.makedirs('Examenes')
        
    # Iniciar la interfaz gráfica
    app = ExamenGeneratorGUI()
    app.mainloop()

if __name__ == "__main__":
    main()