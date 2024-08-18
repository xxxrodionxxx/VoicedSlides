import text_processing
import audio_processing
from file_utils import *
import video_processing
from art import text2art


def main():
    start_time = time.time()
    path_to_project = os.path.dirname(os.path.abspath(__file__)) + '\\'
    # Читаем конфигурационный файл
    codec, scale_width, scale_height, num_threads, name_model = read_config('config.ini')

    # Проверка и создание папок
    check_and_create_folder('output')
    check_and_create_folder('audio_file')
    clear_folder('audio_file')

    # Конвертация PowerPoint в PNG изображения
    file_path_docx, file_path_pptx = find_docx_and_pptm_files('input')
    clear_folder('picture')
    convert_ppt_to_png(path_to_project + file_path_pptx, path_to_project + 'picture\\', scale_width, scale_height)

    # Преобразование текста в аудиофайлы

    processed_texts, name_list = text_processing.main(file_path_docx)
    print(processed_texts, name_list)

    # Преобразование текста в аудиофайлы
    # audio_processing.convert_texts_to_audio(processed_texts, name_model, name_list, path_to_project, num_threads)
    audio_paths = audio_processing.convert_texts_to_audio(processed_texts, name_list, path_to_project)

    # Объединение аудио-файлов
    audio_processing.serch_and_concatenate_wav(path_to_project + 'audio_file\\')

    # Создаём видеофайл из картинок и аудио
    video_processing.video_creation('picture', 'audio_file', file_path_pptx, codec)

    # Вывод на экран времени затраченного на выполнение скрипта
    end_time = time.time()
    execution_time = end_time - start_time
    print('Время затраченное на выполнение скрипта: ' + str(execution_time))
    message = "T h e   E n d ! ! !"
    ascii_art = text2art(message, font='starwars')  # Используйте 'doom' шрифт
    print(ascii_art)


if __name__ == '__main__':
    main()
