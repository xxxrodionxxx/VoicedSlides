import os
import multiprocessing
from ffmpeg import FFmpeg
import subprocess


def get_audio_duration(audio_path):
    """Получает длительность аудиофайла с помощью ffprobe"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    duration = float(result.stdout)
    return duration


def video_creation_with_statusbar_ffmpeg(path_image: str, path_audio: str, file_path_pptx: str, codec: str):
    # Создаем директорию для выходного файла, если её нет
    os.makedirs('./output', exist_ok=True)

    # Список файлов изображений и аудио
    image_files = sorted(os.listdir(path_image), key=lambda x: int(x.split('_')[1][:-4]))
    audio_files = sorted(os.listdir(path_audio), key=lambda x: int(x.split('audio')[1][:-4]))

    # Подготовка имени выходного файла
    output_filename = os.path.splitext(os.path.basename(file_path_pptx))[0] + '.mp4'
    output_path = os.path.join('./output', output_filename)

    # Создаем временные директории для промежуточных файлов
    os.makedirs('temp_segments', exist_ok=True)

    segments = []

    try:
        # Создаем видеосегмент для каждой пары изображение-аудио
        for i, (img, aud) in enumerate(zip(image_files, audio_files)):
            img_path = os.path.join(path_image, img)
            aud_path = os.path.join(path_audio, aud)

            # Получаем длительность аудио
            duration = get_audio_duration(aud_path)

            # Создаем видео из изображения с нужной длительностью
            segment_path = f'temp_segments/segment_{i}.mp4'
            ffmpeg_image = (
                FFmpeg()
                .option('y')
                .option('loop', '1')  # зацикливаем изображение
                .input(img_path)
                .input(aud_path)
                .output(segment_path, {
                    'c:v': codec,
                    'c:a': 'aac',
                    'vf': 'scale=1600:-1',
                    't': str(duration),  # устанавливаем длительность равной длительности аудио
                    'shortest': None,
                    'preset': 'medium',
                    'crf': '23'
                })
            )
            ffmpeg_image.execute()
            segments.append(segment_path)

        # Создаем файл со списком сегментов
        with open('segments.txt', 'w', encoding='utf-8') as f:
            for segment in segments:
                f.write(f"file '{segment}'\n")

        # Объединяем все сегменты
        ffmpeg_concat = (
            FFmpeg()
            .option('y')
            .option('f', 'concat')
            .option('safe', '0')
            .input('segments.txt')
            .output(output_path, {
                'c:v': 'copy',  # просто копируем видеопоток
                'c:a': 'copy'  # просто копируем аудиопоток
            })
        )
        ffmpeg_concat.execute()

        print(f"Видео успешно создано: {output_path}")

    finally:
        # Удаляем временные файлы
        if os.path.exists('segments.txt'):
            os.remove('segments.txt')
        for segment in segments:
            if os.path.exists(segment):
                os.remove(segment)
        if os.path.exists('temp_segments'):
            os.rmdir('temp_segments')