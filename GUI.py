import tkinter as tk
from tkinter import filedialog, scrolledtext

# Функция для выбора файла
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        status_area.insert(tk.END, f"Выбран файл: {file_path}\n")
        global selected_file
        selected_file = file_path

# Функция для обработки файла
def process_file():
    if selected_file:
        output_area.insert(tk.END, f"Начало обработки файла: {selected_file}\n")
        # Пример обработки файла: читаем содержимое и выводим количество строк
        try:
            with open(selected_file, 'r', encoding='utf-8') as file:
                content = file.readlines()
                output_area.insert(tk.END, f"Файл содержит {len(content)} строк\n")
        except Exception as e:
            output_area.insert(tk.END, f"Ошибка при обработке файла: {str(e)}\n")
    else:
        output_area.insert(tk.END, "Ошибка: файл не выбран!\n")

# Инициализация главного окна
root = tk.Tk()
root.title("Приложение для обработки файлов")
root.geometry("600x400")

selected_file = None

# Меню
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Выбрать файл", command=select_file)

# Область для вывода общей информации
status_area = scrolledtext.ScrolledText(root, width=70, height=8, wrap=tk.WORD)
status_area.pack(pady=10)

# Область для вывода процесса обработки
output_area = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
output_area.pack(pady=10)

# Кнопка для начала обработки
process_button = tk.Button(root, text="Начать обработку", command=process_file)
process_button.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()
