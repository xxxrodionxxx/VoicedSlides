from cx_Freeze import setup, Executable
import sys
import os

# Базовый путь для включения файлов
base_path = os.path.abspath(os.path.dirname(__file__))

# Определяем, является ли это Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Файлы и директории для включения
include_files = [
    # Директории
    (os.path.join(base_path, "audio"), "audio"),
    (os.path.join(base_path, "dictionaries"), "dictionaries"),
    (os.path.join(base_path, "text"), "text"),
    (os.path.join(base_path, "ui"), "ui"),
    (os.path.join(base_path, "utils"), "utils"),
    (os.path.join(base_path, "video"), "video"),
    # Отдельные файлы
    (os.path.join(base_path, "config.ini"), "config.ini"),
    (os.path.join(base_path, "modelV3.pt"), "modelV3.pt"),
]

# Зависимости с точными версиями
# packages = {
#     "numpy": "1.26.4",
#     "torch": "2.3.0",
#     "PySide6": "6.7.3",
#     "moviepy": "1.0.3",
#     "SpeechRecognition": "3.8.1",  # speech_recognition в requirements
#     "num2words": "0.5.13",
#     "imageio": "2.34.1",
#     "imageio-ffmpeg": "0.4.9",
#     "tqdm": "4.66.2",
#     "Pillow": "10.3.0",  # PIL в requirements
#     "requests": "2.31.0",
#     # Дополнительные зависимости с версиями
#     "beautifulsoup4": "4.8.2",
#     "networkx": "3.3",
#     "sympy": "1.12",
#     "python-ffmpeg": "2.0.12",
#     "future": "1.0.0",
#     "lxml": "5.2.1",
#     "mpmath": "1.3.0",
#     "pycryptodome": "3.20.0",
# }
packages = {
    "argcomplete": "1.10.3",
    "art": "6.2",
    "beautifulsoup4": "4.8.2",
    "certifi": "2024.2.2",
    "chardet": "3.0.4",
    "charset_normalizer": "3.3.2",
    "colorama": "0.4.6",
    "compressed-rtf": "1.0.6",
    "decorator": "4.4.2",
    "docopt": "0.6.2",
    "docx2txt": "0.8",
    "ebcdic": "1.1.1",
    "extract_msg": "0.28.7",
    "filelock": "3.14.0",
    "fsspec": "2024.3.1",
    "idna": "3.7",
    "imageio": "2.34.1",
    "imageio_ffmpeg": "0.4.9",
    "IMAPClient": "2.1.0",
    "intel-openmp": "2021.4.0",
    "Jinja2": "3.1.3",
    "line_profiler_pycharm": "1.1.0",
    "line_profiler": "4.1.3",
    "lxml": "5.2.1",
    "markupsafe": "2.1.5",
    "mkl": "2021.4.0",
    "moviepy": "1.0.3",
    "mpmath": "1.3.0",
    "networkx": "3.3",
    "num2words": "0.5.13",
    "numpy": "1.26.4",
    "olefile": "0.47",
    "pdfminer.six": "20191110",
    "pillow": "10.3.0",
    "proglog": "0.1.10",
    "pycryptodome": "3.20.0",
    "python_pptx": "0.6.23",
    "pywin32": "306",
    "requests": "2.31.0",
    "six": "1.12.0",
    "sortedcontainers": "2.4.0",
    "soupsieve": "2.5",
    "speech_recognition": "3.8.1",
    "sympy": "1.12",
    "tbb": "2021.12.0",
    "textract": "1.6.5",
    "torch": "2.3.0",
    "tqdm": "4.66.2",
    "typing_extensions": "4.11.0",
    "tzdata": "2024.1",
    "tzlocal": "5.2",
    "urllib3": "2.2.1",
    "xlrd": "1.2.0",
    "XlsxWriter": "3.2.0",
    "PySide6": "6.7.3",
    "future": "1.0.0",
    "python-ffmpeg": "2.0.12"
}


# Преобразуем словарь в список для options
package_list = list(packages.keys())

# Дополнительные модули
includes = [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "numpy.core._methods",
    "numpy.lib.format",
]

# Исключаемые модули
excludes = [
    "tkinter",
    "unittest",
    "email",
    "http",
    "xml",
    "pydoc",
    "intel-openmp",  # Исключаем проблемный модуль
    "mkl",
    "tbb",
]

# Опции сборки
build_options = {
    "packages": package_list,
    "excludes": excludes,
    "includes": includes,
    "include_files": include_files,
    "build_exe": "build/VoicedSlides",
    "optimize": 2,
    # Добавляем необходимые DLL для работы с аудио и видео
    "include_msvcr": True,
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
    # Добавляем пути для поиска модулей
    "path": sys.path + ["modules"],
    # Дополнительные опции для обработки зависимостей
    "constants": {
        "OLEFILE_DISABLE_OLEFILE2": "1"  # Отключаем проблемный модуль olefile2
    }
}

# Создаем requirements.txt с точными версиями
with open('requirements_frozen.txt', 'w') as f:
    for package, version in packages.items():
        f.write(f"{package}=={version}\n")

# Создаем исполняемые файлы
executables = [
    Executable(
        "main_ui_pyside6.py",
        base=base,
        target_name="VoicedSlides.exe",
        icon=None,  # Здесь можно указать путь к иконке
        shortcut_name="VoicedSlides",
        shortcut_dir="DesktopFolder",
        copyright="Your Copyright Info",
    )
]

setup(
    name="VoicedSlides",
    version="1.0.0",
    description="VoicedSlides Application",
    options={"build_exe": build_options},
    executables=executables,
    author="Mordus Radion",
    # Добавляем зависимости с версиями для pip
    install_requires=[f"{package}=={version}" for package, version in packages.items()],
)
