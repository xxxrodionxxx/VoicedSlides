import sqlite3
from line_profiler_pycharm import profile
import re
import os


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


def create_db():
    my_dict = load_dictionary('dictionaries\orthoepy.dic')
    # print(*my_dict)

    # Создать базу данных
    conn = sqlite3.connect('dictionaries\orphoepy.db')
    cursor = conn.cursor()
    # Создать таблицу
    cursor.execute('''CREATE TABLE IF NOT EXISTS dict
      (key TEXT,
      value TEXT)''')

    # Записать данные в таблицу
    for key, value in my_dict.items():
        cursor.execute("INSERT INTO dict VALUES (?, ?)", (key, value))
    # Сохранить изменения
    conn.commit()

    # Закрыть соединение
    conn.close()


def create_index():
    conn = sqlite3.connect('dictionaries\orphoepy.db')
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_key ON dict (key)")
    conn.commit()
    conn.close()


# Поиск ключа в базе данных
@profile
def search_db(key):
    conn = sqlite3.connect('dictionaries\orphoepy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM dict WHERE key = ?", (key,))
    result = cursor.fetchone()
    if result:
        result = result[0]
    conn.close()
    return result


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
        conn.close()


def add_word_in_db(key, value, path_to_db):
    try:
        conn = sqlite3.connect(path_to_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dict VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Общая ошибка при добавлении слова в базу данных: {e}")


def print_db():
    conn = sqlite3.connect('dictionaries\orphoepy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dict")
    result = cursor.fetchall()
    conn.close()
    return result


@profile
def map_serch_dict(key, dict):
    result = dict.get(key)
    return result


if __name__ == '__main__':
    # создание базы данных
    if not os.path.exists('dictionaries\orphoepy.db'):
        try:
            create_db()
            create_index()
            print("База данных создана")
        except Exception as e:
            print(f"Общая ошибка при создании базы данных: {e}")
    dict_word = {}
    dict_word.update({
        "метров": "м+етров",
        "ветра": "в+етра",
        "слабо": "сл+або",
        "нестеренко": "нестер+енко",
        "козина": "к+озина",
        "худякова": "худяк+ова",
        "федченко": "ф+едченко",
        "астанкова": "астанк+ова",
        "титовская": "тит+овская",
        "гапоненко": "гап+оненко",
        "ефремова": "ефр+емова",
        "шабанова": "шаб+анова",
        "симбирева": "симбир+ёва",
        "симбирёва": "симбир+ёва",
        "сазонова": "саз+онова",
        "черниговская": "черн+иговская",
        "мордус": "м+ордус",
        "залетило": "залет+ило",
        "михайлова": "мих+айлова",
        "горно-алтайск": "г+орно алт+айск",
        "лаврентьева": "лавр+ентьева",
        "барабинск": "бар+абинск",
        "колпашево": "колп+ашево",
        "радиозонд": "радиоз+онд",
        "стрежевой": "стрежев+ой",
        "стрежевом": "стрежев+ом",
        "волнами": "в+олнами",
        "астаны": "астан+ы",
        "астана": "астан+а",
        "приземных": "приз+емных",
        "приземного": "приз+емного",
        "кучево": "к+учево",
        "дождевая": "дождев+ая",
        "пирогова": "пирог+ова",
        "бычкова": "бычк+ова",
        "зубова": "з+убова",
        "лалетина": "лалетина",
        "стальнова": "стальн+ова",
        "ламбрехт": "л+амбрехт",
        "завьялова": "завь+ялова",
        "жохова": "ж+охова",
        "стрежевского": "стрежевск+ого"
    })
    for key, value in dict_word.items():
        add_word_in_db(key, value, 'dictionaries\orphoepy.db')