"""
Genera el contenido del short usando Gemini:
- tema de curiosidad (evitando repetir temas usados recientemente)
- guion narrado (~28-32s hablado)
- título llamativo para YouTube Shorts
- descripción + hashtags
- query en inglés para buscar el clip de vídeo en Pexels
"""
import json
import os
import re
import time
import unicodedata
from datetime import datetime, timedelta

from google import genai
from google.genai import errors as genai_errors

from config import GEMINI_API_KEY, TOPICS_FILE

client = genai.Client(api_key=GEMINI_API_KEY)

DIAS_ENFRIAMIENTO = 30  # un tema no puede repetirse antes de este nº de días

SYSTEM_PROMPT = """Eres un guionista experto en YouTube Shorts de curiosidades y datos
random (ciencia, historia, animales, espacio, cuerpo humano, tecnología, etc.).

Devuelve SIEMPRE y ÚNICAMENTE un JSON válido (sin markdown, sin backticks, sin texto
extra) con estas claves exactas:

{
  "topic": "tema corto en 2-4 palabras, usado para no repetir temas",
  "title": "título en español, máximo 60 caracteres, con
