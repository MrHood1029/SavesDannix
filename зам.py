import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
from collections import OrderedDict # Для Python < 3.7

# Настройки по умолчанию
имя_файла_данных = "alphabet_notes.json"
имя_файла_настроек = "settings.json"
алфавит = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
данные = {}
текстовые_поля = {}
текущая_тема = "светлая" #  или "темная"

# ========= A: Функции управления данными =========

def создать_запись():
    раздел = ttk.Notebook.select(notebook)
    if раздел is None:
        messagebox.showerror("Ошибка", "Выберите раздел!")
        return

    название = simpledialog.askstring("Новая запись", "Название:")
    if название:
        содержание = simpledialog.askstring("Новая запись", "Содержание:")
        if содержание:
            добавить_запись_в_раздел(раздел, название, содержание)
            сохранить_данные()

def добавить_запись_в_раздел(раздел, название, содержание):
    global данные
    раздел_текст = notebook.tab(раздел, "text")
    данные[раздел_текст][название] = содержание
    данные[раздел_текст] = OrderedDict(sorted(данные[раздел_текст].items(), key=lambda item: item[0]))  # Сортировка и OrderedDict
    обновить_отображение_раздела(раздел)

def редактировать_запись():
    раздел = ttk.Notebook.select(notebook)
    if раздел is None:
        messagebox.showerror("Ошибка", "Выберите раздел!")
        return

    раздел_текст = notebook.tab(раздел, "text")
    название = simpledialog.askstring("Редактировать", "Название для редактирования:")

    if название:
        if название in данные[раздел_текст]:
            содержание = simpledialog.askstring("Редактировать", "Новое содержание:", initialvalue=данные[раздел_текст][название])
            if содержание:
                данные[раздел_текст][название] = содержание
                обновить_отображение_раздела(раздел)
                сохранить_данные()
        else:
            messagebox.showerror("Ошибка", "Запись не найдена.")

def удалить_запись():
    раздел = ttk.Notebook.select(notebook)
    if раздел is None:
        messagebox.showerror("Ошибка", "Выберите раздел!")
        return

    раздел_текст = notebook.tab(раздел, "text")
    название = simpledialog.askstring("Удалить", "Название для удаления:")

    if название:
        if название in данные[раздел_текст]:
            if messagebox.askyesno("Подтверждение", f"Удалить '{название}'?"):
                del данные[раздел_текст][название]
                обновить_отображение_раздела(раздел)
                сохранить_данные()
        else:
            messagebox.showerror("Ошибка", "Запись не найдена.")

def обновить_отображение_раздела(раздел):
    global данные
    раздел_текст = notebook.tab(раздел, "text")
    текстовое_поле = текстовые_поля[раздел_текст]
    текстовое_поле.delete("1.0", tk.END)

    if раздел_текст in данные:
        for название, содержание in данные[раздел_текст].items():
            текстовое_поле.insert(tk.END, f"{название}:\n{содержание}\n\n")

def сохранить_данные():
    try:
        with open(имя_файла_данных, "w", encoding="utf-8") as f:
            json.dump(данные, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

def загрузить_данные():
    global данные
    try:
        with open(имя_файла_данных, "r", encoding="utf-8") as f:
            данные = json.load(f, object_pairs_hook=OrderedDict)  # OrderedDict при загрузке

            for раздел in данные:
                данные[раздел] = OrderedDict(sorted(данные[раздел].items(), key=lambda item: item[0]))
    except FileNotFoundError:
        данные = OrderedDict() # OrderedDict для хранения данных
        for буква in алфавит:
            данные[буква] = OrderedDict() # И для каждого раздела
        сохранить_данные()
        messagebox.showinfo("Информация", "Файл данных создан.")
    except json.JSONDecodeError:
        данные = OrderedDict()
        for буква in алфавит:
            данные[буква] = OrderedDict()
        сохранить_данные()
        messagebox.showerror("Ошибка", "Ошибка чтения данных. Создан новый файл.")
    except Exception as e:
        данные = OrderedDict()
        for буква in алфавит:
            данные[буква] = OrderedDict()
        сохранить_данные()
        messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")

# ========= B: Функции управления темой =========

def загрузить_настройки():
    global текущая_тема
    try:
        with open(имя_файла_настроек, "r") as f:
            настройки = json.load(f)
            текущая_тема = настройки.get("тема", "светлая") # Значение по умолчанию
    except FileNotFoundError:
        сохранить_настройки() # Создаем файл настроек с темой по умолчанию
    except Exception as e:
        print(f"Ошибка при загрузке настроек: {e}")
        текущая_тема = "светлая"  # Возвращаемся к теме по умолчанию

def сохранить_настройки():
    настройки = {"тема": текущая_тема}
    try:
        with open(имя_файла_настроек, "w") as f:
            json.dump(настройки, f, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения настроек: {e}")

def переключить_тему():
    global текущая_тема
    if текущая_тема == "светлая":
        текущая_тема = "темная"
    else:
        текущая_тема = "светлая"
    применить_тему()
    сохранить_настройки()

def применить_тему():
    global bg_color, text_color, highlight_color

    if текущая_тема == "светлая":
        bg_color = "#F0F0F0"
        text_color = "#333333"
        highlight_color = "#ADD8E6"
    else:
        bg_color = "#333333"
        text_color = "#F0F0F0"
        highlight_color = "#666666"

    root.configure(bg=bg_color)

    стиль.configure("TNotebook", background=bg_color, borderwidth=0)
    стиль.configure("TNotebook.Tab", background=bg_color, borderwidth=0, padding=[10, 5])
    стиль.map("TNotebook.Tab", background=[("selected", highlight_color)])

    стиль.configure("TButton", background=bg_color, foreground=text_color, padding=[8, 4])
    стиль.map("TButton", background=[("active", highlight_color)])

    стиль.configure("TLabel", background=bg_color, foreground=text_color)

    for текстовое_поле in текстовые_поля.values():
        текстовое_поле.configure(bg="white" if текущая_тема == "светлая" else "#444444", fg=text_color)

# ========= C:  Создание GUI =========

root = tk.Tk()
root.title("Алфавитный Заметкин")
root.geometry("800x600")

стиль = ttk.Style() # Создаем стиль перед использованием

загрузить_настройки()
применить_тему()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

for буква in алфавит:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=буква)

    текстовое_поле = tk.Text(frame, wrap=tk.WORD, bg="white" if текущая_тема == "светлая" else "#444444", fg=text_color, font=("Arial", 12))
    текстовое_поле.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    текстовые_поля[буква] = текстовое_поле

frame_кнопок = ttk.Frame(root, padding=10)
frame_кнопок.pack()

кнопка_создать = ttk.Button(frame_кнопок, text="Создать", command=создать_запись)
кнопка_создать.pack(side=tk.LEFT, padx=5)

кнопка_редактировать = ttk.Button(frame_кнопок, text="Редактировать", command=редактировать_запись)
кнопка_редактировать.pack(side=tk.LEFT, padx=5)

кнопка_удалить = ttk.Button(frame_кнопок, text="Удалить", command=удалить_запись)
кнопка_удалить.pack(side=tk.LEFT, padx=5)

кнопка_тема = ttk.Button(frame_кнопок, text="Сменить тему", command=переключить_тему)
кнопка_тема.pack(side=tk.LEFT, padx=5)

# ========= D: Загрузка и отображение данных =========

загрузить_данные()

for буква in алфавит:
    if буква not in данные:
        данные[буква] = OrderedDict()

for i, буква in enumerate(алфавит):
    раздел = notebook.tabs()[i]
    обновить_отображение_раздела(раздел)

# ========= E: Запуск GUI =========

root.mainloop()