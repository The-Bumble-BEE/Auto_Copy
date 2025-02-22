import json
from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Button, PhotoImage, Text
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame1")
SETTINGS_PATH = Path(r"./settings.json")  # Pfad zur settings.json

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_gui(file_name):
    subprocess.Popen(["python", file_name])
    window.after(100, window.destroy)

def load_settings():
    """Lädt die aktuellen Einstellungen aus der JSON-Datei."""
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {}

def save_settings(new_sync_folders):
    """Speichert die aktualisierten Einstellungen in der JSON-Datei."""
    settings = load_settings()
    settings["sync_ordner"] = new_sync_folders
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
    update_current_folders_display(new_sync_folders)

def update_current_folders_display(sync_folders):
    """Aktualisiert die Anzeige der 'Current folders' Liste."""
    current_folders_text = "\n".join(sync_folders) if sync_folders else "Keine Ordner vorhanden"
    canvas.itemconfig(current_folders_text, text=current_folders_text)

def add_sync_folder():
    """Fügt einen neuen Ordner zur Liste der synchronisierten Ordner hinzu."""
    new_folder = entry_1.get("1.0", "end-1c").strip()
    if new_folder:
        current_folders = load_settings().get("sync_ordner", [])
        if new_folder not in current_folders:
            current_folders.append(new_folder)
            save_settings(current_folders)
            # Leere das Eingabefeld nach dem Hinzufügen des Ordners
            entry_1.delete("1.0", "end")
            # Stelle sicher, dass die Ordneranzeige nach dem Hinzufügen aktualisiert wird
            update_folder_list(current_folders)
        else:
            messagebox.showwarning("Warnung", "Dieser Ordner ist bereits in der Liste.")
    else:
        messagebox.showwarning("Fehler", "Bitte einen Ordner eingeben.")



def delete_sync_folder():
    """Löscht einen ausgewählten Ordner aus der Liste der synchronisierten Ordner."""
    folder_to_delete = entry_1.get("1.0", "end-1c").strip()
    if folder_to_delete:
        current_folders = load_settings().get("sync_ordner", [])
        if folder_to_delete in current_folders:
            current_folders.remove(folder_to_delete)
            save_settings(current_folders)
            # Stelle sicher, dass die Ordneranzeige nach dem Löschen aktualisiert wird
            entry_1.delete("1.0", "end")
            update_folder_list(current_folders)
        else:
            messagebox.showwarning("Fehler", "Ordner nicht in der Liste.")
    else:
        messagebox.showwarning("Fehler", "Bitte einen Ordner zum Löschen eingeben.")


# Fenster konfigurieren
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

canvas.create_text(
    546.0, 5.0, anchor="nw", text="Local folders", fill="#FFA3A3", font=("Montserrat Bold", 20 * -1)
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
image_2 = canvas.create_image(183.0, 115.0, image=image_image_2)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(183.5, 114.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=52.0, y=94.0, width=263.0, height=39.0)

# Lade die aktuellen Ordner und setze sie als Standardtext
settings = load_settings()
sync_folders = settings.get("sync_ordner", [])
sync_folders_text = "\n".join(sync_folders)
entry_1.insert("1.0", sync_folders_text)

button_image_2 = PhotoImage(file=relative_to_assets("button_3.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=add_sync_folder,
    relief="flat"
)
button_2.place(x=199.0, y=172.0, width=129.0, height=43.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_2.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=delete_sync_folder,
    relief="flat"
)
button_3.place(x=39.0, y=172.0, width=129.0, height=43.0)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(532.0, 159.0, image=image_image_3)

canvas.create_text(
    396.0, 55.0, anchor="nw", text="Current folders", fill="#FFFFFF", font=("Montserrat ExtraBold", 16 * -1)
)

def on_folder_click(event, folder_name):
    """Setzt den angeklickten Ordner in das Textfeld."""
    entry_1.delete("1.0", "end")
    entry_1.insert("1.0", folder_name)

def update_folder_list(sync_folders):
    entry_1.delete("1.0", "end")
    # Lösche alle bestehenden Ordnertexte
    folder_items = canvas.find_withtag("folder_text")

    for item in folder_items:
        canvas.delete(item)

    # Füge die neuen Ordner in die Anzeige ein
    y_position = 90
    for folder in sync_folders:
        folder_text = canvas.create_text(
            396.0,
            y_position,
            anchor="nw",
            text=folder,
            fill="#575757",
            font=("Montserrat ExtraBold", 10 * -1),
            tags="folder_text"
        )

        # Übergabe der folder-Variable explizit als Argument
        def on_folder_click_with_folder_name(event, folder_name=folder):
            on_folder_click(event, folder_name)
        
        canvas.tag_bind(folder_text, "<Button-1>", on_folder_click_with_folder_name)
        y_position += 20

def print_canvas_content():
    all_items = canvas.find_all()  # Alle Canvas-Elemente abrufen
    for item in all_items:
        # Versuche, den Text des Elements zu holen
        try:
            item_text = canvas.itemcget(item, "text")  # Hole den Text-Inhalt des Items
            print(f"Element-ID: {item}, Text: {item_text}")
        except Exception as e:
            # Falls es sich nicht um ein Text-Element handelt, gebe eine Nachricht aus
            print(f"Element-ID: {item} ist kein Text-Element, Fehler: {e}")


update_folder_list(sync_folders)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(521.0, 19.0, image=image_image_4)

window.resizable(False, False)
window.mainloop()
