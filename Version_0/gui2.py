import json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

SETTINGS_FILE = "settings.json"
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Desktop\Tkinter designer Output\build\assets\frame2")

import subprocess
def open_gui(file_name):
    subprocess.Popen(["python", file_name])
    window.after(100, window.destroy)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)

def update_sync_device(new_path):
    settings = load_settings()
    settings["sync_device"] = new_path
    save_settings(settings)
    canvas.itemconfig(label_backup_folder, text=new_path)

def add_sync_device():
    new_path = entry_1.get("1.0", "end").strip()
    if new_path:
        update_sync_device(new_path)

def remove_sync_device():
    update_sync_device("")

settings = load_settings()
current_sync_device = settings.get("sync_device", "Nicht gesetzt")

window = Tk()
window.geometry("700x280")
window.configure(bg="#B0B0B0")

canvas = Canvas(
    window,
    bg="#B0B0B0",
    height=280,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(350.0, 21.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1, borderwidth=0, highlightthickness=0, relief="flat", command=lambda: open_gui("gui.py"),
)
button_1.place(x=6.0, y=5.0, width=67.0, height=27.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(167.0, 115.0, image=image_image_2)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(167.5, 114.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=36.0, y=94.0, width=263.0, height=39.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=remove_sync_device, relief="flat")
button_2.place(x=183.0, y=172.0, width=129.0, height=43.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=add_sync_device, relief="flat")
button_3.place(x=23.0, y=172.0, width=129.0, height=43.0)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(535.0, 115.0, image=image_image_3)

canvas.create_text(
    527.0, 5.0, anchor="nw", text="Backup device", fill="#FFA3A3", font=("Montserrat Bold", 20 * -1)
)

canvas.create_text(
    469.0,
    82.0,
    anchor="nw",
    text="Backup device",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 16 * -1)
)


label_backup_folder = canvas.create_text(490.0, 119.0, anchor="nw", text=current_sync_device, fill="#575757", font=("Montserrat ExtraBold", 10 * -1))

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(497.0, 21.0, image=image_image_4)

window.resizable(False, False)
window.mainloop()
