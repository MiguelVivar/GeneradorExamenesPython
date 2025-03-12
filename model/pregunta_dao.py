#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para el acceso a datos de las preguntas
"""

import random
from model.database import DatabaseConnection
from model.pregunta import Pregunta

class PreguntaDAO:
    """
    Clase de acceso a datos para las preguntas del examen
    """
    
    def obtener_todas_las_preguntas(self):
        """
        Obtiene todas las preguntas de la base de datos
        
        Returns:
            list: Lista de objetos Pregunta
        """
        preguntas = []
        sql = "SELECT id, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e FROM preguntas"
        
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            for row in resultados:
                pregunta = Pregunta(
                    id=row[0],
                    enunciado=row[1],
                    alternativa_a=row[2],
                    alternativa_b=row[3],
                    alternativa_c=row[4],
                    alternativa_d=row[5],
                    alternativa_e=row[6]
                )
                preguntas.append(pregunta)
                
            cursor.close()
            
        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
        
        return preguntas
    
    def obtener_preguntas_aleatorias(self):
        """
        Obtiene todas las preguntas en orden aleatorio
        
        Returns:
            list: Lista de objetos Pregunta en orden aleatorio
        """
        preguntas = self.obtener_todas_las_preguntas()
        
        # Mezclar el orden de las preguntas
        random.shuffle(preguntas)
        
        return preguntas
    
    def reorganizar_alternativas(self, pregunta):
        """
        Reorganiza aleatoriamente las alternativas de una pregunta
        
        Args:
            pregunta (Pregunta): La pregunta cuyas alternativas se reorganizarán
            
        Returns:
            Pregunta: Una nueva pregunta con las alternativas reorganizadas
        """
        # Crear una lista con las alternativas
        alternativas = [
            pregunta.alternativa_a,
            pregunta.alternativa_b,
            pregunta.alternativa_c,
            pregunta.alternativa_d,
            pregunta.alternativa_e
        ]
        
        # Mezclar las alternativas
        random.shuffle(alternativas)
        
        # Crear una nueva pregunta con las alternativas reorganizadas
        return Pregunta(
            id=pregunta.id,
            enunciado=pregunta.enunciado,
            alternativa_a=alternativas[0],
            alternativa_b=alternativas[1],
            alternativa_c=alternativas[2],
            alternativa_d=alternativas[3],
            alternativa_e=alternativas[4]
        )
    
    def generar_examen_aleatorio(self):
        """
        Genera un conjunto de preguntas con alternativas reorganizadas para un tema específico
        
        Returns:
            list: Lista de preguntas con alternativas reorganizadas
        """
        preguntas_originales = self.obtener_preguntas_aleatorias()
        preguntas_reorganizadas = []
        
        for pregunta in preguntas_originales:
            preguntas_reorganizadas.append(self.reorganizar_alternativas(pregunta))
        
        return preguntas_reorganizadas