from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r"./assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_gui(file_name):
    subprocess.Popen(["python", file_name])
    window.after(100, window.destroy)

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

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_gui("gui4.py"),
    relief="flat"
)
button_1.place(x=367.0, y=154.0, width=299.0, height=108.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_gui("gui3.py"),
    relief="flat"
)
button_2.place(x=367.0, y=18.0, width=300.0, height=108.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_gui("gui2.py"),
    relief="flat"
)
button_3.place(x=32.0, y=154.0, width=300.0, height=104.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_gui("gui1.py"),
    relief="flat"
)
button_4.place(x=32.0, y=20.0, width=300.0, height=108.0)

window.resizable(False, False)
window.mainloop()
