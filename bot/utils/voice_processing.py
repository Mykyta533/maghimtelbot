"""Обробка голосових повідомлень"""
import os
import asyncio
from gtts import gTTS
import tempfile
import subprocess
from typing import Optional

async def voice_to_text(voice_file_path: str) -> Optional[str]:
    """Конвертація голосу в текст через Whisper"""
    try:
        # Тут би була інтеграція з Whisper API
        # Поки що повертаємо заглушку
        return "Приклад розпізнаного тексту з голосового повідомлення"
        
    except Exception as e:
        print(f"Помилка розпізнавання голосу: {e}")
        return None

async def text_to_voice(text: str, user_id: int) -> Optional[str]:
    """Конвертація тексту в голос через gTTS"""
    try:
        # Обмежуємо довжину тексту для TTS
        if len(text) > 500:
            text = text[:500] + "..."
        
        # Створюємо тимчасовий файл
        temp_file = f"temp_tts_{user_id}.mp3"
        
        # Генеруємо голос
        tts = gTTS(text=text, lang='uk', slow=False)
        tts.save(temp_file)
        
        return temp_file
        
    except Exception as e:
        print(f"Помилка генерації голосу: {e}")
        return None

def convert_ogg_to_wav(ogg_path: str) -> Optional[str]:
    """Конвертація OGG в WAV для Whisper"""
    try:
        wav_path = ogg_path.replace('.ogg', '.wav')
        
        # Використовуємо ffmpeg для конвертації
        subprocess.run([
            'ffmpeg', '-i', ogg_path, '-ar', '16000', '-ac', '1', wav_path
        ], check=True, capture_output=True)
        
        return wav_path
        
    except Exception as e:
        print(f"Помилка конвертації аудіо: {e}")
        return None