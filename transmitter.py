import re
from num2words import num2words
from dictionaries_processing import numbers_dict, numbers_dict2, numbers_dict_date


def replace_text_with_dictionary(text, my_dict):
    sorted_keys = sorted(my_dict.keys(), key=len, reverse=True)
    for key in sorted_keys:
        value = my_dict[key]
        pattern = re.compile(re.escape(key), re.IGNORECASE)
        text = pattern.sub(value, text)
    return text


def replace_digits_with_words(input_string):
    result = ''
    current_number = ''

    try:
        for char in input_string:
            if char.isdigit():
                current_number += char
            else:
                if current_number:
                    result += num2words(int(current_number), lang='ru') + ' '
                    current_number = ''
                result += char

        if current_number:
            result += num2words(int(current_number), lang='ru')

        return result.strip()

    except ValueError as e:
        print(f"Ошибка при конвертации числа в слова: {e}")
        return None


def load_dictionary(file_path):
    try:
        my_dict = {}
        with open(file_path, 'r', encoding='ansi') as file:
            data = file.read()

        # Разделяем строки по символу '=' и записываем в словарь
        for line in data.split('\n'):
            if '=' in line:
                key, value = line.split('=')
                my_dict[key.strip()] = value.strip()

        return my_dict

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None

    except Exception as e:
        print(f"Общая ошибка при загрузке словаря: {e}")
        return None


def process_and_replace(text, start, end, numbers_dict):
    # Находим подстроку между start и end
    match = re.search(f'{re.escape(start)}(.*?){re.escape(end)}', text)
    if match:
        # Извлекаем текст между start и end
        found_text = match.group(1)
        # Ищем две цифры перед и после обратного слэша
        matches = re.findall(r'(\d{2})(\d{2})/(\d{2})(\d{2})', found_text)
        found_t = found_text  # Исправлено: объявляем переменную перед циклом
        for match in matches:
            # Преобразуем найденные значения в нужный формат
            start_value = str(int(match[1]))  # Убираем 0 перед числом
            end_value = str(int(match[3]))
            start_value2 = ""  # Исправлено: объявляем как строку
            end_value2 = ""  # Исправлено: объявляем как строку
            for key, value in numbers_dict.items():
                if key == int(start_value):
                    start_value2 = value
                if key == int(end_value):
                    end_value2 = value
            replacement = f'с {start_value2} до {end_value2} Z'

            # Заменяем найденную подстроку в тексте
            old_substring = match[0] + match[1] + "/" + match[2] + match[3]
            found_t = found_t.replace(old_substring, replacement)
        return found_t

    else:
        print(f'Не найден текст: {start}')
        return None


def process_and_replace2(text, numbers_dict):
    # Ищем две цифры перед и после обратного слэша
    matches = re.findall(r'(\d{2})(\d{2})/(\d{2})(\d{2})', text)
    found_t = text  # Исправлено: объявляем переменную перед циклом
    for match in matches:
        # Преобразуем найденные значения в нужный формат
        start_value = str(int(match[1]))  # Убираем 0 перед числом
        end_value = str(int(match[3]))
        start_value2 = ""  # Исправлено: объявляем как строку
        end_value2 = ""  # Исправлено: объявляем как строку
        for key, value in numbers_dict.items():
            if key == int(start_value):
                start_value2 = value
            if key == int(end_value):
                end_value2 = value
        replacement = f'с {start_value2} до {end_value2} Z'

        # Заменяем найденную подстроку в тексте
        old_substring = match[0] + match[1] + "/" + match[2] + match[3]
        found_t = found_t.replace(old_substring, replacement)
    return found_t


def process_and_replace_wind_data(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'(\d{3})(\d{2})G(\d{2})MPS', text)

    for match in matches:
        # Извлекаем значения
        wind_direction = int(match.group(1))
        wind_speed = int(match.group(2))
        gusts_speed = int(match.group(3))

        replacement = f"в+етер {wind_direction} градус, {wind_speed}, пор+ывы {gusts_speed} м/с."

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def process_and_replace_wind_data2(text):
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


def process_and_replace_wind_data3(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'VRB(\d{2})MPS', text)
    for match in matches:
        # Извлекаем значения
        wind_speed = int(match.group(1))

        replacement = f"в+етер неуст+ойчивый {wind_speed} м/с."

        # Заменяем найденную подстроку в тексте
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def wind(text):
    result = process_and_replace_wind_data3(process_and_replace_wind_data2(process_and_replace_wind_data(text)))
    return result


def replace_temp(text, numbers_dict_date, numbers_dict):
    word_replacements = {
        "11 градус,": "11 градусов",
        "12 градус,": "12 градусов",
        "13 градус,": "13 градусов",
        "14 градус,": "14 градусов",
        "0 градус,": "0 градусов",
        "1 градус,": "1 градус",
        "2 градус,": "2 градуса",
        "3 градус,": "3 градуса",
        "4 градус,": "4 градуса",
        "5 градус,": "5 градусов",
        "6 градус,": "6 градусов",
        "7 градус,": "7 градусов",
        "8 градус,": "8 градусов",
        "9 градус,": "9 градусов"
    }
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'T([XN])M(\d{2})/(\d{2})(\d{2})Z', text)
    for match in matches:
        max_min = match.group(1)
        temperature = int(match.group(2))
        date = int(match.group(3))
        time = int(match.group(4))
        for key, value in numbers_dict_date.items():
            if key == date:
                date = value
        for key_2, value_2 in numbers_dict.items():
            if key_2 == time:
                time = value_2
        if max_min == 'X':
            max_min = 'максим+альная'
        elif max_min == 'N':
            max_min = 'миним+альная'
        else:
            max_min = ''

        temperature_degrees = f'{temperature} градус,'
        temperature_degrees = replace_text_with_dictionary(temperature_degrees, word_replacements)
        temperature_degrees = replace_digits_with_words(str(temperature_degrees))

        replacement = f'{max_min} температ+ура м+инус {temperature_degrees}, в {time} Z {date}. '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def replace_temp2(text, numbers_dict_date, numbers_dict):
    word_replacements = {
        "11 градус,": "11 градусов",
        "12 градус,": "12 градусов",
        "13 градус,": "13 градусов",
        "14 градус,": "14 градусов",
        "0 градус,": "0 градусов",
        "1 градус,": "1 градус",
        "2 градус,": "2 градуса",
        "3 градус,": "3 градуса",
        "4 градус,": "4 градуса",
        "5 градус,": "5 градусов",
        "6 градус,": "6 градусов",
        "7 градус,": "7 градусов",
        "8 градус,": "8 градусов",
        "9 градус,": "9 градусов"
    }
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'T([XN])(\d{2})/(\d{2})(\d{2})Z', text)
    for match in matches:
        max_min = match.group(1)
        temperature = int(match.group(2))
        date = int(match.group(3))
        time = int(match.group(4))
        for key, value in numbers_dict_date.items():
            if key == date:
                date = value
        for key_2, value_2 in numbers_dict.items():
            if key_2 == time:
                time = value_2
        if max_min == 'X':
            max_min = 'максим+альная'
        elif max_min == 'N':
            max_min = 'миним+альная'
        else:
            max_min = ''

        temperature_degrees = f'{temperature} градус,'
        temperature_degrees = replace_text_with_dictionary(temperature_degrees, word_replacements)
        temperature_degrees = replace_digits_with_words(str(temperature_degrees))
        replacement = f'{max_min} температ+ура {temperature_degrees}, в {time} Z {date}. '
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def replace_from(text, numbers_dict):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'FM(\d{2})(\d{2})(\d{2})', text)
    for match in matches:
        time = int(match.group(2))
        for key, value in numbers_dict.items():
            if key == time:
                time = value
        replacement = f'С {time} Z.'
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def replace_storm(text):
    # Ищем все значения с MPS в тексте
    matches = re.finditer(r'PROB(\d{2})', text)
    for match in matches:
        percentage = int(match.group(1))
        replacement = f'с веро+ятностью  {percentage} проц+ентов.'
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def visibility(text):
    matches = re.finditer(r'(\d{4})', text)
    for match in matches:
        visibility_data = int(match.group(1))
        if not visibility_data >= 9999:
            visibility_data_word = replace_digits_with_words(str(visibility_data))
            replacement = f'в+идимость {visibility_data_word}.'
            text = re.sub(re.escape(match.group(0)), replacement, text)
        else:
            replacement = 'видимость более десяти километров'
            text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def cloud(text):
    matches_bkn = re.finditer(r'BKN(\d{3})CB', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1)) * 30
        replacement = f'знач+ительная к+учево дождев+ая +облачность на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_ovc = re.finditer(r'OVC(\d{3})CB', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1)) * 30
        replacement = f'сплошн+ая к+учево дождев+ая +облачность на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_sct = re.finditer(r'SCT(\d{3})CB', text)
    for match in matches_sct:
        cloud_data = int(match.group(1)) * 30
        replacement = f'разбр+осанная к+учево дождев+ая +облачность на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_few = re.finditer(r'FEW(\d{3})CB', text)
    for match in matches_few:
        cloud_data = int(match.group(1)) * 30
        replacement = f'не знач+ительная к+учево дождев+ая +облачность на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def cloud2(text):
    matches_bkn = re.finditer(r'BKN(\d{3})', text)
    for match in matches_bkn:
        cloud_data = int(match.group(1)) * 30
        replacement = f'+облачность знач+ительная на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_ovc = re.finditer(r'OVC(\d{3})', text)
    for match in matches_ovc:
        cloud_data = int(match.group(1)) * 30
        replacement = f'+облачность сплошн+ая на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_sct = re.finditer(r'SCT(\d{3})', text)
    for match in matches_sct:
        cloud_data = int(match.group(1)) * 30
        replacement = f'+облачность разбр+осанная на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    matches_few = re.finditer(r'FEW(\d{3})', text)
    for match in matches_few:
        cloud_data = int(match.group(1)) * 30
        replacement = f'+облачность не знач+ительная на {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)
    return text


def cloud3(text):
    matches_bkn = re.finditer(r"VV(\d{3})", text)
    for match in matches_bkn:
        cloud_data = int(match.group(1)) * 30
        replacement = f'вертикальная видимость {cloud_data} метр.'
        text = re.sub(re.escape(match.group(0)), replacement, text)

    return text


def transmitter_taf(text):
    # Пример использования                             # BECMG постепенно
    # text = 'Прогноз по аэродрому Толмачёво SHSN 1212/5613  25003G08MPS 25003MPS 8000 -SN BKN016CB SCT004 OVC010 BECMG 1614/1618 21003G08MPS ' \
    #        'TEMPO 1621/1709 3000 -SN BECMG 1703/1707 25005G10MPS TX04/1915Z TNM04/1911Z VRB01MPS FM171500 PROB30 VV040='
    start = 'Прогноз по аэродрому Толмачёво'
    end = '='
    my_dict = load_dictionary(r'dictionaries\dict_weather.txt')

    start_text_end = process_and_replace(text, start, end, numbers_dict)
    result = replace_storm(cloud3(cloud2(cloud(visibility(
        replace_from(replace_temp2(replace_temp(process_and_replace_wind_data3(process_and_replace_wind_data2(
            process_and_replace_wind_data(start_text_end))), numbers_dict_date,
            numbers_dict2),
            numbers_dict_date, numbers_dict2), numbers_dict))))))

    result = replace_text_with_dictionary(result, my_dict)

    return result
