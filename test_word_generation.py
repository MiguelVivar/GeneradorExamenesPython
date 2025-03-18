#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de prueba para diagnosticar problemas con la generación de documentos Word
"""

import os
import sys

print('Iniciando prueba de generación de documentos Word...')

# Verificar directorio de exámenes
if not os.path.exists('Examenes'):
    os.makedirs('Examenes')
    print('Se creó el directorio Examenes')
else:
    print('El directorio Examenes ya existe')

# Probar la generación de documentos Word
try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    
    print('Biblioteca python-docx importada correctamente')
    
    # Crear un documento de prueba
    doc = Document()
    doc.add_paragraph('Documento de prueba')
    test_path = os.path.join('Examenes', 'test_document.docx')
    doc.save(test_path)
    print(f'Documento Word creado exitosamente en: {test_path}')
except ImportError as e:
    print(f'Error al importar la biblioteca python-docx: {e}')
    print('Asegúrese de que python-docx esté instalado correctamente (pip install python-docx)')
    sys.exit(1)
except Exception as e:
    print(f'Error al crear el documento Word: {e}')
    sys.exit(1)

# Probar la conexión a la base de datos
try:
    import mysql.connector
    from mysql.connector import Error
    
    print('\nProbando conexión a la base de datos...')
    
    # Verificar si existe el directorio config
    if not os.path.exists('config'):
        print('El directorio config no existe')
        os.makedirs('config')
        print('Se creó el directorio config')
    
    # Verificar si existe el archivo database.ini
    config_path = os.path.join('config', 'database.ini')
    if not os.path.exists(config_path):
        print('El archivo database.ini no existe')
        with open(config_path, 'w') as f:
            f.write('[mysql]\nhost = localhost\ndatabase = examen_db\nuser = root\npassword = root')
        print('Se creó el archivo database.ini con configuración predeterminada')
    
    # Intentar conectar a la base de datos
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='examen_db',
            user='root',
            password='root'
        )
        
        if conn.is_connected():
            print('Conexión a la base de datos exitosa')
            
            # Verificar si existen preguntas en la base de datos
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM preguntas')
            count = cursor.fetchone()[0]
            print(f'Número de preguntas en la base de datos: {count}')
            
            cursor.close()
            conn.close()
    except Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        print('\nCreando base de datos de prueba...')
        
        # Intentar crear la base de datos y tabla de prueba
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root'
            )
            
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Crear base de datos si no existe
                cursor.execute('CREATE DATABASE IF NOT EXISTS examen_db')
                print('Base de datos examen_db creada o ya existente')
                
                # Usar la base de datos
                cursor.execute('USE examen_db')
                
                # Crear tabla de preguntas si no existe
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS preguntas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    enunciado TEXT NOT NULL,
                    alternativa_a TEXT NOT NULL,
                    alternativa_b TEXT NOT NULL,
                    alternativa_c TEXT NOT NULL,
                    alternativa_d TEXT NOT NULL,
                    alternativa_e TEXT NOT NULL
                )
                ''')
                print('Tabla preguntas creada o ya existente')
                
                # Insertar una pregunta de prueba
                cursor.execute('''
                INSERT INTO preguntas (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e)
                VALUES ('¿Cuál es la capital de Perú?', 'Lima', 'Bogotá', 'Santiago', 'Quito', 'La Paz')
                ''')
                conn.commit()
                print('Pregunta de prueba insertada')
                
                cursor.close()
                conn.close()
        except Error as e:
            print(f'Error al crear la base de datos de prueba: {e}')

except ImportError as e:
    print(f'Error al importar la biblioteca mysql-connector-python: {e}')
    print('Asegúrese de que mysql-connector-python esté instalado correctamente (pip install mysql-connector-python)')

print('\nPrueba completada. Revise los mensajes anteriores para diagnosticar posibles problemas.')