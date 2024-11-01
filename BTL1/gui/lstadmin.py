from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
from tkinter import ttk
import os

def GUILISTADMIN(response, titlename):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "assets" / "frame4"

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title("DANH SÁCH CÁC PEER - BK FILE SHARING")
    window.geometry("1200x700")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=700,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        100.0,
        1200.0,
        700.0,
        fill="#EBF5F5",
        outline=""
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        1200.0,
        100.0,
        fill="#0688B4",
        outline=""
    )

    # image_image_1 = PhotoImage(
    #     file=relative_to_assets("image_1.png"))
    # image_1 = canvas.create_image(
    #     66.0,
    #     50.0,
    #     image=image_image_1
    # )

    canvas.create_text(
        334.0,
        34.0,
        anchor="nw",
        text="HỆ THỐNG CHIA SẺ TỆP BK FILE SHARING",
        fill="#FFFFFF",
        font=("Inter", 20, "bold")
    )

    canvas.create_rectangle(
        1.0,
        674.0,
        1201.0,
        700.0,
        fill="#6D98D7",
        outline=""
    )

    canvas.create_text(
        31.0,
        677.0,
        anchor="nw",
        text="COPYRIGHT 2024 BK FILE SHARING",
        fill="#FFFFFF",
        font=("Inter SemiBold", 14 * -1)
    )

    canvas.create_text(
        31.0,
        120.0,
        anchor="nw",
        text=titlename,
        fill="#0688B4",
        font=("Inter", 16, "bold")
    )

    # Tạo khung cho Treeview
    frame = Frame(window)
    frame.place(x=31.0, y=159.0, width=1138.0, height=490.0)

    # Tạo bảng Treeview
    tree = ttk.Treeview(frame, columns=("ID", "IP", "Port", "Hostname"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("IP", text="IP")
    tree.heading("Port", text="Port")
    tree.heading("Hostname", text="Hostname")

    for idx, (IP, port, hostname) in enumerate(response, start=1):
        tree.insert("", "end", values=(str(idx), IP, str(port), hostname))

    # Đặt scrollbar cho Treeview
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)

    window.resizable(False, False)
    window.mainloop()
