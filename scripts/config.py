"""
Configuración central del bot.
Todas las claves se leen de variables de entorno (nunca hardcodeadas),
que en producción vienen de los Secrets de GitHub Actions.
"""
import os

# --- APIs de contenido ---
PEXELS_API_KEY = os.environ["PEXELS_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# --- YouTube OAuth ---
YT_CLIENT_ID = os.environ["YT_CLIENT_ID"]
YT_CLIENT_SECRET = os.environ["YT_CLIENT_SECRET"]
YT_REFRESH_TOKEN = os.environ["YT_REFRESH_TOKEN"]

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# --- Parámetros del vídeo ---
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
TARGET_DURATION = 30  # segundos aprox. de cada short
TTS_VOICE = "es-ES-AlvaroNeural"  # voz en español (España), gratis vía edge-tts
MUSIC_VOLUME = 0.12  # volumen relativo de la música de fondo frente a la voz

# --- Rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "font.ttf")
WORKDIR = os.path.join(BASE_DIR, "workdir")
TOPICS_FILE = os.path.join(BASE_DIR, "topics_used.json")
