#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo controlador para la generación de exámenes en PDF
"""

import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.flowables import HRFlowable
from model.pregunta_dao import PreguntaDAO

class ExamenGenerator:
    """
    Controlador para generar exámenes en formato PDF
    """
    
    def __init__(self):
        """
        Constructor de la clase ExamenGenerator
        """
        self.pregunta_dao = PreguntaDAO()
        self.directorio_examenes = "Examenes"
        
        # Crear directorio si no existe
        if not os.path.exists(self.directorio_examenes):
            os.makedirs(self.directorio_examenes)
    
    def generar_examenes(self, cantidad_temas):
        """
        Genera múltiples versiones de exámenes en formato PDF
        
        Args:
            cantidad_temas (int): Número de temas diferentes a generar
            
        Returns:
            list: Lista con las rutas de los archivos PDF generados
        """
        rutas_archivos = []
        
        for i in range(cantidad_temas):
            # Generar letra del tema (A, B, C, ...)
            letra_tema = chr(65 + i)  # 65 es el código ASCII de 'A'
            nombre_archivo = os.path.join(self.directorio_examenes, f"Examen_Tema_{letra_tema}.pdf")
            
            # Generar examen aleatorio
            preguntas_examen = self.pregunta_dao.generar_examen_aleatorio()
            
            # Crear PDF
            if self.generar_pdf(preguntas_examen, nombre_archivo, f"Tema {letra_tema}"):
                rutas_archivos.append(nombre_archivo)
        
        return rutas_archivos
    
    def generar_pdf(self, preguntas, ruta_archivo, titulo_examen):
        """
        Genera un archivo PDF con las preguntas del examen
        
        Args:
            preguntas (list): Lista de objetos Pregunta para el examen
            ruta_archivo (str): Ruta donde se guardará el archivo PDF
            titulo_examen (str): Título del examen (Tema A, Tema B, etc.)
            
        Returns:
            bool: True si el PDF se generó correctamente, False en caso contrario
        """
        try:
            # Configurar el documento
            doc = SimpleDocTemplate(
                ruta_archivo,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Estilos
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='TituloPrincipal',
                fontName='Helvetica-Bold',
                fontSize=16,
                alignment=1,  # Centrado
                spaceBefore=12
            ))
            styles.add(ParagraphStyle(
                name='Pregunta',
                fontName='Helvetica-Bold',
                fontSize=11,
                spaceAfter=6
            ))
            styles.add(ParagraphStyle(
                name='Alternativa',
                fontName='Helvetica',
                fontSize=10,
                leftIndent=20,
                spaceAfter=3
            ))
            
            # Contenido del documento
            contenido = []
            
            # Agregar portada
            self.agregar_portada(contenido, styles, titulo_examen)
            
            # Agregar título
            contenido.append(Paragraph(f"EXAMEN DE ADMISIÓN - {titulo_examen}", styles['TituloPrincipal']))
            contenido.append(Spacer(1, 12))
            
            # Agregar instrucciones
            contenido.append(Paragraph(
                "Instrucciones: Marque la alternativa correcta para cada pregunta.",
                styles['Italic']
            ))
            contenido.append(Spacer(1, 12))
            
            # Agregar preguntas
            for i, pregunta in enumerate(preguntas):
                # Número y enunciado de la pregunta
                contenido.append(Paragraph(
                    f"{i+1}. {pregunta.enunciado}",
                    styles['Pregunta']
                ))
                
                # Alternativas
                contenido.append(Paragraph(f"a) {pregunta.alternativa_a}", styles['Alternativa']))
                contenido.append(Paragraph(f"b) {pregunta.alternativa_b}", styles['Alternativa']))
                contenido.append(Paragraph(f"c) {pregunta.alternativa_c}", styles['Alternativa']))
                contenido.append(Paragraph(f"d) {pregunta.alternativa_d}", styles['Alternativa']))
                contenido.append(Paragraph(f"e) {pregunta.alternativa_e}", styles['Alternativa']))
                
                contenido.append(Spacer(1, 12))
            
            # Construir el documento
            doc.build(contenido)
            return True
            
        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            return False    
    def agregar_portada(self, contenido, styles, titulo_examen):
        """
        Agrega una portada al documento PDF
        """
        # Crear estilos específicos para la portada
        styles.add(ParagraphStyle(
            name='UniversidadTitulo',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=30,
            alignment=1,
            spaceAfter=30
        ))
        
        styles.add(ParagraphStyle(
            name='ExamenTitulo',
            fontName='Helvetica-Bold',
            fontSize=26,
            alignment=1,
            leading=30,
        ))

        styles.add(ParagraphStyle(
            name='Tema',
            fontName='Helvetica-Bold',
            fontSize=32,
            alignment=1,
            leading=30,
            spaceBefore=20,
            spaceAfter=20
        ))

        # Nombre de la universidad (en dos líneas)
        contenido.append(Paragraph(
            'UNIVERSIDAD NACIONAL "SAN LUIS<br/>GONZAGA"',
            styles['UniversidadTitulo']
        ))
        
        # Examen de admisión
        contenido.append(Paragraph(
            "EXAMEN DE ADMISIÓN 2025",
            styles['ExamenTitulo']
        ))
        
        # Espacio antes del logo
        contenido.append(Spacer(1, 0))
        
        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'logo.png')
        if os.path.exists(logo_path):
            img = Image(logo_path)
            img.drawHeight = 5*inch
            img.drawWidth = 5*inch
            contenido.append(img)
        
        # Espacio después del logo
        contenido.append(Spacer(1, 0))
        
        # Modalidad
        contenido.append(Paragraph(
            "MODALIDAD",
            styles['ExamenTitulo']
        ))
        contenido.append(Paragraph(
            "ORDINARIO",
            styles['ExamenTitulo'],
        ))
        
        # Espacio antes del tema
        contenido.append(Spacer(1, 0))
        
        # Tema
        contenido.append(Paragraph(
            f"TEMA: ({titulo_examen[-1]})",
            styles['Tema']
        ))
        
        # Espacio antes del pie de página
        contenido.append(Spacer(1, 0))
        
        # Pie de página
        contenido.append(Paragraph(
            "UNIVERSIDAD LICENCIADA POR SUNEDU",
            ParagraphStyle(
                'PiePagina',
                parent=styles['Normal'],
                alignment=1,
                spaceBefore=14,
                fontSize=16
            )
        ))
        
        # Salto de página
        contenido.append(Paragraph("<br clear=all style='page-break-before:always'/>", styles['Normal']))
