from audio import model
from text import replace_words_in_text_in_db, process_text_3
import re



def model_transform(ssml_sample):
    try:

        # Configuration settings
        sample_rate = 48000
        speaker = 'xenia'
        put_accent = False
        put_yo = False

        # Generate and save the audio
        audio_paths = model.save_wav(ssml_text=ssml_sample,
                                     speaker=speaker,
                                     sample_rate=sample_rate,
                                     put_accent=put_accent,
                                     put_yo=put_yo)

        return audio_paths

    except Exception as e:
        print(f"An error occurred: {e}")

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")

    except Exception as e:
        print(f"Общая ошибка: {e}")

def apply_stress_marks(text):
    # Словарь с формами слова "сектор" и их ударениями
    stress_dict = {
        r"\bсектор\b": "сй+эктор",
        r"\bкроме сектора\b": "кроме сй+эктора",
        r"\bкроме  сектора\b": "кроме  сй+эктора",
        r"\bсектора\b": "сйэктор+а",
        r"\bсекторе\b": "сй+экторе",
        r"\bсектору\b": "сй+эктору",
        r"\bсектором\b": "сй+эктором",
        r"\bсекторы\b": "сй+экторы",
        r"\bсекторов\b": "сйэктор+ов",
        r"\bсекторами\b": "сйэктор+ами",
        r"\bсекторах\b": "сйэктор+ах"
    }

    # Проход по словарю и замена форм в тексте на формы с ударениями
    for pattern, stressed_form in stress_dict.items():
        text = re.sub(pattern, stressed_form, text, flags=re.IGNORECASE)

    return text

# Тестирование функции на заданном тексте
text = (
    "Сектор на стадионе был заполнен. В этом секторе собрались самые преданные болельщики. "
    "Я подошёл к сектору и увидел там своих друзей. Мы сидели в одном секторе, и у нас был отличный обзор. "
    "После игры я вышел из сектора и пошёл к выходу. По пути я заметил, что все кроме сектора начали постепенно пустеть."
"На стадионе было несколько секторов, каждый из которых был заполнен болельщиками. "
    "В этих секторах всегда царит особая атмосфера. "
    "Мы переместились между секторами, чтобы найти лучшие места. "
    "После окончания матча люди начали покидать свои сектора, и стадион постепенно опустел."
    "По сектору"
)

stressed_text = apply_stress_marks(text)
stressed_text = process_text_3(replace_words_in_text_in_db(stressed_text, 'dictionaries/orphoepy.db'))
print(stressed_text)
model_transform(stressed_text)





