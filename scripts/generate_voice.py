"""
Convierte el guion en audio narrado usando edge-tts.
No requiere API key ni tarjeta: usa las voces neuronales de Microsoft Edge
de forma gratuita.
"""
import asyncio
import os

import edge_tts

from config import TTS_VOICE, WORKDIR


async def _generate(text, out_path):
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate="+2%")
    await communicate.save(out_path)


def generate_voice(script_text, out_path=None):
    out_path = out_path or os.path.join(WORKDIR, "voice.mp3")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    asyncio.run(_generate(script_text, out_path))
    return out_path


if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "Esto es una prueba de voz."
    path = generate_voice(text)
    print("Audio generado en:", path)
