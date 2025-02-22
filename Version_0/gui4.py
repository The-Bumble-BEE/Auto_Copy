import json
import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

SETTINGS_PATH = Path(r"settings.json")
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_settings():
    with open(SETTINGS_PATH, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as file:
        json.dump(settings, file, indent=4)

def update_backup_interval():
    try:
        new_interval = int(entry_1.get("1.0", "end").strip())
        settings = load_settings()
        settings["backup_intervall"] = new_interval
        save_settings(settings)
        canvas.itemconfig(intervall_text, text=str(new_interval))
        print(f"Backup-Intervall auf {new_interval} geändert.")
    except ValueError:
        print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

def open_gui(file_name):
    subprocess.Popen(["python", file_name])
    window.after(100, window.destroy)

settings = load_settings()
current_interval = settings.get("backup_intervall", "Unbekannt")

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

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(569.0, 19.0, image=image_image_4)

canvas.create_text(
    465.0, 73.0,
    anchor="nw",
    text="Current Intervall",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 16 * -1)
)

canvas.create_text(
    591.0, 4.0,
    anchor="nw",
    text="Intervall",
    fill="#FFA3A3",
    font=("Montserrat Bold", 20 * -1)
)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(538.0, 103.0, image=image_image_3)

canvas.create_text(
    465.0,
    73.0,
    anchor="nw",
    text="Current Intervall",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 16 * -1)
)


intervall_text = canvas.create_text(
    510.0, 107.0,
    anchor="nw",
    text=str(current_interval),
    fill="#575757",
    font=("Montserrat ExtraBold", 10 * -1)
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_gui("gui.py"),
    relief="flat"
)
button_1.place(x=6.0, y=5.0, width=67.0, height=27.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(170.0, 103.0, image=image_image_2)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(170.5, 102.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=39.0, y=82.0, width=263.0, height=39.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=update_backup_interval,
    relief="flat"
)
button_2.place(x=60.0, y=149.0, width=221.5, height=43.0)

window.resizable(False, False)
window.mainloop()
