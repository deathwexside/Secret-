import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys
import webbrowser

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

folders_state = {folder: True for folder in folders}

texts = {
    "ru": {
        "title": "AntiCheck",
        "hide": "Скрыть 🛑",
        "unhide": "Восстановить 🔄",
        "dev": "Разработчик 👨‍💻",
        "funpay": "FunPay 💰",
        "exit": "Выход ❌",
        "hide_done": "Я всё скрыл! 🛑",
        "unhide_done": "Я всё восстановил! 🔄",
        "add_folder": "Добавить папку",
        "remove_folder": "Удалить папку",
        "select_folders": "Выберите папки:",
        "lang_title": "Выбор языка"
    },
    "en": {
        "title": "AntiCheck",
        "hide": "Hide 🛑",
        "unhide": "Unhide 🔄",
        "dev": "Developer 👨‍💻",
        "funpay": "FunPay 💰",
        "exit": "Exit ❌",
        "hide_done": "Folders hidden! 🛑",
        "unhide_done": "Folders restored! 🔄",
        "add_folder": "Add Folder",
        "remove_folder": "Remove Folder",
        "select_folders": "Select folders to hide/unhide:",
        "lang_title": "Choose Language"
    },
    "uk": {
        "title": "АнтиЧек",
        "hide": "Сховати 🛑",
        "unhide": "Відновити 🔄",
        "dev": "Розробник 👨‍💻",
        "funpay": "FunPay 💰",
        "exit": "Вихід ❌",
        "hide_done": "Я все сховав! 🛑",
        "unhide_done": "Я все відновив! 🔄",
        "add_folder": "Додати папку",
        "remove_folder": "Видалити папку",
        "select_folders": "Виберіть папки для приховування/відновлення:",
        "lang_title": "Вибір мови"
    },
    "de": {
        "title": "AntiCheck",
        "hide": "Verstecken 🛑",
        "unhide": "Wiederherstellen 🔄",
        "dev": "Entwickler 👨‍💻",
        "funpay": "FunPay 💰",
        "exit": "Beenden ❌",
        "hide_done": "Alles versteckt! 🛑",
        "unhide_done": "Alles wiederhergestellt! 🔄",
        "add_folder": "Ordner hinzufügen",
        "remove_folder": "Ordner entfernen",
        "select_folders": "Ordner zum Verstecken/Wiederherstellen auswählen:",
        "lang_title": "Sprache wählen"
    }
}

current_lang = "ru"

def hide_folders():
    to_hide = [f for f, checked in folders_state.items() if checked]
    for folder in to_hide:
        if os.path.exists(folder):
            os.system(f'attrib +s +h "{folder}"')
    messagebox.showinfo(app_title.get(), texts[current_lang]["hide_done"], icon="info")

def unhide_folders():
    to_unhide = [f for f, checked in folders_state.items() if checked]
    for folder in to_unhide:
        if os.path.exists(folder):
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
    btn_add_folder.config(text=texts[lang_code]["add_folder"])
    btn_remove_folder.config(text=texts[lang_code]["remove_folder"])
    label_select.config(text=texts[lang_code]["select_folders"])

    # Обновить флаг на кнопке выбора языка
    flag_img = flag_images.get(lang_code)
    if flag_img:
        btn_lang.config(image=flag_img)
        btn_lang.image = flag_img

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

def add_folder():
    new_folder = filedialog.askdirectory()
    if new_folder:
        if new_folder not in folders_state:
            folders_state[new_folder] = True
            update_treeview()
        else:
            messagebox.showwarning(app_title.get(), "Folder already in list!")

def remove_folder():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        folder = tree.item(item, "text")
        if folder in folders_state:
            del folders_state[folder]
    update_treeview()
    btn_remove_folder.config(state="disabled")

def on_tree_select(event):
    selected = tree.selection()
    btn_remove_folder.config(state="normal" if selected else "disabled")

def toggle_check(event):
    item = tree.identify_row(event.y)
    if not item:
        return
    x, y, width, height = tree.bbox(item)
    if event.x < 20:
        folder = tree.item(item, "text")
        folders_state[folder] = not folders_state[folder]
        update_treeview()

def update_treeview():
    tree.delete(*tree.get_children())
    for folder, checked in folders_state.items():
        checkmark = "☑" if checked else "☐"
        tree.insert("", "end", text=folder, values=(checkmark,))

root = tk.Tk()
root.title("AntiCheck")
root.geometry("800x600")
root.configure(bg="#121212")
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (600 // 2)
root.geometry(f"800x600+{x}+{y}")

root.x = None
root.y = None

app_title = tk.StringVar(value=texts[current_lang]["title"])

# Логотип в меню (например, слева сверху)
try:
    logo_img = Image.open(resource_path("logo.png")).resize((64, 64), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
except Exception:
    logo_photo = None

frame_top = tk.Frame(root, bg="#121212")
frame_top.pack(fill="x", pady=5)

if logo_photo:
    label_logo = tk.Label(frame_top, image=logo_photo, bg="#121212")
    label_logo.pack(side="left", padx=15)

title_label = tk.Label(frame_top, textvariable=app_title, font=("Segoe UI Semibold", 24), fg="white", bg="#121212")
title_label.pack(side="left", padx=5)
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<ButtonRelease-1>", stop_move)
title_label.bind("<B1-Motion>", on_motion)

frame_left = tk.Frame(root, bg="#1e1e1e", bd=2, relief="groove")
frame_left.place(x=20, y=80, width=380, height=470)

label_select = tk.Label(frame_left, text=texts[current_lang]["select_folders"], fg="white", bg="#1e1e1e", font=("Segoe UI", 13))
label_select.pack(anchor="w", padx=10, pady=5)

tree = ttk.Treeview(frame_left, columns=("check",), show="tree", selectmode="extended")
tree.pack(fill="both", expand=True, padx=10, pady=5)

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#121212", foreground="white", fieldbackground="#121212", font=("Segoe UI", 11))
style.map('Treeview', background=[('selected', '#2a2a2a')], foreground=[('selected', 'white')])

scrollbar = ttk.Scrollbar(frame_left, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

tree.bind("<Button-1>", toggle_check)
tree.bind("<<TreeviewSelect>>", on_tree_select)

def insert_all():
    tree.delete(*tree.get_children())
    for folder, checked in folders_state.items():
        checkmark = "☑" if checked else "☐"
        tree.insert("", "end", text=folder, values=(checkmark,))

insert_all()

frame_buttons = tk.Frame(root, bg="#121212")
frame_buttons.place(x=20, y=560, width=380, height=30)

btn_add_folder = tk.Button(frame_buttons, text=texts[current_lang]["add_folder"], bg="#333", fg="white", font=("Segoe UI", 12), relief="flat", command=add_folder)
btn_add_folder.pack(side="left", padx=5, ipadx=5)

btn_remove_folder = tk.Button(frame_buttons, text=texts[current_lang]["remove_folder"], bg="#333", fg="white", font=("Segoe UI", 12), relief="flat", command=remove_folder, state="disabled")
btn_remove_folder.pack(side="left", padx=5, ipadx=5)

for btn in (btn_add_folder, btn_remove_folder):
    btn.bind("<Enter>", lambda e: e.widget.config(bg="#555"))
    btn.bind("<Leave>", lambda e: e.widget.config(bg="#333"))

frame_right = tk.Frame(root, bg="#121212")
frame_right.place(x=420, y=80, width=360, height=510)

btn_style = {
    "font": ("Segoe UI", 16),
    "bg": "#444",
    "fg": "white",
    "width": 20,
    "relief": "flat",
    "borderwidth": 0,
    "highlightthickness": 0,
    "activebackground": "#222",
    "activeforeground": "red"
}

btn_hide = tk.Button(frame_right, text=texts[current_lang]["hide"], command=hide_folders, **btn_style)
btn_hide.pack(pady=15)
btn_hide.bind("<Enter>", lambda e: e.widget.config(fg="red", bg="#222"))
btn_hide.bind("<Leave>", lambda e: e.widget.config(fg="white", bg="#444"))

btn_unhide = tk.Button(frame_right, text=texts[current_lang]["unhide"], command=unhide_folders, **btn_style)
btn_unhide.pack(pady=15)
btn_unhide.bind("<Enter>", lambda e: e.widget.config(fg="red", bg="#222"))
btn_unhide.bind("<Leave>", lambda e: e.widget.config(fg="white", bg="#444"))

btn_telegram = tk.Button(frame_right, text=texts[current_lang]["dev"], command=open_telegram, **btn_style)
btn_telegram.pack(pady=15)
btn_telegram.bind("<Enter>", lambda e: e.widget.config(fg="red", bg="#222"))
btn_telegram.bind("<Leave>", lambda e: e.widget.config(fg="white", bg="#444"))

btn_funpay = tk.Button(frame_right, text=texts[current_lang]["funpay"], command=open_funpay, **btn_style)
btn_funpay.pack(pady=15)
btn_funpay.bind("<Enter>", lambda e: e.widget.config(fg="red", bg="#222"))
btn_funpay.bind("<Leave>", lambda e: e.widget.config(fg="white", bg="#444"))

btn_exit = tk.Button(frame_right, text=texts[current_lang]["exit"], command=exit_app, **btn_style)
btn_exit.pack(pady=15)
btn_exit.bind("<Enter>", lambda e: e.widget.config(fg="red", bg="#222"))
btn_exit.bind("<Leave>", lambda e: e.widget.config(fg="white", bg="#444"))

# Загрузка флагов
flag_images = {}
for code in ("ru", "uk", "en", "de"):
    try:
        path = resource_path(f"{code}.png")
        img = Image.open(path).resize((32, 24), Image.LANCZOS)
        flag_images[code] = ImageTk.PhotoImage(img)
    except Exception:
        flag_images[code] = None

# Кнопка выбора языка с флагом
btn_lang = tk.Button(root, image=flag_images[current_lang], bg="#121212", bd=0, relief="flat", activebackground="#121212", highlightthickness=0)
btn_lang.place(x=760, y=10, width=32, height=24)

# Создаем выпадающее меню выбора языка с флагами
lang_menu = tk.Menu(root, tearoff=0, bg="#1e1e1e", fg="white", activebackground="#444", activeforeground="red", relief="flat", borderwidth=0)

def select_lang(code):
    change_language(code)
    lang_menu.unpost()

for code, lang_name in [("ru", "Русский"), ("uk", "Українська"), ("en", "English"), ("de", "Deutsch")]:
    img = flag_images.get(code)
    def _cmd(c=code):
        select_lang(c)
    lang_menu.add_command(label=lang_name, image=img, compound="left", command=_cmd)

def show_lang_menu(event=None):
    x = btn_lang.winfo_rootx()
    y = btn_lang.winfo_rooty() + btn_lang.winfo_height()
    lang_menu.tk_popup(x, y)

btn_lang.config(command=show_lang_menu)

def start_move_root(event):
    widget = event.widget
    # Проверяем, что клик не по tree или кнопкам
    if widget in (tree, btn_hide, btn_unhide, btn_telegram, btn_funpay, btn_exit, btn_add_folder, btn_remove_folder):
        return
    root.x = event.x_root
    root.y = event.y_root

def on_motion_root(event):
    if root.x is not None and root.y is not None:
        dx = event.x_root - root.x
        dy = event.y_root - root.y
        geom = root.geometry()
        # Получаем текущие координаты окна
        cur_x = root.winfo_x()
        cur_y = root.winfo_y()
        # Сдвигаем окно
        root.geometry(f"+{cur_x + dx}+{cur_y + dy}")
        root.x = event.x_root
        root.y = event.y_root

def stop_move_root(event):
    root.x = None
    root.y = None

# Привязываем к корневому окну
root.bind("<ButtonPress-1>", start_move_root)
root.bind("<B1-Motion>", on_motion_root)
root.bind("<ButtonRelease-1>", stop_move_root)

root.mainloop()
