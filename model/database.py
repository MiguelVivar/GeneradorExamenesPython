#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para la conexión a la base de datos MySQL
"""

import os
import configparser
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Clase para manejar la conexión a la base de datos MySQL
    """
    _connection = None
    
    @staticmethod
    def get_connection():
        """
        Obtiene una conexión a la base de datos
        
        Returns:
            mysql.connector.connection.MySQLConnection: Objeto de conexión a MySQL
        """
        if DatabaseConnection._connection is None or not DatabaseConnection._connection.is_connected():
            try:
                # Cargar configuración desde archivo
                config = configparser.ConfigParser()
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'database.ini')
                
                if not os.path.exists(config_path):
                    raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
                
                config.read(config_path)
                
                # Obtener credenciales
                host = config['mysql']['host']
                database = config['mysql']['database']
                user = config['mysql']['user']
                password = config['mysql']['password']
                
                # Establecer conexión
                DatabaseConnection._connection = mysql.connector.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password
                )
                
                print("Conexión a MySQL establecida correctamente")
                
            except Error as e:
                print(f"Error al conectar a MySQL: {e}")
                raise
            except FileNotFoundError as e:
                print(e)
                raise
            except Exception as e:
                print(f"Error inesperado: {e}")
                raise
                
        return DatabaseConnection._connection
    
    @staticmethod
    def close_connection():
        """
        Cierra la conexión a la base de datos
        """
        if DatabaseConnection._connection and DatabaseConnection._connection.is_connected():
            DatabaseConnection._connection.close()
            print("Conexión a MySQL cerrada")