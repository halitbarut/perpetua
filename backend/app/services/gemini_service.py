import google.generativeai as genai
from app.core.config import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def _get_prompt_for_exercise(exercise_type: str, level: str):
    """Alıştırma tipine göre doğru AI prompt'unu döndürür."""
    if exercise_type == "grammar":
        return f"""
        Sen, A1 seviyesinde İngilizce öğreten bir yapay zekasın.
        Görevin, A1 seviyesi için "cümle tamamlama" formatında 5 adet gramer sorusu oluşturmak.
        Her soru, içinde '___' bulunan bir cümle ve bu boşluğa gelebilecek kelimelerden oluşan bir kelime bankası içermelidir.

        KURALLAR:
        1. Toplam 5 adet soru nesnesi oluştur.
        2. Her soru için 4 kelimelik bir kelime bankası oluştur (1 doğru, 3 yanlış).
        3. Çıktı olarak SADECE ve SADECE bir JSON objesi döndür. Bu obje, "questions" adında bir anahtar ve bu 5 soru nesnesini içeren bir liste barındırmalıdır.
        4. Her soru nesnesi şu alanları içermelidir: "sentence_template", "word_bank", "correct_word".

        ÖRNEK ÇIKTI FORMATI:
        {{
          "questions": [
            {{
              "sentence_template": "She ___ an apple.",
              "word_bank": ["eat", "eats", "ate", "eating"],
              "correct_word": "eats"
            }},
            {{
              "sentence_template": "There ___ two cats on the roof.",
              "word_bank": ["is", "are", "am", "be"],
              "correct_word": "are"
            }}
          ]
        }}

        Şimdi {level} seviyesi için 5 soruluk listeyi oluştur.
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


def evaluate_exercise_from_ai(results: dict, username: str):
    user_performance = f"Kullanıcı {results['total_questions']} sorudan {results['correct_answers']} tanesini doğru cevapladı."
    mistakes_summary = "Kullanıcının yaptığı hatalar:\n"
    if results['wrong_answers']:
        for item in results['wrong_answers']:
            mistakes_summary += f"- Soru: '{item['question']}', Kullanıcının Cevabı: '{item['user_answer']}', Doğru Cevap: '{item['correct_answer']}'\n"
    else:
        mistakes_summary = "Hata yok."

    prompt = f"""
    Sen, Perpetua adlı bir dil öğrenme uygulamasında kişisel bir AI öğretmensin. Öğrencinin adı {username}.
    {username} az önce bir alıştırmayı tamamladı. İşte performansı:

    Performans Özeti: {user_performance}
    Detaylar: {mistakes_summary}

    GÖREVLERİN:
    1. PUAN HESAPLA: Puanı (correct_answers / total_questions) * 100 formülüyle hesapla ve tam sayıya yuvarla.
    2. YORUM YAZ: {username}'a ismiyle hitap ederek, pozitif ve cesaretlendirici bir dille yorum yaz.
       - Eğer HİÇ HATA YOKSA: Onu içtenlikle tebrik et. "Harika iş, {username}! Bu turda hiç hatan olmadı, tebrikler!" gibi.
       - Eğer HATA VARSA:
         a) Sadece BİR hatasına odaklan.
         b) Hatasının nedenini basit bir gramer kuralıyla açıkla. Örneğin, sadece "'have' yerine 'has' kullan" deme. NEDENİNİ söyle: "'He', 'She' gibi özneler üçüncü tekil şahıs olduğu için fiilin sonuna '-s' takısı gelir, bu yüzden 'have' yerine 'has' kullanırız." gibi.
         c) Onu cesaretlendirerek bitir. "Ama bu harika bir denemeydi, öğrenme sürecinin bir parçası bu. Çalışmaya devam et!" gibi.
       - Klişe ifadelerden kaçın. Samimi ve kişisel bir ton kullan.

    Çıktı olarak SADECE ve SADECE aşağıdaki formatta bir JSON objesi döndür:
    {{
      "score": <hesaplanan_puan>,
      "feedback": "<{username}'a özel olarak yazdığın yorum>"
    }}
    """

    try:
        # Temperature ayarını eklemek, daha tutarlı çıktılar için iyidir.
        generation_config = genai.types.GenerationConfig(temperature=0.3)
        response = model.generate_content(prompt, generation_config=generation_config)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"AI Evaluation Error: {e}")
        return {"score": 0, "feedback": "Değerlendirme sırasında bir hata oluştu. Lütfen tekrar dene."}