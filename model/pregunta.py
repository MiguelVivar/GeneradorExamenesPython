#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo que define la clase Pregunta para el modelo de datos
"""

class Pregunta:
    """
    Clase modelo que representa una pregunta del examen con sus alternativas
    """
    
    def __init__(self, id=None, enunciado=None, alternativa_a=None, alternativa_b=None, 
                 alternativa_c=None, alternativa_d=None, alternativa_e=None):
        """
        Constructor de la clase Pregunta
        
        Args:
            id (int): Identificador único de la pregunta
            enunciado (str): Texto de la pregunta
            alternativa_a (str): Texto de la alternativa A
            alternativa_b (str): Texto de la alternativa B
            alternativa_c (str): Texto de la alternativa C
            alternativa_d (str): Texto de la alternativa D
            alternativa_e (str): Texto de la alternativa E
        """
        self.id = id
        self.enunciado = enunciado
        self.alternativa_a = alternativa_a
        self.alternativa_b = alternativa_b
        self.alternativa_c = alternativa_c
        self.alternativa_d = alternativa_d
        self.alternativa_e = alternativa_e
    
    def __str__(self):
        """
        Representación en cadena de la pregunta
        
        Returns:
            str: Representación textual de la pregunta
        """
        return f"Pregunta {self.id}: {self.enunciado}"