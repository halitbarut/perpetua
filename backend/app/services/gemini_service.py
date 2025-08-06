from typing import List

import google.generativeai as genai
from app.core.config import settings
import json
import random

from app.db.models.user_mistake import UserMistake

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def _get_prompt_for_exercise(exercise_type: str, level: str):
    """Alıştırma tipine göre doğru AI prompt'unu döndürür."""
    if exercise_type == "grammar":
        return f"""
            Sen, {level} seviyesinde İngilizce öğreten bir yapay zekasın.
            Görevin, {level} seviyesi için "cümle tamamlama" formatında 5 adet gramer sorusu oluşturmak.
            Her soru, içinde '___' bulunan bir cümle ve bu boşluğa gelebilecek kelimelerden oluşan bir kelime bankası içermelidir.

            KURALLAR:
            1. Toplam 5 adet soru nesnesi oluştur.
            2. Her soru için 4 kelimelik bir kelime bankası oluştur (1 doğru, 3 yanlış).
            3. ÇOK ÖNEMLİ: Her bir soru nesnesinin içine, `"type": "grammar"` alanını MUTLAKA ekle. Bu alan zorunludur.
            4. Çıktı olarak SADECE ve SADECE bir JSON objesi döndür. Bu obje, "questions" adında bir anahtar ve bu 5 soru nesnesini içeren bir liste barındırmalıdır.

            ÖRNEK ÇIKTI FORMATI:
        {{
          "questions": [
            {{
              "type": "grammar",
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

    if exercise_type == "dialogue":
        return f"""
        Sen, {level} seviyesinde İngilizce öğreten bir yapay zekasın.
        Görevin, {level} seviyesi için "diyalog tamamlama" formatında 5 ADET FARKLI soru oluşturmak.

        KURALLAR:
        1. Birbirinden bağımsız, 5 adet diyalog sorusu oluştur.
        2. Her soru için, iki kişi arasında geçen 2-3 satırlık basit bir diyalog oluştur. Diyalogun son cümlesi eksik olmalı.
        3. Her soru için 4 adet mantıklı seçenek (1 doğru, 3 yanlış) üret.
        4. Çıktı olarak SADECE ve SADECE bir JSON objesi döndür.
        5. ÇOK ÖNEMLİ: "dialogue" alanı, her biri "speaker" ve "line" anahtarlarına sahip SÖZLÜKLERDEN (dictionary/object) oluşan bir LİSTE olmalıdır. BASİT METİN LİSTESİ (list of strings) KESİNLİKLE KULLANMA.

        ÖRNEK ÇIKTI FORMATI (BU FORMATA TAM OLARAK UYMALISIN):
        {{
          "questions": [
            {{
              "type": "dialogue",
              "dialogue": [
                {{"speaker": "Shopkeeper", "line": "Hello, can I help you?"}},
                {{"speaker": "Customer", "line": "Yes, please. I'd like an apple."}}
              ],
              "question": "What should the shopkeeper say next?",
              "options": [
                "Here you are.",
                "I am a doctor.",
                "My name is John.",
                "Thank you."
              ],
              "correct_answer": "Here you are."
            }}
          ]
        }}

        Şimdi {level} seviyesi için, yukarıdaki kurallara ve formata HARFİYEN uyarak 5 diyalog sorusu içeren listeyi oluştur.
        """

    if exercise_type == "word_matching":
        topics = ["Fruits", "Animals", "Family Members", "Colors", "Jobs", "Food", "Clothes"]
        chosen_topics = random.sample(topics, 5)

        return f"""
        Sen, {level} seviyesinde İngilizce öğreten bir yapay zekasın.
        Görevin, {level} seviyesi için "kelime eşleştirme" formatında 5 ADET FARKLI set oluşturmak.

        KURALLAR:
        1. Sırasıyla şu konular için setler oluştur: {', '.join(chosen_topics)}.
        2. Her konu için 4 adet basit İngilizce kelime ve Türkçe karşılıklarını bul.
        3. ÇOK ÖNEMLİ: Çıktı olarak, "words" ve "meanings" listelerini BİRBİRİNDEN FARKLI, yani tamamen karışık sıralarda ver.
        4. Ek olarak, "correct_pairs" adında bir SÖZLÜK (dictionary/object) oluştur. Bu sözlükte anahtar (key) İngilizce kelime, değer (value) ise onun doğru Türkçe karşılığı olmalıdır.
        5. Çıktı olarak SADECE ve SADECE bir JSON objesi döndür.

        ÖRNEK ÇIKTI FORMATI:
        {{
          "questions": [
            {{
              "type": "word_matching",
              "topic": "Fruits",
              "words": ["Apple", "Banana", "Orange", "Grape"],
              "meanings": ["Muz", "Portakal", "Elma", "Üzüm"],
              "correct_pairs": {{
                "Apple": "Elma",
                "Banana": "Muz",
                "Orange": "Portakal",
                "Grape": "Üzüm"
              }}
            }}
          ]
        }}

        Şimdi belirtilen konular için, {level} seviyesinde "correct_pairs" cevap anahtarını da içeren 5 kelime eşleştirme seti oluştur.
        """

    return None


def create_exercise_from_ai(exercise_type: str, user_level: str):
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

        - Nihai Puanı: {results['final_score']}
        - Toplam Hamle Sayısı: {results['total_questions']}
        - Doğru Hamle Sayısı: {results['correct_answers']}
        - Yaptığı spesifik hatalar: {results['wrong_answers'] if results['wrong_answers'] else 'Yok.'}

        GÖREVİN:
        Bu performansa göre, {username}'a ismiyle hitap ederek, pozitif ve cesaretlendirici bir dille, 1-2 cümlelik kişisel bir yorum yaz.
        - Eğer puanı yüksekse (örn: 80 üzeri), hızını ve doğruluğunu öv.
        - Eğer puanı ortalamaysa, iyi çabasını takdir et ve hangi konularda zorlandığını nazikçe belirt.
        - Eğer puanı düşükse, bunun öğrenmenin bir parçası olduğunu vurgula ve moralini yüksek tutması için cesaretlendir.
        - Yaptığı spesifik bir hataya (eğer varsa) odaklanarak, neden yanlış olduğunu kısaca açıkla.

        Çıktı olarak SADECE ve SADECE aşağıdaki formatta bir JSON objesi döndür. Puanı TEKRAR HESAPLAMA, sana verilen puanı kullan:
        {{
          "score": {results['final_score']},
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


def generate_feedback_from_mistakes(mistakes: List[UserMistake], username: str):
    """
    Kullanıcının hatalarından yola çıkarak kişisel bir tavsiye metni üretir.
    """
    if not mistakes:
        return f"Harika gidiyorsun {username}! Son alıştırmalarında hiç hatan yok. Bu harika seriyi devam ettir."

    mistakes_summary = "\n".join(
        [f"- Soru: '{m.question_text}', Yanlış Cevap: '{m.user_answer}', Doğru Cevap: '{m.correct_answer}'" for m in
         mistakes]
    )


    prompt = f"""
    Sen, Perpetua adlı bir dil öğrenme uygulamasında kişisel ve pozitif bir AI koçusun. Öğrencinin adı {username}.
    Aşağıda, {username}'ın son zamanlarda yaptığı bazı hatalar listeleniyor:

    {mistakes_summary}

    GÖREVİN:
    Bu hatalara genel olarak bakarak, {username}'a yönelik 1-2 cümlelik, kısa, samimi ve motive edici bir tavsiye yaz.
    - Belirli bir gramer kuralında mı zorlanıyor? (örn: 'is/are' kullanımı)
    - Yoksa kelime eşleştirmede mi zorlanıyor?
    - Genel bir tavsiye ver. Örneğin: "Merhaba {username}, 'is' ve 'are' kullanımında biraz zorlandığını fark ettim. Unutma, tekil öznelerle 'is', çoğul öznelerle 'are' kullanırız. Pratik yapmaya devam, çok iyi gidiyorsun!"
    - Asla yargılayıcı veya negatif olma. Her zaman cesaretlendirici ol.

    Şimdi bu tavsiye metnini oluştur. Sadece metni döndür, başka hiçbir şey ekleme.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"')
    except Exception as e:
        print(f"AI Feedback Error: {e}")
        return "Bugün senin için özel bir tavsiye hazırlayamadım, ama harika gittiğini biliyorum!"
