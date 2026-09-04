"""
Genera el contenido del short usando Gemini:
- tema de curiosidad (evitando repetir temas ya usados)
- guion narrado (~28-32s hablado)
- título llamativo para YouTube Shorts
- descripción + hashtags
- query en inglés para buscar el clip de vídeo en Pexels
"""
import json
import os
import re
import time
from datetime import datetime

from google import genai
from google.genai import errors as genai_errors

from config import GEMINI_API_KEY, TOPICS_FILE

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Eres un guionista experto en YouTube Shorts de curiosidades y datos
random (ciencia, historia, animales, espacio, cuerpo humano, tecnología, etc.).

Devuelve SIEMPRE y ÚNICAMENTE un JSON válido (sin markdown, sin backticks, sin texto
extra) con estas claves exactas:

{
  "topic": "tema corto en 2-4 palabras, usado para no repetir temas",
  "title": "título en español, máximo 60 caracteres, con gancho/curiosidad, sin comillas",
  "script": "guion en español, 65-85 palabras, tono cercano y sorprendente, empieza con
              un gancho fuerte en la primera frase, sin emojis, listo para ser narrado
              en voz alta en unos 28-32 segundos",
  "description": "descripción para YouTube de 2-3 frases, en español",
  "hashtags": ["#shorts", "#curiosidades", "#dato3", "#dato4", "#dato5"],
  "pexels_query": "2-4 palabras EN INGLÉS que describan una imagen o vídeo genérico
                    relacionado con el tema (para buscar stock footage), ej. 'ocean waves',
                    'brain neurons', 'ancient ruins'"
}

Reglas:
- El guion debe caber hablado en 30 segundos aproximadamente (no más de 85 palabras).
- No repitas ninguno de los temas ya usados que se te pasan.
- El pexels_query debe describir algo VISUAL genérico y fácil de encontrar en un banco
  de stock (paisajes, naturaleza, ciudad, laboratorio, espacio, animales...), no algo
  demasiado específico.
"""


def _load_used_topics():
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_used_topic(topic):
    used = _load_used_topics()
    used.append({"topic": topic, "date": datetime.utcnow().isoformat()})
    # nos quedamos solo con los últimos 200 para no repetir sin que el archivo crezca infinito
    used = used[-200:]
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def _extract_json(text):
    """Limpia posibles ```json ... ``` que a veces añade el modelo."""
    text = text.strip()
    text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def generate_content():
    used_topics = [t["topic"] for t in _load_used_topics()]
    used_list_str = ", ".join(used_topics[-40:]) if used_topics else "ninguno todavía"

    user_prompt = f"Temas ya usados recientemente (NO los repitas): {used_list_str}\n\nGenera un short nuevo."

    max_retries = 3
    last_error = None
    response = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_prompt,
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "temperature": 1.0,
                },
            )
            break
        except genai_errors.ServerError as e:
            last_error = e
            wait = 15 * attempt  # 15s, 30s, 45s
            print(f"Gemini sobrecargado (intento {attempt}/{max_retries}), reintentando en {wait}s...")
            time.sleep(wait)

    if response is None:
        raise last_error

    data = _extract_json(response.text)
    _save_used_topic(data["topic"])
    return data


if __name__ == "__main__":
    content = generate_content()
    print(json.dumps(content, ensure_ascii=False, indent=2))
