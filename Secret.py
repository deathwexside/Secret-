import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys
import webbrowser
import shutil
import send2trash
import glob
import pystray
from threading import Thread

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
        "support": "Поддержать 💖",
        "exit": "Выход ❌",
        "hide_done": "Я всё скрыл! 🛑",
        "unhide_done": "Я всё восстановил! 🔄",
        "add_folder": "Добавить папку",
        "remove_folder": "Удалить папку",
        "select_folders": "Выберите папки:",
        "lang_title": "Выбор языка",
        "clear_history": "Очистить историю 🗑️",
        "history_cleared": "История и загрузки очищены!",
        "history_error": "Не удалось очистить историю. Закройте браузеры и попробуйте снова.",
        "no_files_found": "Файлы истории или загрузок не найдены.",
        "tray_show": "Показать",
        "tray_hide": "Скрыть",
        "tray_exit": "Выход"
    },
    "en": {
        "title": "AntiCheck",
        "hide": "Hide 🛑",
        "unhide": "Unhide 🔄",
        "dev": "Developer 👨‍💻",
        "funpay": "FunPay 💰",
        "support": "Support 💖",
        "exit": "Exit ❌",
        "hide_done": "Folders hidden! 🛑",
        "unhide_done": "Folders restored! 🔄",
        "add_folder": "Add Folder",
        "remove_folder": "Remove Folder",
        "select_folders": "Select folders to hide/unhide:",
        "lang_title": "Choose Language",
        "clear_history": "Clear History 🗑️",
        "history_cleared": "History and downloads cleared!",
        "history_error": "Failed to clear history. Close browsers and try again.",
        "no_files_found": "No history or download files found.",
        "tray_show": "Show",
        "tray_hide": "Hide",
        "tray_exit": "Exit"
    },
    "uk": {
        "title": "АнтиЧек",
        "hide": "Сховати 🛑",
        "unhide": "Відновити 🔄",
        "dev": "Розробник 👨‍💻",
        "funpay": "FunPay 💰",
        "support": "Підтримати 💖",
        "exit": "Вихід ❌",
        "hide_done": "Я все сховав! 🛑",
        "unhide_done": "Я все відновив! 🔄",
        "add_folder": "Додати папку",
        "remove_folder": "Видалити папку",
        "select_folders": "Виберіть папки для приховування/відновлення:",
        "lang_title": "Вибір мови",
        "clear_history": "Очистити історію 🗑️",
        "history_cleared": "Історію та завантаження очищено!",
        "history_error": "Не вдалося очистити історію. Закрийте браузери та спробуйте ще раз.",
        "no_files_found": "Файли історії або завантажень не знайдено.",
        "tray_show": "Показати",
        "tray_hide": "Сховати",
        "tray_exit": "Вихід"
    },
    "de": {
        "title": "AntiCheck",
        "hide": "Verstecken 🛑",
        "unhide": "Wiederherstellen 🔄",
        "dev": "Entwickler 👨‍💻",
        "funpay": "FunPay 💰",
        "support": "Unterstützen 💖",
        "exit": "Beenden ❌",
        "hide_done": "Alles versteckt! 🛑",
        "unhide_done": "Alles wiederhergestellt! 🔄",
        "add_folder": "Ordner hinzufügen",
        "remove_folder": "Ordner entfernen",
        "select_folders": "Ordner zum Verstecken/Wiederherstellen auswählen:",
        "lang_title": "Sprache wählen",
        "clear_history": "Verlauf löschen 🗑️",
        "history_cleared": "Verlauf und Downloads gelöscht!",
        "history_error": "Verlauf konnte nicht gelöscht werden. Schließen Sie Browser und versuchen Sie es erneut.",
        "no_files_found": "Keine Verlaufs- oder Download-Dateien gefunden.",
        "tray_show": "Anzeigen",
        "tray_hide": "Verstecken",
        "tray_exit": "Beenden"
    }
}

current_lang = "ru"

def custom_messagebox(title, message, icon="info"):
    """Кастомная функция для messagebox с логотипом"""
    msg_box = tk.Toplevel(root)
    msg_box.title(title)
    msg_box.configure(bg="#121212")
    msg_box.geometry("300x150")
    msg_box.resizable(False, False)

    if logo_photo_message:
        msg_box.iconphoto(True, logo_photo_message)
    else:
        print("Иконка окна сообщения (logo.ico) не загружена")

    screen_width = msg_box.winfo_screenwidth()
    screen_height = msg_box.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (150 // 2)
    msg_box.geometry(f"300x150+{x}+{y}")

    label = tk.Label(msg_box, text=message, fg="white", bg="#121212", font=("Segoe UI", 12), wraplength=250)
    label.pack(pady=20)

    ok_button = tk.Button(msg_box, text="OK", command=msg_box.destroy, bg="#444", fg="white", font=("Segoe UI", 12), relief="groove", borderwidth=4, width=10)
    ok_button.pack(pady=10, padx=10)
    ok_button.bind("<Enter>", lambda e: e.widget.config(fg="red"))
    ok_button.bind("<Leave>", lambda e: e.widget.config(fg="white"))

    msg_box.transient(root)
    msg_box.grab_set()
    root.wait_window(msg_box)

def delete_configs(folder):
    config_extensions = ['*.wex', '*.json', '*.cfg', '*.config', '*.celka']
    for ext in config_extensions:
        for file in glob.glob(os.path.join(folder, ext)):
            try:
                os.remove(file)  # ✅ это полное удаление
                print(f"Удалён файл: {file}")
            except Exception as e:
                print(f"Ошибка при удалении {file}: {e}")


def clear_browser_history():
    """Очищает историю и загрузки популярных браузеров"""
    user_home = os.path.expanduser("~")
    browser_paths = {
        'Chrome History': os.path.join(user_home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'),
        'Chrome Downloads': os.path.join(user_home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Web Data'),
        'Firefox History': os.path.join(user_home, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles', '*', 'places.sqlite'),
        'Firefox Downloads (legacy)': os.path.join(user_home, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles', '*', 'downloads.json'),
        'Edge History': os.path.join(user_home, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History'),
    }


    success = False
    files_found = False

    for name, path in browser_paths.items():
        try:
            matched_files = glob.glob(path, recursive=True)
            if not matched_files:
                print(f"Файлы не найдены для {name}: {path}")
                continue
            files_found = True
            for file in matched_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                        print(f"Удалён файл: {file}")
                        success = True
                    except Exception as e:
                        print(f"Ошибка при удалении {file}: {e}")
                else:
                    print(f"Файл не существует: {file}")
        except Exception as e:
            print(f"Ошибка при обработке {name} ({path}): {e}")

    return success, files_found

def hide_folders():
    to_hide = [f for f, checked in folders_state.items() if checked]
    for folder in to_hide:
        if os.path.exists(folder):
            os.system(f'attrib +s +h "{folder}"')
            delete_configs(folder)
    custom_messagebox(app_title.get(), texts[current_lang]["hide_done"], icon="info")

def unhide_folders():
    to_unhide = [f for f, checked in folders_state.items() if checked]
    for folder in to_unhide:
        if os.path.exists(folder):
            os.system(f'attrib -s -h "{folder}"')
    custom_messagebox(app_title.get(), texts[current_lang]["unhide_done"], icon="info")

def clear_history():
    success, files_found = clear_browser_history()
    if success:
        custom_messagebox(app_title.get(), texts[current_lang]["history_cleared"], icon="info")
    elif files_found:
        custom_messagebox(app_title.get(), texts[current_lang]["history_error"], icon="warning")
    else:
        custom_messagebox(app_title.get(), texts[current_lang]["no_files_found"], icon="info")

def support_coder():
    webbrowser.open("https://www.donationalerts.com/r/devarov")

def exit_app():
    icon.stop()  # Остановить системный трей
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
    btn_support.config(text=texts[lang_code]["support"])
    btn_exit.config(text=texts[lang_code]["exit"])
    btn_add_folder.config(text=texts[lang_code]["add_folder"])
    btn_remove_folder.config(text=texts[lang_code]["remove_folder"])
    btn_clear_history.config(text=texts[lang_code]["clear_history"])
    label_select.config(text=texts[lang_code]["select_folders"])

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
            custom_messagebox(app_title.get(), "Папка уже в списке!", icon="warning")

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

def show_window():
    root.deiconify()
    root.lift()

def hide_window():
    root.withdraw()

def create_system_tray():
    try:
        icon_path = resource_path("logo.ico")
        image = Image.open(icon_path)
        menu = (
            pystray.MenuItem(texts[current_lang]["tray_show"], show_window),
            pystray.MenuItem(texts[current_lang]["tray_hide"], hide_window),
            pystray.MenuItem(texts[current_lang]["tray_exit"], exit_app)
        )
        global icon
        icon = pystray.Icon("AntiCheck", image, "AntiCheck", menu)
        icon.run()
    except Exception as e:
        print(f"Ошибка создания системного трея: {e}")

root = tk.Tk()
root.title("AntiCheck")
root.geometry("800x750")
root.configure(bg="#121212")
root.overrideredirect(True)

# Загрузка логотипа для окон сообщений и главного окна
logo_photo_message = None
try:
    logo_img_message = Image.open(resource_path("logo.ico")).resize((32, 32), Image.LANCZOS)
    logo_photo_message = ImageTk.PhotoImage(logo_img_message)
except Exception as e:
    print(f"Ошибка загрузки logo.ico для окон: {e}")

# Загрузка логотипа для верхнего фрейма
logo_photo = None
try:
    logo_img_frame = Image.open(resource_path("logo.ico")).resize((64, 64), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img_frame)
except Exception as e:
    print(f"Ошибка загрузки logo.ico для фрейма: {e}")

# Установка иконки главного окна
if logo_photo_message:
    root.iconphoto(True, logo_photo_message)
else:
    print("Иконка главного окна (logo.ico) не загружена")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (750 // 2)
root.geometry(f"800x750+{x}+{y}")

root.x = None
root.y = None

app_title = tk.StringVar(value=texts[current_lang]["title"])

frame_top = tk.Frame(root, bg="#121212")
frame_top.pack(fill="x", pady=5)

if logo_photo:
    label_logo = tk.Label(frame_top, image=logo_photo, bg="#121212")
    label_logo.pack(side="left", padx=15)
else:
    print("Логотип в верхнем фрейме (logo.ico) не загружен")

title_label = tk.Label(frame_top, textvariable=app_title, font=("Segoe UI Semibold", 24), fg="white", bg="#121212")
title_label.pack(side="left", padx=5)
title_label.bind("<ButtonPress-1>", start_move)
title_label.bind("<ButtonRelease-1>", stop_move)
title_label.bind("<B1-Motion>", on_motion)

frame_left = tk.Frame(root, bg="#1e1e1e", bd=2, relief="groove")
frame_left.place(x=20, y=80, width=380, height=620)

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
frame_buttons.place(x=20, y=710, width=380, height=30)

btn_add_folder = tk.Button(frame_buttons, text=texts[current_lang]["add_folder"], bg="#333", fg="white", font=("Segoe UI", 12), relief="groove", borderwidth=4, width=15, command=add_folder)
btn_add_folder.pack(side="left", padx=10)
btn_add_folder.bind("<Enter>", lambda e: e.widget.config(fg="red"))
btn_add_folder.bind("<Leave>", lambda e: e.widget.config(fg="white"))

btn_remove_folder = tk.Button(frame_buttons, text=texts[current_lang]["remove_folder"], bg="#333", fg="white", font=("Segoe UI", 12), relief="groove", borderwidth=4, width=15, command=remove_folder, state="disabled")
btn_remove_folder.pack(side="left", padx=10)
btn_remove_folder.bind("<Enter>", lambda e: e.widget.config(fg="red"))
btn_remove_folder.bind("<Leave>", lambda e: e.widget.config(fg="white"))

frame_right = tk.Frame(root, bg="#121212")
frame_right.place(x=420, y=80, width=360, height=660)

btn_style = {
    "font": ("Segoe UI", 16),
    "bg": "#444",
    "fg": "white",
    "width": 20,
    "relief": "groove",
    "borderwidth": 4,
    "activebackground": "#444",
    "activeforeground": "red"
}

def on_button_enter(event):
    event.widget.config(fg="red")

def on_button_leave(event):
    event.widget.config(fg="white")

btn_hide = tk.Button(frame_right, text=texts[current_lang]["hide"], command=hide_folders, **btn_style)
btn_hide.pack(pady=20, padx=10)
btn_hide.bind("<Enter>", on_button_enter)
btn_hide.bind("<Leave>", on_button_leave)

btn_unhide = tk.Button(frame_right, text=texts[current_lang]["unhide"], command=unhide_folders, **btn_style)
btn_unhide.pack(pady=20, padx=10)
btn_unhide.bind("<Enter>", on_button_enter)
btn_unhide.bind("<Leave>", on_button_leave)

btn_clear_history = tk.Button(frame_right, text=texts[current_lang]["clear_history"], command=clear_history, **btn_style)
btn_clear_history.pack(pady=20, padx=10)
btn_clear_history.bind("<Enter>", on_button_enter)
btn_clear_history.bind("<Leave>", on_button_leave)

btn_telegram = tk.Button(frame_right, text=texts[current_lang]["dev"], command=open_telegram, **btn_style)
btn_telegram.pack(pady=20, padx=10)
btn_telegram.bind("<Enter>", on_button_enter)
btn_telegram.bind("<Leave>", on_button_leave)

btn_funpay = tk.Button(frame_right, text=texts[current_lang]["funpay"], command=open_funpay, **btn_style)
btn_funpay.pack(pady=20, padx=10)
btn_funpay.bind("<Enter>", on_button_enter)
btn_funpay.bind("<Leave>", on_button_leave)

btn_support = tk.Button(frame_right, text=texts[current_lang]["support"], command=support_coder, **btn_style)
btn_support.pack(pady=20, padx=10)
btn_support.bind("<Enter>", on_button_enter)
btn_support.bind("<Leave>", on_button_leave)

btn_exit = tk.Button(frame_right, text=texts[current_lang]["exit"], command=exit_app, **btn_style)
btn_exit.pack(pady=20, padx=10)
btn_exit.bind("<Enter>", on_button_enter)
btn_exit.bind("<Leave>", on_button_leave)

flag_images = {}
for code in ("ru", "uk", "en", "de"):
    try:
        path = resource_path(f"{code}.png")
        img = Image.open(path).resize((32, 24), Image.LANCZOS)
        flag_images[code] = ImageTk.PhotoImage(img)
    except Exception:
        flag_images[code] = None

btn_lang = tk.Button(root, image=flag_images[current_lang], bg="#121212", bd=0, relief="flat", activebackground="#121212")
btn_lang.place(x=760, y=10, width=32, height=24)

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
    if widget in (tree, btn_hide, btn_unhide, btn_telegram, btn_funpay, btn_exit, btn_add_folder, btn_remove_folder, btn_clear_history, btn_support):
        return
    root.x = event.x_root
    root.y = event.y_root

def on_motion_root(event):
    if root.x is not None and root.y is not None:
        dx = event.x_root - root.x
        dy = event.y_root - root.y
        geom = root.geometry()
        cur_x = root.winfo_x()
        cur_y = root.winfo_y()
        root.geometry(f"+{cur_x + dx}+{cur_y + dy}")
        root.x = event.x_root
        root.y = event.y_root

def stop_move_root(event):
    root.x = None
    root.y = None

root.bind("<ButtonPress-1>", start_move_root)
root.bind("<B1-Motion>", on_motion_root)
root.bind("<ButtonRelease-1>", stop_move_root)

# Запуск системного трея в отдельном потоке
tray_thread = Thread(target=create_system_tray, daemon=True)
tray_thread.start()

root.mainloop()
