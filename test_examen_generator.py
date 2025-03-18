#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar directamente la funcionalidad de generación de Word del ExamenGenerator
"""

import os
import sys
from controller.examen_generator import ExamenGenerator

print('Iniciando prueba directa del ExamenGenerator...')

# Verificar directorio de exámenes
if not os.path.exists('Examenes'):
    os.makedirs('Examenes')
    print('Se creó el directorio Examenes')
else:
    print('El directorio Examenes ya existe')

# Crear instancia del generador
generador = ExamenGenerator()

# Probar generación de Word directamente
try:
    print('Generando examen Word tema A...')
    ruta = generador.generar_examen_word(1)  # Tema A
    if ruta and os.path.exists(ruta):
        print(f'Examen Word generado exitosamente en: {ruta}')
        tamaño = os.path.getsize(ruta)
        print(f'Tamaño del archivo: {tamaño} bytes')
    else:
        print('Error: No se generó el archivo Word o la ruta es inválida')
        
    print('\nGenerando examen PDF tema B para comparar...')
    ruta_pdf = generador.generar_examen_pdf(2)  # Tema B
    if ruta_pdf and os.path.exists(ruta_pdf):
        print(f'Examen PDF generado exitosamente en: {ruta_pdf}')
        tamaño_pdf = os.path.getsize(ruta_pdf)
        print(f'Tamaño del archivo PDF: {tamaño_pdf} bytes')
    else:
        print('Error: No se generó el archivo PDF o la ruta es inválida')
        
except Exception as e:
    print(f'Error durante la generación: {e}')
    import traceback
    traceback.print_exc()

print('\nPrueba completada.')