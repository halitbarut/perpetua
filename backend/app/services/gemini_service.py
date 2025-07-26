import google.generativeai as genai
from app.core.config import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def _get_prompt_for_exercise(exercise_type: str, level: str):
    """Alıştırma tipine göre doğru AI prompt'unu döndürür."""
    if exercise_type == "grammar":
        return f"""
        Sen, A1 seviyesinde İngilizce öğreten bir yapay zekasın.
        Görevin, A1 seviyesi için bir gramer sorusu oluşturmak.
        Çıktı olarak SADECE ve SADECE aşağıdaki formatta bir JSON objesi döndür:
        {{
          "question": "Soru metni...",
          "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
          "correct_answer": "Doğru seçeneğin harfi (örn: 'A')"
        }}
        """
    return None

def create_exercise_from_ai(exercise_type: str):
    user_level = "A1"
    prompt = _get_prompt_for_exercise(exercise_type, user_level)

    if not prompt:
        return {"error": "Unsupported exercise type"}

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"AI Error: {e}")
        return None