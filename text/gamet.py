from dictionaries import numbers_dict
from .text_transformation import replace_digits_with_words, replace_text_with_dictionary, load_dictionary
# from text import replace_digits_with_words, replace_text_with_dictionary, load_dictionary
import re


def num_to_word(num, is_after_po=False):
    words = [
        "", "п+ерв", "втор+", "треть", "четв+ёрт", "п+ят", "шест+", "седьм+",
        "восьм+", "дев+ят", "дес+ят", "од+иннадцат", "двен+адцат", "трин+адцат", "чет+ырнадцат"
    ]
    if 1 <= num <= 14:
        if num == 3:
            return "тр+етью" if is_after_po else "тр+етьей"
        ending = "ую" if is_after_po else "ой"
        return words[num] + ending
    return str(num)


def replace_letters(text):
    return text.replace('A', 'Аа').replace('B', ' Бээ')


def transform_area(text):
    def replace_area(match):
        area = match.group(1)
        parts = area.split('-')
        if len(parts) == 1:
            items = re.findall(r'(\d+|\D+)', parts[0])
            return '. по площад+ям ' + ' '.join(
                replace_letters(num_to_word(int(item), False) + '.') if item.isdigit() else replace_letters(
                    item.strip()) + '.' for item in items if item.strip())
        else:
            start = re.findall(r'(\d+|\D+)', parts[0])
            end = re.findall(r'(\d+|\D+)', parts[1])
            start_num = int(start[0]) if start[0].isdigit() else start[0]
            end_num = int(end[0]) if end[0].isdigit() else end[0]
            start_word = num_to_word(start_num, False) if isinstance(start_num, int) else start_num
            end_word = num_to_word(end_num, True) if isinstance(end_num, int) else end_num
            return f". по площад+ям с {replace_letters(start_word)} {replace_letters(' '.join(start[1:]).strip())} по {replace_letters(end_word)} {replace_letters(' '.join(end[1:]).strip())}"

    pattern = r'\bAREA\s+([\w\s-]+?)(?=\s+(?:AREA|[A-Z]{2,}|\d{2}/\d{2}|\d{4}/\d{2}|FL\d{3}|$))'
    return re.sub(pattern, replace_area, text)


def cloud(text):
    matches_bkn = re.finditer(r'(\d{3})/(\d{3}) M AGL', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1))
        replacement = f'с н+ижней гран+ицей {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_bkn = re.finditer(r'CB (\d{3})/(\d{4}) M AGL', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1))
        cloud_data2 = int(match.group(2))
        replacement = f'к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей {cloud_data2} метр. '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'TCU (\d{3})/(\d{4}) M AGL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        cloud_data2 = int(match.group(2))
        replacement = f'м+ощно к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей {cloud_data2} метр. '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'CB (\d{3})/XXX M AGL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        replacement = f'к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей в+ыше эшел+она 100 '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'TCU (\d{3})/XXX M AGL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        replacement = f'м+ощно к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей в+ыше эшел+она 100 '
        text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def cloud2(text):
    matches_bkn = re.finditer(r'(\d{4})/(\d{4}) M AMSL', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1))
        replacement = f'с н+ижней гран+ицей {cloud_data} метр. от +уровня м+оря '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_bkn = re.finditer(r'CB (\d{4})/(\d{4}) M AMSL', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1))
        cloud_data2 = int(match.group(2))
        replacement = f'к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей {cloud_data2} метр. от +уровня м+оря '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'TCU (\d{4})/(\d{4}) M AMSL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        cloud_data2 = int(match.group(2))
        replacement = f'м+ощно к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей {cloud_data2} метр. от +уровня м+оря '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'CB (\d{4})/XXX M AMSL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        replacement = f'к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей в+ыше эшел+она 150 от +уровня м+оря '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    matches_ovc = re.finditer(r'TCU (\d{4})/XXX M AMSL', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1))
        replacement = f'м+ощно к+учево дождев+ая с н+ижней гран+ицей {cloud_data} метр. и в+ерхней гран+ицей в+ыше эшел+она 150 от +уровня м+оря '
        text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def visibility_sigmet(text):
    matches = re.finditer(r'(\d{4} M)', text)
    for match in matches:
        visibility_data = int(match.group(1)[:4])
        if not visibility_data >= 9999:
            visibility_data_word = replace_digits_with_words(str(visibility_data))
            replacement = f'в+идимость {visibility_data_word}.'
            text = re.sub(re.escape(match.group(0)), replacement, text)
        else:
            replacement = 'в+идимость б+олее десят+и килом+етров'
            text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def replace_wind_vrb(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'LCA VRB(\d{2})MPS', text)
    for match in matches:
        # Извлекаем значения
        wind_speed = int(match.group(1))

        replacement = f"лок+ально перем+енный  {wind_speed} м/с."

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text

def replace_ws(text):
    dict_digit = {
        1: 'п+ервое',
        2: 'втор+ое',
        3: 'тр+етье',
        4: 'четв+ёртое',
        5: 'п+ятое',
        6: 'шест+ое',
        7: 'седьм+ое',
        8: 'восьм+ое',
        9: 'дев+ятое'
    }
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'WS (\d) ', text)
    for match in matches:
        # Извлекаем значения
        digit = dict_digit[int(match.group(1))]

        replacement = f"д+ействует {digit} сообщ+ение сигм+ет"

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text

def replace_wind_with_impulses(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'(\d{3})/(\d{2})G(\d{2})MPS', text)

    for match in matches:
        # Извлекаем значения
        wind_direction = int(match.group(1))
        wind_speed = int(match.group(2))
        gusts_speed = int(match.group(3))

        replacement = f"в+етер {wind_direction} градус, {wind_speed}, пор+ывы {gusts_speed} м/с."

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def replace_wind_without_impulses(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'(\d{3})(\d{2})MPS', text)
    for match in matches:
        # Извлекаем значения
        wind_direction = int(match.group(1))
        wind_speed = int(match.group(2))

        replacement = f"в+етер {wind_direction} градус, {wind_speed} м/с."

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def replace_fl(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r' FL(\d{3})/(\d{3})', text)
    for match in matches:
        # Извлекаем значения
        echelon_bottom = int(match.group(1))
        echelon_top = int(match.group(2))

        replacement = f" от эшел+она {echelon_bottom} до эшел+она {echelon_top}"

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'ABV FL(\d{3}) ', text)
    for match in matches:
        # Извлекаем значения
        wind_speed = int(match.group(1))

        replacement = f" в+ыше эшел+она {wind_speed}"

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'SFC/FL(\d{3}) ', text)
    for match in matches:
        # Извлекаем значения
        wind_speed = int(match.group(1))

        replacement = f" от пов+ерхности земл+и до эшел+она {wind_speed}"

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def remove_patterns(text):
    patterns = {
        r'UNNT GAMET VALID': ' Прогн+оз Гам+ет',
        r'UNNT GAMET AMD VALID': ' Коррект+ив к прогн+озу Гам+ет',
        r'UNNT GAMET COR VALID': ' Исправл+ение к прогн+озу Гамет ',
        r'UNNT NOVOSIBIRSK FIR/TOMSK 1AB-9 BLW FL100*': 'по площад+ям с п+ервой Аа Бэ, по дев+ятую ЦэПэ+И Т+омск, н+иже эшел+она ст+о ',
        r'SECN I': ', раздел од+ин',
        r'SECN 1': ', раздел од+ин',
        r'HAZARDOUS WX NIL': 'оп+асные явл+ения пог+оды отс+утствуют',
        r'USTV TYUMEN FIR/NIZHNEVARTOVSK 1-11 BLW FL100*': 'по площад+ям с п+ервой по од+иннадцатую ЦэПэ+И Нижнев+артовск, н+иже эшелона ст+о ',
        r'USTV GAMET VALID': ' Прогн+оз Гам+ет',
        r'USTV GAMET AMD VALID': ' Коррект+ив к прогн+озу Гам+ет',
        r'USTV GAMET COR VALID': ' Исправл+ение к прогн+озу Гам+ет ',
        r'INC AND PRECIPITATION': 'в облак+ах и ос+адках',
        r'UNNT NOVOSIBIRSK FIR/TOMSK 10 11 12 13 14AB BLW FL150': 'по площад+ям с дес+ятой по чет+ырнадцатую Аа Бэ, ЦэПэ+И Т+омск, н+иже эшел+она 150 ',
        r"VAL": "в дол+инах, в низ+инах",
        r"RIVERS": "над р+еками",
        r"VILLAGES": "над деревн+ями",
        r"VAL RIVERS": "в дол+инах, в низ+инах и над р+еками",
        r"VAL VILLAGES": "в дол+инах, в низ+инах и над деревн+ями",
        r'LCA': 'лок+ально'
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()


def remove_patterns_sigwx(text):
    patterns = {
        r'ISOL TS': 'отд+ельные гр+озы',
        r'OCNL TS': 'р+едкие гр+озы',
        r'FRQ TS': 'ч+астые гр+озы',
        r'OBSC TS': 'в +облачности ',
        r'EMBD TS': 'скр+ытые гр+озы',
        r'ISOL TSGR': 'отд+ельные гр+озы с гр+адом',
        r'OCNL TSGR': 'р+едкие  гр+озы с гр+адом',
        r'FRQ TSGR': 'ч+астые  гр+озы с гр+адом',
        r'OBSC TSGR': 'в +облачности гр+озы с гр+адом',
        r'EMBD TSGR': 'скр+ытые гр+озы с гр+адом',
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()


def remove_patters_sig_cld(text):
    patterns = {
        r'ISOL CB': 'отде+льная CB',
        r'OCNL CB': 'р+едкая CB',
        r'FRQ CB': 'ч+астая CB',
        r'OBSC CB': 'в +облачности CB',
        r'EMBD CB': 'скр+ытая CB',
        r'ISOL TCU': 'отд+ельная TCU',
        r'OCNL TCU': 'р+едкая TCU',
        r'FRQ TCU': 'ч+астая TCU',
        r'OBSC TCU': 'в +облачности TCU',
        r'EMBD TCU': 'скр+ытая TCU',
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()


def transmitter_data(text, my_numbers_dict):
    # Ищем две цифры перед и после обратного слэша
    matches = re.findall(r'(\d{2})(\d{2})(\d{2})/(\d{2})(\d{2})(\d{2})', text)
    found_t = text  # Исправлено: объявляем переменную перед циклом
    for match in matches:
        # Преобразуем найденные значения в нужный формат
        start_value = str(int(match[1]))  # Убираем 0 перед числом
        end_value = str(int(match[4]))
        start_value2 = ""  # Исправлено: объявляем как строку
        end_value2 = ""  # Исправлено: объявляем как строку
        for key, value in my_numbers_dict.items():
            if key == int(start_value):
                start_value2 = value
            if key == int(end_value):
                end_value2 = value
        replacement = f'от {start_value2} до {end_value2} Z'

        # Заменяем найденную подстроку в тексте
        old_substring = match[0] + match[1] + match[2] + "/" + match[3] + match[4] + match[5]
        found_t = found_t.replace(old_substring, replacement)

    return found_t


def transmitter_hour_minute(text, my_numbers_dict):
    # Ищем две цифры перед и после обратного слэша
    matches = re.findall(r' (\d{2})(\d{2})/(\d{2}) ', text)
    found_t = text  # Исправлено: объявляем переменную перед циклом
    for match in matches:
        # Преобразуем найденные значения в нужный формат
        start_value = str(int(match[0]))  # Убираем 0 перед числом
        end_value = str(int(match[2]))
        start_value2 = ""  # Исправлено: объявляем как строку
        end_value2 = ""  # Исправлено: объявляем как строку
        for key, value in my_numbers_dict.items():
            if key == int(start_value):
                start_value2 = value
            if key == int(end_value):
                end_value2 = value
        replacement = f'от {start_value2} до {end_value2} Z'

        # Заменяем найденную подстроку в тексте
        old_substring = match[0] + match[1] + "/" + match[2]
        found_t = found_t.replace(old_substring, replacement)

    return found_t


def transmitter_hour(text, my_numbers_dict):
    # Ищем две цифры перед и после обратного слэша
    matches = re.findall(r'(\d{2})/(\d{2}) ', text)
    found_t = text  # Исправлено: объявляем переменную перед циклом
    for match in matches:
        # Преобразуем найденные значения в нужный формат
        start_value = str(int(match[0]))  # Убираем 0 перед числом
        end_value = str(int(match[1]))
        start_value2 = ""  # Исправлено: объявляем как строку
        end_value2 = ""  # Исправлено: объявляем как строку
        for key, value in my_numbers_dict.items():
            if key == int(start_value):
                start_value2 = value
            if key == int(end_value):
                end_value2 = value
        replacement = f'от {start_value2} до {end_value2} Z'

        # Заменяем найденную подстроку в тексте
        old_substring = match[0] + "/" + match[1]
        found_t = found_t.replace(old_substring, replacement)

    return found_t


# Ключевые слова для разделения
keywords = [
    "START",
    "SFC WIND:",
    "SFC VIS:",
    "SIGWX:",
    "SIG CLD:",
    "ICE:",
    "TURB:",
    "SIGMET APPLICABLE:",
    "MT OBSC:"
]


# Функция для разделения текста по ключевым словам, сохраняя весь текст
def split_text_by_keywords(text, keywords):
    # Создаем регулярное выражение для поиска ключевых слов
    pattern = '|'.join(map(re.escape, keywords))
    text = 'START' + text
    # Разбиваем текст по ключевым словам, сохраняя их в результате
    sections = re.split(f'({pattern})', text)

    # Обрабатываем разбитый текст
    result = {}
    current_key = None
    for section in sections:
        section = section.strip()  # Убираем лишние пробелы и переводы строк
        if section in keywords:
            current_key = section  # Обновляем текущий ключ
            result[current_key] = ''  # Инициализируем секцию в словаре
        elif current_key:
            # Добавляем текст в текущую секцию
            result[current_key] += section + ' '

    return result


# Полный словарь для замены погодных явлений с учетом усилителей
weather_phrases_re = {
    r"FBL BR": "слабая дымка",
    r"HVY BR": "сильная дымка",
    r"FBL DS": "слабая пыльная буря",
    r"HVY DS": "сильная пыльная буря",
    r"FBL DU": "слабая пыль",
    r"HVY DU": "сильная пыль",
    r"FBL DZ": "слабая морось",
    r"HVY DZ": "сильная морось",
    r"FBL FG": "слабый туман",
    r"HVY FG": "сильный туман",
    r"FBL FU": "слабый дым",
    r"HVY FU": "сильный дым",
    r"FBL HZ": "слабая мгла",
    r"HVY HZ": "сильная мгла",
    r"FBL RA": "слабый дождь",
    r"HVY RA": "сильный дождь",
    r"FBL SA": "слабая песчаная буря",
    r"HVY SA": "сильная песчаная буря",
    r"FBL SG": "слабые снежные зерна",
    r"HVY SG": "сильные снежные зерна",
    r"FBL SN": "слабый снег",
    r"HVY SN": "сильный снег",
    r"FBL FZFG": "слабый переохлажденный туман",
    r"HVY FZFG": "сильный переохлажденный туман",
    r"FBL FZDZ": "слабая переохлажденная морось",
    r"HVY FZDZ": "сильная переохлажденная морось",
    r"FBL FZRA": "слабый переохлажденный дождь",
    r"HVY FZRA": "сильный переохлажденный дождь",
    r"FBL SHRA": "слабый ливневый дождь",
    r"HVY SHRA": "сильный ливневый дождь",
    r"FBL SHSN": "слабый ливневый снег",
    r"HVY SHSN": "сильный ливневый снег",
    r"FBL RASN": "слабый дождь со снегом",
    r"HVY RASN": "сильный дождь со снегом",
    r"FBL SNRA": "слабый снег с дождем",
    r"HVY SNRA": "сильный снег с дождем",
    r"FBL SHRASN": "слабый ливневый дождь со снегом",
    r"HVY SHRASN": "сильный ливневый дождь со снегом",
    r"FBL SHSNRA": "слабый ливневый снег с дождем",
    r"HVY SHSNRA": "сильный ливневый снег с дождем",
    r"BR": "дымка",
    r"DS": "пыльная буря",
    r"DU": "пыль",
    r"DZ": "морось",
    r"FG": "туман",
    r"FU": "дым",
    r"HZ": "мгла",
    r"RA": "дождь",
    r"SA": "песчаная буря",
    r"SG": "снежные зерна",
    r"SN": "снег",
    r"FZFG": "переохлажденный туман",
    r"FZDZ": "переохлажденная морось",
    r"FZRA": "переохлажденный дождь",
    r"SHRA": "ливневый дождь",
    r"SHSN": "ливневый снег",
    r"RASN": "дождь со снегом",
    r"SNRA": "снег с дождем",
    r"SHRASN": "ливневый дождь со снегом",
    r"SHSNRA": "ливневый снег с дождем"
}


# Функция для перевода строки с погодными явлениями с использованием re
def translate_weather_code_with_re(weather_string):
    # Заменим каждое погодное явление из строки на его перевод по регулярному выражению
    for pattern, translation in weather_phrases_re.items():
        weather_string = re.sub(rf"\b{pattern}\b", translation, weather_string)
    return weather_string


def process_gamet_text(text_gamet: str) -> str:
    if text_gamet is not None:
        my_dict_abbreviations_and_endings = load_dictionary('./dictionaries/dict_abbreviations_and_endings.txt')
        my_dict_weather = load_dictionary('./dictionaries/dict_weather.txt')

        text_gamet = transform_area(text_gamet)
        text_gamet = remove_patterns(text_gamet)
        text_gamet = transmitter_data(text_gamet, numbers_dict)
        # print(text_gamet)

        text_gamet = split_text_by_keywords(text_gamet, keywords)
        if 'START' in text_gamet:
            text_gamet['START'] = remove_patterns(text_gamet['START'])
            text_gamet['START'] = transmitter_data(text_gamet['START'], numbers_dict)
            text_gamet['START'] = text_gamet['START'].replace('-', '')

        # расшифровка 'SFC WIND:'
        if 'SFC WIND:' in text_gamet:
            text_gamet['SFC WIND:'] = replace_wind_vrb(text_gamet['SFC WIND:'])
            text_gamet['SFC WIND:'] = transmitter_hour(text_gamet['SFC WIND:'], numbers_dict)
            text_gamet['SFC WIND:'] = transmitter_hour_minute(text_gamet['SFC WIND:'], numbers_dict)
            text_gamet['SFC WIND:'] = replace_wind_vrb(text_gamet['SFC WIND:'])
            text_gamet['SFC WIND:'] = replace_wind_with_impulses(text_gamet['SFC WIND:'])
            text_gamet['SFC WIND:'] = replace_wind_without_impulses(text_gamet['SFC WIND:'])
            text_gamet['SFC WIND:'] = 'Приз+емный в+етер: ' + text_gamet['SFC WIND:']

        # расшифровка 'SFC VIS:'
        if 'SFC VIS:' in text_gamet:
            text_gamet['SFC VIS:'] = transform_area(text_gamet['SFC VIS:'])
            text_gamet['SFC VIS:'] = translate_weather_code_with_re(text_gamet['SFC VIS:'])
            text_gamet['SFC VIS:'] = visibility_sigmet(text_gamet['SFC VIS:'])
            text_gamet['SFC VIS:'] = transmitter_hour(text_gamet['SFC VIS:'], numbers_dict)
            text_gamet['SFC VIS:'] = transmitter_hour_minute(text_gamet['SFC VIS:'], numbers_dict)
            text_gamet['SFC VIS:'] = 'В+идимость у пов+ерхности земл+и: ' + text_gamet['SFC VIS:']


        # расшифровка 'SIGWX:'
        if 'SIGWX:' in text_gamet:
            text_gamet['SIGWX:'] = remove_patterns_sigwx(text_gamet['SIGWX:'])
            text_gamet['SIGWX:'] = text_gamet['SIGWX:'].replace('HVY', 'с+ильные')
            text_gamet['SIGWX:'] = text_gamet['SIGWX:'].replace('SS', 'песч+аные б+ури')
            text_gamet['SIGWX:'] = text_gamet['SIGWX:'].replace('DS', 'п+ыльные б+ури')
            text_gamet['SIGWX:'] = 'Ос+обые явл+ения пог+оды: ' + text_gamet['SIGWX:']
        # print(text_gamet['SIGWX:'])

        # расшифровка 'SIG CLD:'
        if 'SIG CLD:' in text_gamet:
            text_gamet['SIG CLD:'] = remove_patters_sig_cld(text_gamet['SIG CLD:'])
            text_gamet['SIG CLD:'] = cloud(text_gamet['SIG CLD:'])
            text_gamet['SIG CLD:'] = cloud2(text_gamet['SIG CLD:'])
            text_gamet['SIG CLD:'] = transmitter_hour(text_gamet['SIG CLD:'], numbers_dict)
            text_gamet['SIG CLD:'] = transmitter_hour_minute(text_gamet['SIG CLD:'], numbers_dict)
            text_gamet['SIG CLD:'] = '+Облачность: ' + text_gamet['SIG CLD:']

        # расшифровка 'ICE:'
        if 'ICE:' in text_gamet:
            text_gamet['ICE:'] = transmitter_hour(text_gamet['ICE:'], numbers_dict)
            text_gamet['ICE:'] = replace_fl(text_gamet['ICE:'])
            text_gamet['ICE:'] = text_gamet['ICE:'].replace('MOD', 'ум+еренное')
            text_gamet['ICE:'] = text_gamet['ICE:'].replace('SEV', 'с+ильное')
            text_gamet['ICE:'] = 'Обледен+ение: ' + text_gamet['ICE:']

        # расшифровка 'TURB:'
        if 'TURB:' in text_gamet:
            text_gamet['TURB:'] = replace_fl(text_gamet['TURB:'])
            text_gamet['TURB:'] = text_gamet['TURB:'].replace('MOD', 'ум+еренная')
            text_gamet['TURB:'] = text_gamet['TURB:'].replace('SEV', 'с+ильная')
            text_gamet['TURB:'] = 'Турбул+ентность: ' + text_gamet['TURB:']

        # расшифровка 'SIGMET APPLICABLE:'
        if 'SIGMET APPLICABLE:' in text_gamet:
            text_gamet['SIGMET APPLICABLE:'] = replace_ws(text_gamet['SIGMET APPLICABLE:'])

        # расшифровка 'MT OBSC:'
        if 'MT OBSC:' in text_gamet:
            text_gamet['MT OBSC:'] = transmitter_hour(text_gamet['MT OBSC:'], numbers_dict)

        # Восстанавливаем весь текст с сохранением порядка и структуры
        final_text = ''
        for key, value in text_gamet.items():
            #final_text += f"{key}\n{value.strip()}\n"
            final_text += f"\n{value.strip()}\n"

        #final_text = remove_patterns2(final_text)
        final_text = replace_text_with_dictionary(final_text, my_dict_abbreviations_and_endings)
        final_text = replace_text_with_dictionary(final_text, my_dict_weather)
        final_text = replace_digits_with_words(final_text).replace('  ', ' ')
        final_text = re.sub(r'[a-zA-Z]', '', final_text)

        return final_text
