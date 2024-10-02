import configparser
import os
import shutil
import time
import win32com.client


def remove_file(pat_to_file_remove):
    try:
        os.remove(pat_to_file_remove)
    except FileNotFoundError:
        print(f"Файл {pat_to_file_remove} не найден.")
    except Exception as e:
        print(f"Ошибка при удалении файла {pat_to_file_remove}: {e}")


def check_and_create_folder(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            print(f"Ошибка при создании папки по пути '{folder_path}': {e}")
    else:
        print(f"Папка по пути '{folder_path}' уже существует.")


def clear_folder(folder_path):
    # Очищает содержимое указанной папки, удаляя все файлы и подпапки.

    try:
        # Удаляем все файлы в папке
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Удаляем все подпапки в папке
        for sub_folder_name in os.listdir(folder_path):
            sub_folder_path = os.path.join(folder_path, sub_folder_name)
            if os.path.isdir(sub_folder_path):
                shutil.rmtree(sub_folder_path)

    except Exception as e:
        print(f"Ошибка при очистке папки '{folder_path}': {e}")


def read_config(name_file: str) -> object:
    """

    :rtype: object
    """
    config = configparser.ConfigParser()
    config.read(name_file)
    #path_to_project = config['Paths']['DataPath']
    codec = config['Video']['Codec']
    scale_width = int(config['Video']['ScaleWidth'])
    scale_height = int(config['Video']['ScaleHeight'])
    num_threads = int(config['Model']['NumThreads'])
    name_model = config['Model']['NameModel']
    flag_gamet = bool(config['GAMET']['gamet'])
    return codec, scale_width, scale_height, num_threads, name_model, flag_gamet


def find_docx_and_pptm_files(folder_path):
    """
    Ищет файлы с расширениями .docx и .pptx в указанной папке.

    Возвращает:
        tuple: Путь к .docx файлу и путь к .pptx файлу.
               Если файл не найден, возвращает None.
    """
    docx_path = None
    pptx_path = None

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".docx"):
            docx_path = file_path
        elif file_name.endswith(".pptx"):
            pptx_path = file_path

    if not docx_path:
        print("Отсутствует файл .docx")
    if not pptx_path:
        print("Отсутствует файл .pptx")

    return docx_path, pptx_path


def convert_ppt_to_png(ppt_file, output_folder, scale_width=960, scale_height=540):
    """
    Конвертирует слайды PowerPoint презентации в PNG изображения.

    Параметры:
    ppt_file (str): Путь к файлу PowerPoint (.pptx).
    output_folder (str): Путь к папке, где будут сохранены изображения.
    scale_width (int, optional): Ширина изображения. По умолчанию 960.
    scale_height (int, optional): Высота изображения. По умолчанию 540.
    """
    try:
        print('Создаем объект PowerPoint')
        # Создаем объект PowerPoint
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True  # Сделать PowerPoint видимым, если нужно для отладки

        print('Открываем презентацию')
        # Открываем презентацию
        presentation = powerpoint.Presentations.Open(ppt_file, WithWindow=False)

        for i, slide in enumerate(presentation.Slides):
            # Создаем файл изображения .png для каждого слайда
            image_path = os.path.join(output_folder, f"slide_{i + 1}.png")
            slide.Export(image_path, "PNG", ScaleWidth=scale_width, ScaleHeight=scale_height)
            print(f'Слайд {i + 1} экспортирован как PNG')

        # Небольшая пауза перед закрытием PowerPoint
        time.sleep(3)
        print('Закрываем презентацию')
        presentation.Close()
        powerpoint.Quit()
        print('Конвертация завершена успешно')
    except Exception as e:
        print(f"Произошла ошибка при конвертации: {e}")
        if 'powerpoint' in locals():
            presentation.Close()
            powerpoint.Quit()


def rename_file(folder, old_name, new_name):
    try:
        file_path = os.path.join(folder, old_name)

        if os.path.exists(file_path):
            new_path = os.path.join(folder, new_name)
            os.rename(file_path, new_path)
            # print(f'File successfully renamed: {old_name} -> {new_name}')
        else:
            print(f'File not found: {old_name}')

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")

    except PermissionError as e:
        print(f"Ошибка: Недостаточно прав для переименования файла - {e}")

    except Exception as e:
        print(f"Общая ошибка при переименовании файла: {e}")
