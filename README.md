# Generador de Exámenes de Admisión (Python)

Sistema de generación automática de exámenes de admisión para la Universidad Nacional "San Luis Gonzaga" implementado en Python.

## Descripción

Esta aplicación permite generar múltiples versiones de exámenes de admisión de manera automática, facilitando la creación de diferentes temas para los procesos de admisión universitaria. Cada tema contiene las mismas 100 preguntas pero en orden aleatorio, y con las 5 alternativas (a-e) también en orden aleatorio para cada pregunta.

## Características

- Interfaz gráfica intuitiva y fácil de usar con Tkinter
- Generación de múltiples temas de examen (de 2 hasta 100)
- Exportación automática en formato PDF
- Visualización directa de los exámenes generados
- Diseño personalizado con la imagen institucional
- Almacenamiento de preguntas en base de datos MySQL

## Requisitos del Sistema

- Python 3.8 o superior
- MySQL Server
- Bibliotecas Python: tkinter, mysql-connector-python, reportlab
- Sistema operativo: Windows, Linux o macOS
- Memoria RAM: 2GB mínimo recomendado
- Espacio en disco: 100MB mínimo

## Instalación

1. Clone este repositorio
2. Instale las dependencias: `pip install -r requirements.txt`
3. Configure la base de datos MySQL según las instrucciones en `config/database.ini`
4. Ejecute la aplicación: `python main.py`

## Configuración de la Base de Datos

1. Cree una base de datos MySQL llamada `examen_db`:
   ```sql
   CREATE DATABASE examen_db;
   USE examen_db;
   ```

2. Cree la tabla `preguntas` con la siguiente estructura:
   ```sql
   CREATE TABLE preguntas (
     id INT AUTO_INCREMENT PRIMARY KEY,
     enunciado TEXT NOT NULL,
     alternativa_a TEXT NOT NULL,
     alternativa_b TEXT NOT NULL,
     alternativa_c TEXT NOT NULL,
     alternativa_d TEXT NOT NULL,
     alternativa_e TEXT NOT NULL
   );
   ```

3. Inserte preguntas de ejemplo (opcional):
   ```sql
   INSERT INTO preguntas (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e) VALUES
   ('¿Cuál es la capital de Perú?', 'Lima', 'Arequipa', 'Cusco', 'Trujillo', 'Ica');
   -- Añada más preguntas según sea necesario
   ```

4. Configure los parámetros de conexión en el archivo `config/database.ini`:
   ```ini
   [mysql]
   host = localhost
   database = examen_db
   user = root
   password = root
   ```
   *Nota: Modifique el usuario y contraseña según su configuración de MySQL*

## Uso

1. Inicie la aplicación
2. Seleccione la cantidad de temas que desea generar (2-100)
3. Haga clic en "GENERAR EXÁMENES"
4. Los exámenes se guardarán automáticamente en la carpeta "Examenes"
5. Use el botón "VER EXÁMENES" para acceder a los archivos generados

## Desarrollado por

III Ciclo "A" 2024-I
Universidad Nacional "San Luis Gonzaga"

## Licencia

Este proyecto es de uso exclusivo para la Universidad Nacional "San Luis Gonzaga".