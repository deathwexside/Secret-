import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import webbrowser

def resource_path(relative_path):
    """Путь к файлу, учитывая режим exe или dev"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Папки для скрытия
folders = [
    "C:\\Nurik",
    "C:\\Nursultan",
    "C:\\Celestial",
    "C:\\DeltaClient",
    "C:\\Catlavan",
    "C:\\.wexside",
    "C:\\Wild",
    "C:\\Expensive"
]

texts = {
    "ru": {"title": "AntiCheck", "hide": "Скрыть 🛑", "unhide": "Восстановить 🔄",
           "dev": "Разработчик 👨‍💻", "funpay": "FunPay 💰", "exit": "Выход ❌",
           "hide_done": "Я всё скрыл! 🛑", "unhide_done": "Я всё восстановил! 🔄"},
    "en": {"title": "AntiCheck", "hide": "Hide 🛑", "unhide": "Unhide 🔄",
           "dev": "Developer 👨‍💻", "funpay": "FunPay 💰", "exit": "Exit ❌",
           "hide_done": "Folders hidden! 🛑", "unhide_done": "Folders restored! 🔄"},
    "uk": {"title": "АнтиЧек", "hide": "Сховати 🛑", "unhide": "Відновити 🔄",
           "dev": "Розробник 👨‍💻", "funpay": "FunPay 💰", "exit": "Вихід ❌",
           "hide_done": "Я все сховав! 🛑", "unhide_done": "Я все відновив! 🔄"},
    "de": {"title": "AntiCheck", "hide": "Verstecken 🛑", "unhide": "Wiederherstellen 🔄",
           "dev": "Entwickler 👨‍💻", "funpay": "FunPay 💰", "exit": "Beenden ❌",
           "hide_done": "Alles versteckt! 🛑", "unhide_done": "Alles wiederhergestellt! 🔄"},
}

current_lang = "ru"

def hide_folders():
    for folder in folders:
        os.system(f'attrib +s +h "{folder}"')
    messagebox.showinfo(app_title.get(), texts[current_lang]["hide_done"], icon="info")

def unhide_folders():
    for folder in folders:
        os.system(f'attrib -s -h "{folder}"')
    messagebox.showinfo(app_title.get(), texts[current_lang]["unhide_done"], icon="info")

def exit_app():
    root.destroy()

def open_telegram():
    webbrowser.open("https://t.me/devarovFWK")

def open_funpay():
    webbrowser.open("https://funpay.com/users/7836130/")

def change_language(lang_code):
    global current_lang
    current_lang = lang_code
    app_title.set(texts[lang_code]["title"])
    btn_hide.config(text=texts[lang_code]["hide"])
    btn_unhide.config(text=texts[lang_code]["unhide"])
    btn_telegram.config(text=texts[lang_code]["dev"])
    btn_funpay.config(text=texts[lang_code]["funpay"])
    btn_exit.config(text=texts[lang_code]["exit"])
    btn_lang.config(image=flags[lang_code])

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    if root.x is not None and root.y is not None:
        x = root.winfo_pointerx() - root.x
        y = root.winfo_pointery() - root.y
        root.geometry(f"+{x}+{y}")

def toggle_language_menu():
    if lang_menu.winfo_ismapped():
        lang_menu.unpost()
    else:
        x = btn_lang.winfo_rootx()
        y = btn_lang.winfo_rooty() + btn_lang.winfo_height()
        lang_menu.post(x, y)

def on_lang_select(lang_code):
    change_language(lang_code)
    lang_menu.unpost()

# Инициализация окна
root = tk.Tk()
root.title("AntiCheck")
root.geometry("600x520")
root.configure(bg="black")
root.overrideredirect(True)  # Без стандартного заголовка

# Центрирование окна
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (520 // 2)
root.geometry(f"600x520+{x}+{y}")

root.x = None
root.y = None

# Загрузка изображений
def load_img(filename, size=None):
    path = resource_path(filename)
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

logo_img = load_img("logo.png", (150, 150))

flags = {
    "ru": load_img("flag_ru.png", (32, 20)),
    "en": load_img("flag_en.png", (32, 20)),
    "uk": load_img("flag_uk.png", (32, 20)),
    "de": load_img("flag_de.png", (32, 20)),
}

# Интерфейс

logo_label = tk.Label(root, image=logo_img, bg="black")
logo_label.pack(pady=10)
logo_label.bind("<ButtonPress-1>", start_move)
logo_label.bind("<ButtonRelease-1>", stop_move)
logo_label.bind("<B1-Motion>", on_motion)

app_title = tk.StringVar(value=texts[current_lang]["title"])
title_label = tk.Label(root, textvariable=app_title, font=("Segoe UI Semibold", 20), fg="white", bg="black")
title_label.pack(pady=10)
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<ButtonRelease-1>", stop_move)
title_label.bind("<B1-Motion>", on_motion)

btn_style = {
    "font": ("Segoe UI", 14),
    "bg": "#444",
    "fg": "white",
    "width": 18,
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "activebackground": "#222",
    "activeforeground": "red"
}

def on_enter(e):
    e.widget.config(fg="red", bg="#222")

def on_leave(e):
    e.widget.config(fg="white", bg="#444")

btn_hide = tk.Button(root, text=texts[current_lang]["hide"], command=hide_folders, **btn_style)
btn_hide.pack(pady=6)
btn_hide.bind("<Enter>", on_enter)
btn_hide.bind("<Leave>", on_leave)

btn_unhide = tk.Button(root, text=texts[current_lang]["unhide"], command=unhide_folders, **btn_style)
btn_unhide.pack(pady=6)
btn_unhide.bind("<Enter>", on_enter)
btn_unhide.bind("<Leave>", on_leave)

btn_telegram = tk.Button(root, text=texts[current_lang]["dev"], command=open_telegram, **btn_style)
btn_telegram.pack(pady=6)
btn_telegram.bind("<Enter>", on_enter)
btn_telegram.bind("<Leave>", on_leave)

btn_funpay = tk.Button(root, text=texts[current_lang]["funpay"], command=open_funpay, **btn_style)
btn_funpay.pack(pady=6)
btn_funpay.bind("<Enter>", on_enter)
btn_funpay.bind("<Leave>", on_leave)

btn_exit = tk.Button(root, text=texts[current_lang]["exit"], command=exit_app, **btn_style)
btn_exit.pack(pady=10)
btn_exit.bind("<Enter>", on_enter)
btn_exit.bind("<Leave>", on_leave)

# Языковое меню справа вверху
btn_lang = tk.Button(root, image=flags[current_lang], bg="black", relief="flat", command=toggle_language_menu)
btn_lang.place(x=560, y=10, width=32, height=20)

lang_menu = tk.Menu(root, tearoff=0)
for code, img in flags.items():
    lang_menu.add_command(label=code.upper(), image=img, compound="left", command=lambda c=code: on_lang_select(c))

# Перетаскивание окна за любое место (кроме кнопок)
def start_move_all(event):
    widget = event.widget
    if isinstance(widget, tk.Button) or isinstance(widget, tk.Menu):
        return
    start_move(event)

def stop_move_all(event):
    stop_move(event)

def on_motion_all(event):
    on_motion(event)

root.bind("<ButtonPress-1>", start_move_all)
root.bind("<ButtonRelease-1>", stop_move_all)
root.bind("<B1-Motion>", on_motion_all)

root.mainloop()
