from utils.file_utils import rename_file
import torch
import wave
import os
from utils.file_utils import remove_file

from concurrent.futures import ThreadPoolExecutor


def find_wav_files_with_prefix(folder_path, prefix="sep"):
    try:
        result_files = []

        # Проверяем, существует ли указанная папка
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует.")
            return result_files

        # Получаем список файлов в указанной папке
        files = os.listdir(folder_path)

        # Фильтруем файлы с расширением .wav и начинающиеся с указанного префикса
        for file in files:
            if file.endswith(".wav") and file.startswith(prefix):
                result_files.append(os.path.join(folder_path, file))

        return result_files

    except Exception as e:
        print(f"Общая ошибка при поиске файлов: {e}")
        return None


def concatenate_wav_files(input_files, output_file):
    try:
        with wave.open(output_file, 'wb') as output_wav:
            for input_file in input_files:
                with wave.open(input_file, 'rb') as input_wav:
                    if not output_wav.getnframes():
                        output_wav.setparams(input_wav.getparams())
                    output_wav.writeframes(input_wav.readframes(input_wav.getnframes()))

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")

    except wave.Error as e:
        print(f"Ошибка при работе с файлом WAV: {e}")

    except Exception as e:
        print(f"Общая ошибка при объединении WAV-файлов: {e}")


def serch_and_concatenate_wav(path_to_wav):
    input_wav_files = find_wav_files_with_prefix(path_to_wav)
    file_list = []
    for name_file_wav in enumerate(input_wav_files):
        file_list.append(os.path.basename(name_file_wav[1]))
    result_dict = {}

    for file_name in file_list:
        # Разбиваем строку по символу '_' и берем второй элемент (после знака '_')
        key = file_name.split('_')[1]
        # Проверяем, есть ли уже такой ключ в словаре
        if key in result_dict:
            # Если есть, добавляем текущий файл к соответствующему массиву
            result_dict[key].append(file_name)
        else:
            # Если нет, создаем новый массив с текущим файлом
            result_dict[key] = [file_name]

    value_new = []
    for key, value in result_dict.items():
        for string in value:
            value_new.append(path_to_wav + '\\' + string)
            output_file_path_new = f'audio\\audio_file\\{key}'
        concatenate_wav_files(value_new, output_file_path_new)
        for path in value_new:
            remove_file(path)
        value_new.clear()


def model_transform(ssml_sample, name, path_to_project):
    try:

        # Configuration settings
        sample_rate = 48000
        speaker = 'xenia'
        put_accent = True
        put_yo = True

        # Generate and save the audio
        audio_paths = model.save_wav(ssml_text=ssml_sample,
                                     speaker=speaker,
                                     sample_rate=sample_rate,
                                     put_accent=put_accent,
                                     put_yo=put_yo)

        print(path_to_project)  # Rename the output file
        rename_file(path_to_project, 'test.wav', f'audio\\audio_file\\{name}.wav')

        return audio_paths

    except Exception as e:
        print(f"An error occurred: {e}")

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")

    except Exception as e:
        print(f"Общая ошибка: {e}")


# Загрузка модели (выполняется один раз)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.package.PackageImporter('modelV3.pt').load_pickle("tts_models", "model")
model.to(device)


def convert_texts_to_audio(processed_texts, name_list, path_to_project, num_threads=8):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(model_transform, text, name, path_to_project)
                   for text, name in zip(processed_texts, name_list)]
        return [future.result() for future in futures]
