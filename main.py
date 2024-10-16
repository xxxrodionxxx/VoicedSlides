from text import text_processing, remove_tags_2
from audio import audio_processing
from utils.file_utils import *
from video import video_processing
from pathlib import Path
from art import text2art
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog


def run_pro(progress_callback, progress_callback_edit, file_path_word, file_path_ppt):
    print(file_path_word, file_path_ppt)
    if check_path(file_path_ppt) and check_path(file_path_word):
        # Начало измерения времени
        progress_callback('Старт обработки')
        start_time = time.time()
        path_to_project = os.path.dirname(os.path.abspath(__file__)) + '\\'
        # Читаем конфигурационный файл
        progress_callback('Читаем конфигурационный файл')
        codec, scale_width, scale_height, num_threads, name_model, flag_gamet = read_config('config.ini')

        # Проверка и создание папок
        progress_callback('Проверка и создание папок')
        check_and_create_folder('input')
        check_and_create_folder('picture')
        check_and_create_folder('output')
        check_and_create_folder('audio/audio_file')
        clear_folder('audio/audio_file')
        # Конвертация PowerPoint в PNG изображения
        progress_callback('Конвертация PowerPoint в PNG изображения')
        file_path_ppt = Path(file_path_ppt)
        file_path_word = Path(file_path_word)

        clear_folder('picture')
        convert_ppt_to_png(file_path_ppt, path_to_project + 'picture\\', scale_width, scale_height)

        processed_texts, name_list, text_consultations = text_processing.main(file_path_word, flag_gamet=flag_gamet)
        for i in text_consultations:
            i = remove_tags_2(i)
            progress_callback_edit('       ' + i.replace('\n', ' '))

        # Преобразование текста в аудиофайлы
        progress_callback('Преобразование текста в аудиофайлы')
        # audio_processing.convert_texts_to_audio(processed_texts, name_model, name_list, path_to_project, num_threads)
        audio_paths = audio_processing.convert_texts_to_audio(processed_texts, name_list, path_to_project)

        # Объединение аудио-файлов
        audio_processing.serch_and_concatenate_wav(path_to_project + 'audio/audio_file')

        # Создаём видеофайл из картинок и аудио
        progress_callback('Создаём видеофайл из картинок и аудио')
        video_processing.video_creation('picture', 'audio/audio_file', file_path_ppt, codec)

        # Вывод на экран времени затраченного на выполнение скрипта
        end_time = time.time()
        execution_time = end_time - start_time
        message = "T h e   E n d ! ! !"
        progress_callback('Время затраченное на выполнение скрипта: ' + '  ' + f'{execution_time:.2f}'+ ' сек.')

        # ascii_art = text2art(message, font='starwars')  # Используйте 'doom' шрифт
        # progress_callback(ascii_art)
    else:
        progress_callback('Выберите пути до файлов!')

def main():
    # Начало измерения времени vv
    print('Старт обработки')
    start_time = time.time()
    path_to_project = os.path.dirname(os.path.abspath(__file__)) + '\\'
    # Читаем конфигурационный файл
    print('Читаем конфигурационный файл')
    codec, scale_width, scale_height, num_threads, name_model, flag_gamet = read_config('config.ini')

    # Проверка и создание папок
    print('Проверка и создание папок')
    check_and_create_folder('input')
    check_and_create_folder('picture')
    check_and_create_folder('output')
    check_and_create_folder('audio/audio_file')
    clear_folder('audio/audio_file')
    # Конвертация PowerPoint в PNG изображения
    print('Конвертация PowerPoint в PNG изображения')
    file_path_docx, file_path_pptx = find_docx_and_pptm_files('input')
    # file_path_ppt = Path(file_path_ppt)
    # file_path_word = Path(file_path_word)
    file_path_docx = Path(file_path_docx)
    file_path_pptx = Path(file_path_pptx)
    # print(file_path_ppt)
    # print(file_path_word)
    # print(path_to_project, file_path_docx)
    # print(path_to_project, file_path_pptx)
    clear_folder('picture')
    convert_ppt_to_png(path_to_project / file_path_pptx, path_to_project + 'picture\\', scale_width, scale_height)



    processed_texts, name_list, text_consultations = text_processing.main(file_path_docx, flag_gamet=flag_gamet)
    # for i in text_consultations:
    #     progress_callback_edit(i.replace('\n', ' '))
    # for i in text_consultations:
    #     progress_callback_edit(i)
    # print(processed_texts, name_list)

    # Преобразование текста в аудиофайлы
    print('Преобразование текста в аудиофайлы')
    # audio_processing.convert_texts_to_audio(processed_texts, name_model, name_list, path_to_project, num_threads)
    audio_paths = audio_processing.convert_texts_to_audio(processed_texts, name_list, path_to_project)

    # Объединение аудио-файлов
    audio_processing.serch_and_concatenate_wav(path_to_project + 'audio/audio_file')

    # Создаём видеофайл из картинок и аудио
    print('Создаём видеофайл из картинок и аудио')
    video_processing.video_creation('picture', 'audio/audio_file', file_path_pptx, codec)

    # Вывод на экран времени затраченного на выполнение скрипта
    end_time = time.time()
    execution_time = end_time - start_time
    message = "T h e   E n d ! ! !"
    print('Время затраченное на выполнение скрипта: ' + '  ' + f'{execution_time:.2f}'+ ' сек.')
    ascii_art = text2art(message, font='starwars')  # Используйте 'doom' шрифт

if __name__ == '__main__':
    main()
