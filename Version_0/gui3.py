import json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess

SETTINGS_FILE = "settings.json"
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/assets/frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_settings():
    try:
        settings["max_backups"] = int(entry_1.get("1.0", "end").strip())
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)
        update_display()
    except ValueError:
        print("Invalid input. Please enter a number.")

def update_display():
    entry_1.delete("1.0", "end")
    canvas.itemconfig(text_backupsize, text=f"{settings.get('max_backups', 'N/A')}")

def open_gui(file_name):
    subprocess.Popen(["python", file_name])
    window.after(100, window.destroy)

settings = load_settings()
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
canvas.create_image(350.0, 21.0, image=image_image_1)

canvas.create_text(527.0, 5.0, anchor="nw", text="Max Backups", fill="#FFA3A3", font=("Montserrat Bold", 20 * -1))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: open_gui("gui.py"), relief="flat")
button_1.place(x=6.0, y=5.0, width=67.0, height=27.0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(170.5, 102.5, image=entry_image_1)

entry_1 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=39.0, y=82.0, width=263.0, height=39.0)
entry_1.insert("1.0", str(settings.get("max_backups", "")))

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=save_settings, relief="flat")
button_2.place(x=60.0, y=149.0, width=221.503662109375, height=43.0)

canvas.create_text(465.0, 73.0, anchor="nw", text="Current Backups", fill="#FFFFFF", font=("Montserrat ExtraBold", 16 * -1))

text_backupsize = canvas.create_text(525.0, 107.0, anchor="nw", text=f"{settings.get('max_backups', 'N/A')}", fill="#575757", font=("Montserrat ExtraBold", 32 * -1))

canvas.create_text(48.0, 223.0, anchor="nw", text="Informationstext", fill="#FFFFFF", font=("Montserrat ExtraBold", 10 * -1))

window.resizable(False, False)
update_display()
window.mainloop()
