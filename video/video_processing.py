import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import multiprocessing


def video_creation(path_image: str, path_audio: str, file_path_pptx: str, codec: str):
    # Список файлов изображений
    image_files = sorted(os.listdir(path_image), key=lambda x: int(x.split('_')[1][:-4]))

    # Список аудиофайлов
    audio_files = sorted(os.listdir(path_audio), key=lambda x: int(x.split('audio')[1][:-4]))

    # Создание видеоклипов из изображений и аудио
    video_clips = []
    for img, aud in zip(image_files, audio_files):
        image_clip = ImageClip(os.path.join(path_image, img))
        audio_clip = AudioFileClip(os.path.join(path_audio, aud))
        image_clip = image_clip.set_duration(audio_clip.duration)
        video_clip = image_clip.set_audio(audio_clip)
        video_clips.append(video_clip)

    # Объединение видеоклипов
    final_clip = concatenate_videoclips(video_clips, method="compose")

    # Подготовка имени выходного файла
    output_filename = os.path.splitext(os.path.basename(file_path_pptx))[0] + '.mp4'
    output_path = os.path.join('./output', output_filename)

    # Определение количества ядер процессора
    num_threads = multiprocessing.cpu_count()

    # Сохранение видеофайла
    final_clip.write_videofile(
        output_path,
        codec=codec,  # Используем x264 кодек, который хорошо оптимизирован для Intel
        audio_codec='aac',
        fps=24,
        threads=num_threads,  # Используем все доступные ядра
        preset='medium',  # Баланс между скоростью и качеством
        # bitrate='5000k',  # Установите подходящий битрейт
        # audio_bitrate='192k'
    )
