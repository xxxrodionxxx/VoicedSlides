import textract
import sqlite3
from dictionaries import load_dictionary, numbers_dict
from .gamet import process_gamet_text
from .text_transformation import *


def split_text(text, start, end):
    start_index = text.find(start)
    if start_index == -1:
        return None  # Начальное значение не найдено
    end_index = text.find(end, start_index)
    if end_index == -1:
        return None  # Конечное значение не найдено
    return text[start_index:end_index + len(end)]


def transmitter_data(text, my_numbers_dict):
    # Ищем две цифры перед и после обратного слэша
    matches = re.findall(r'(\d{2})(\d{2})/(\d{2})(\d{2})', text)
    found_t = text  # Исправлено: объявляем переменную перед циклом
    for match in matches:
        # Преобразуем найденные значения в нужный формат
        start_value = str(int(match[1]))  # Убираем 0 перед числом
        end_value = str(int(match[3]))
        start_value2 = ""  # Исправлено: объявляем как строку
        end_value2 = ""  # Исправлено: объявляем как строку
        for key, value in my_numbers_dict.items():
            if key == int(start_value):
                start_value2 = value
            if key == int(end_value):
                end_value2 = value
        replacement = f'от {start_value2} до {end_value2} Z'

        # Заменяем найденную подстроку в тексте
        old_substring = match[0] + match[1] + "/" + match[2] + match[3]
        found_t = found_t.replace(old_substring, replacement)

    return found_t


def wind_zero(text):
    matches_bkn = re.finditer(r"Ветер на высоте круга   0 градус, 0 м/с", text)
    for match in matches_bkn:
        replacement = 'Данные о ветре на высоте круга в течение последнего часа не поступали.'
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def visibility_new(text):
    list_value = ['BECMG', 'TEMPO']
    for value in list_value:
        matches = re.finditer(fr'{value} (\d{{4}})/(\d{{4}}) (\d{{4}})\b', text)
        for match in matches:
            visibility_data = int(match.group(3))
            group1 = str(match.group(1))
            group2 = str(match.group(2))
            if not visibility_data >= 9999:
                visibility_data_word = str(visibility_data)
                replacement = f'{value} {group1}/{group2} видимость {visibility_data_word}.'
                text = re.sub(re.escape(match.group(0)), replacement, text)
            else:
                replacement = f'{value} {group1}/{group2} видимость более десяти километров'
                text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def replace_from_visibility(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'FM(\d{6}) (\d{4})\b', text)
    for match in matches:
        visibility_fm = int(match.group(2))
        time_data = int(match.group(1))
        if not visibility_fm >= 9999:
            replacement = f'FM{time_data} видимость {visibility_fm}.'
            text = re.sub(re.escape(match.group(0)), replacement, text)
        else:
            replacement = f'FM{time_data} видимость более десяти километров.'
            text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def remove_patterns_cloud(text):
    patterns = {
        r'Облачность NSC.*': 'нет существенной облачности',
        r'.*круга ТИХО.*': 'ветер на высоте круга ТИХО',
        r'.*круга VRB.*': 'ветер на высоте круга переменный',
        r'порывы 0 м/с*': '',
        r'Видимость 9999 метр.*': 'Видимость более десяти километров',
        r'метр. CB.*': 'метр. к+учево дождевая'
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()


def remove_tags(text):
    patterns = {
        r'!TAF_START!': '',
        r'!TAF_END!': '',
        r'!START!': '',
        r'!END!': '',
        r'!GAMET_START!': '',
        r'!GAMET_END!': ''
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def concatenate_texts(*texts):
    concatenated_text = ""
    for text in texts:
        concatenated_text += text
    return remove_tags(concatenated_text)


def split_text_by_tags(text):
    try:
        text_list_split = []
        tag_list_split = []
        current_tag = None
        current_content = ""

        has_tags = False  # Переменная для отслеживания наличия тегов

        for line in text.split('\n'):
            if line.startswith("<") and line.endswith(">"):
                # Завершаем предыдущий тег, если он был
                if current_tag is not None:
                    tag_list_split.append(current_tag)
                    text_list_split.append(current_content.strip())
                    current_content = ""

                # Начинаем новый тег
                current_tag = line.strip("<>").strip()

                # Помечаем, что найдены теги
                has_tags = True
            else:
                # Продолжаем собирать содержимое текущего тега
                current_content += line + "\n"

        # Добавляем последний тег в списки
        if current_tag is not None:
            tag_list_split.append(current_tag)
            text_list_split.append(current_content.strip())

        # Проверяем наличие тегов и выводим сообщение, если их нет
        if not has_tags:
            print("Ошибка! В тексте отсутствуют теги для разделения аудио на слайды!")

        return tag_list_split, text_list_split

    except Exception as e:
        print(f"Общая ошибка при разделении текста по тегам: {e}")
        return None, None  # или другой способ обработки ошибки


def separate_text(example_text):
    # Разделение текста на предложения по запятой или точке
    sentences = []
    current_sentence = ""
    for char in example_text:
        current_sentence += char
        if 700 <= len(current_sentence) <= 999 and (char == ',' or char == '.'):
            sentences.append(current_sentence)
            current_sentence = ""
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


def process_text_list(text_list):
    """
    Если разделённый текст имеет больше 1000 знаков, то он делится на части,
    преобразование цифровых значений в слова
    """
    list_list = []
    name_list = []

    for i in range(len(text_list)):
        if len(text_list[i]) >= 999:
            separate_list = separate_text(text_list[i])
            for k, text in enumerate(separate_list):
                list_list.append(text)
                name_list.append(f'sep{k}_audio{i}')
        else:
            list_list.append(text_list[i])
            name_list.append(f'audio{i}')

    return list_list, name_list


def replace_words_in_text(text, dictionary):
    try:
        words = re.findall(r'\b\w+\b|\W', text)
        for i in range(len(words)):
            if words[i].isalpha():
                word = words[i].lower()
                if word in dictionary and '+' not in word:
                    words[i] = dictionary[word]
        return ''.join(words)

    except Exception as e:
        print(f"Общая ошибка при замене слов в тексте: {e}")
        return None


def replace_words_in_text_in_db(text, path_to_db):
    try:
        words = re.findall(r'\b\w+\b|\W', text)
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        for i in range(len(words)):
            if words[i].isalpha():
                word = words[i].lower()
                cursor.execute("SELECT value FROM dict WHERE key = ?", (word,))
                result = cursor.fetchone()
                if result:
                    words[i] = result[0]
        return ''.join(words)
    except Exception as e:
        print(f"Общая ошибка при замене слов в тексте: {e}")
        return None
    finally:
        if 'conn' in locals() or 'conn' in globals():
            conn.close()


def process_and_transform_text(list_list, my_dictionary):
    processed_texts = []
    for text in list_list:
        output_text = process_text_3(replace_words_in_text_in_db(text, my_dictionary))
        processed_texts.append(output_text)
    return processed_texts


def process_text_3(input_text: object) -> object:
    if input_text is not None:
        # Разбиваем текст на параграфы
        paragraphs = input_text.split('\n')

        # Добавляем теги к каждому параграфу
        processed_paragraphs = ['<p>' + paragraph + '</p>' for paragraph in paragraphs]

        # Собираем обработанные параграфы обратно в текст
        processed_text = '\n'.join(processed_paragraphs)

        # Добавляем теги speak в начало и конец текста
        processed_text = '<speak>' + processed_text + '</speak>'

        return processed_text
    else:
        raise Exception('!!!!')


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


def manipulate_text(text, start_marker: str, end_marker: str, function):

    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index == -1 or end_index == -1 or start_index >= end_index:
        # Если маркеры не найдены или расположены неправильно, возвращаем исходный текст
        return text

    # Индексы начала и конца содержимого между маркерами
    content_start = start_index + len(start_marker)
    content_end = end_index

    # Извлекаем текст между маркерами
    content = text[content_start:content_end]

    # Здесь проводим необходимые манипуляции с контентом
    manipulated_content = function(content)  # Пример: переводим в верхний регистр

    # Собираем новый текст
    new_text = (
            text[:content_start] +
            manipulated_content +
            text[content_end:]
    )

    return new_text


def main(file_path_docx, flag_gamet=False):
    # Загружаем словари
    # flag_gamet = True
    my_dict_abbreviations_and_endings = load_dictionary('./dictionaries/dict_abbreviations_and_endings.txt')
    my_dict_weather = load_dictionary('./dictionaries/dict_weather.txt')
    # Читаем текст из .docx файла
    docx_text = textract.process(file_path_docx)
    text_consultations = docx_text.decode("utf-8")
    # расставляем ударения в различных склонениях слова "сектор"
    text_consultations = apply_stress_marks(text_consultations)
    # Разделяем текст на части
    if not flag_gamet:
        start_text = split_text(text_consultations, '!START!', '!TAF_START!')
        end_text = split_text(text_consultations, '!TAF_END!', '!END!')
        taf_text = split_text(text_consultations, '!TAF_START!', '!TAF_END!')
        # Преобразуем текст в формат TAF в текст
        taf_text_new = transmitter_taf(taf_text)
        # Обрабатываем текст до 'Прогноз по аэродрому Толмачёво'
        processed_visibility = visibility_new(start_text)
        replaced_from_visibility = replace_from_visibility(processed_visibility)
        cloud_data = cloud(replace_from(replaced_from_visibility, numbers_dict))
        cloud2_data = cloud2(cloud_data)
        cloud3_data = cloud3(cloud2_data)
        wind_data = wind(cloud3_data)
        result_1 = transmitter_data(wind_data, numbers_dict)

        result_2 = wind_zero(remove_patterns_cloud(end_text))

        text_consultations_new = concatenate_texts(result_1, taf_text_new, result_2)
    else:
        start_text = split_text(text_consultations, '!START!', '!GAMET_ONE_START!')
        end_text = split_text(text_consultations, '!TAF_END!', '!END!')
        print(end_text)
        taf_and_gamet_text = split_text(text_consultations, '!GAMET_ONE_START!', '!TAF_END!')
        # Преобразуем текст в формат TAF в текст
        taf_and_gamet_text = manipulate_text(taf_and_gamet_text, '!TAF_START!', '!TAF_END!', transmitter_taf)
        taf_and_gamet_text = manipulate_text(taf_and_gamet_text, '!GAMET_ONE_START!', '!GAMET_ONE_END!', process_gamet_text)
        taf_and_gamet_text = manipulate_text(taf_and_gamet_text, '!GAMET_TWO_START!', '!GAMET_TWO_END!', process_gamet_text)
        # Обрабатываем текст до 'Прогноз по аэродрому Толмачёво'
        start_text = visibility_new(start_text)
        start_text = replace_from_visibility(start_text)
        start_text = cloud(replace_from(start_text, numbers_dict))
        start_text = cloud2(start_text)
        start_text = cloud3(start_text)
        start_text = wind(start_text)
        start_text = transmitter_data(start_text, numbers_dict)

        end_text = wind_zero(remove_patterns_cloud(end_text))

        text_consultations_new = concatenate_texts(start_text, taf_and_gamet_text, end_text)

    text_consultations_new_2 = replace_text_with_dictionary(replace_text_with_dictionary(
        text_consultations_new, my_dict_abbreviations_and_endings), my_dict_weather)

    tag_list, text_list_2 = split_text_by_tags(text_consultations_new_2)

    text_list = [replace_digits_with_words(text) for text in text_list_2]

    list_list, name_list = process_text_list(text_list)
    # Расстановка ударений и тегов для нейросети
    processed_texts = process_and_transform_text(list_list, 'dictionaries\orphoepy.db')

    return processed_texts, name_list
